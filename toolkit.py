import argparse
import sys

from teranganet.inventaire import charger_inventaire, trouver_equipement, trouver_site
from teranganet.meteo import meteo_actuelle


def commande_inventaire():
    sites, equipements = charger_inventaire("data/equipements.yaml")
    print(f"=== Inventaire TerangaNet — {len(equipements)} équipements, {len(sites)} sites ===")
    for e in equipements:
        print(e.site.code, f"({e.site.nom})", e.nom, e.type, e.ip, e.statut)


def commande_show(nom):
    sites, equipements = charger_inventaire("data/equipements.yaml")
    equipement = trouver_equipement(nom, equipements)
    if equipement is None:
        print(f"Erreur : aucun équipement nommé '{nom}' dans l'inventaire.")
        return
    print(f"{equipement.nom} — {equipement.type}")
    print(f" Site : {equipement.site.code} ({equipement.site.nom}) · lat {equipement.site.latitude}, lon {equipement.site.longitude}")
    print(f" IP : {equipement.ip}")
    print(f" Statut : {equipement.statut}")


def commande_meteo(code_site):
    sites, equipements = charger_inventaire("data/equipements.yaml")

    site = trouver_site(code_site, sites)

    if site is None:
        print(f"Erreur : aucun site avec le code '{code_site}' dans l'inventaire.")
        return

    data = meteo_actuelle(site.latitude, site.longitude)

    if data is None:
        return

    current = data["current"]

    print(f"Météo actuelle — {site.nom} ({site.latitude}, {site.longitude})")
    print(f" Température : {current['temperature_2m']} °C")
    print(f" Vent : {current['wind_speed_10m']} km/h")
    print(f" (source : API Open-Meteo, code HTTP {data['status_code']})")


def main():
    parser = argparse.ArgumentParser(description="TerangaNet Ops Toolkit")
    parser.add_argument("commande", choices=["inventaire", "show", "meteo"])
    parser.add_argument("argument", nargs="?", default=None)
    args = parser.parse_args()

    if args.commande == "inventaire":
        commande_inventaire()
    elif args.commande == "show":
        if args.argument is None:
            print("Erreur : la commande 'show' nécessite un nom d'équipement.")
            return
        commande_show(args.argument)
    elif args.commande == "meteo":
        if args.argument is None:
            print("Erreur : la commande 'meteo' nécessite un code de site.")
            return
        commande_meteo(args.argument)


if __name__ == "__main__":
    main()