import argparse
import json
import os
import sys
from teranganet.inventaire import charger_inventaire, trouver_equipement, trouver_site
from teranganet.meteo import meteo_actuelle
from teranganet.audit import charger_config, auditer_site
from teranganet.rapport import construire_rapport, ecrire_rapport, lister_rapports, charger_dernier_rapport
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
def commande_audit():
    sites, equipements = charger_inventaire("data/equipements.yaml")
    seuils = charger_config("config.yaml")
    nombre_alertes = 0
    for site in sites:
        resultat = auditer_site(site, equipements, seuils)
        alertes = resultat["alertes"]
        if not alertes:
            message_alerte = "OK"
        else:
            nombre_alertes += 1
            messages = []
            if "VENT" in alertes:
                messages.append("[ALERTE VENT]")
            if "TEMPERATURE" in alertes:
                messages.append("[ALERTE TEMPÉRATURE]")
            message_alerte = " ".join(messages)
        print(
            f"{resultat['site'].code} ({resultat['site'].nom}) "
            f"vent {resultat['vent']} km/h "
            f"temp {resultat['temperature']} °C "
            f"{message_alerte}"
        )
    nombre_exterieurs = sum(
        1 for equipement in equipements
        if equipement.exterieur is True
    )
    print(
        f"Bilan : {nombre_alertes} alertes sur {len(sites)} sites. "
        f"Équipements extérieurs exposés au vent : {nombre_exterieurs}."
    )
def commande_rapport():
    sites, equipements = charger_inventaire("data/equipements.yaml")
    seuils = charger_config("config.yaml")
    rapport = construire_rapport(sites, equipements, seuils)
    chemin_fichier = ecrire_rapport(rapport)
    print(f"Rapport écrit : {chemin_fichier}")
def commande_historique():
    fichiers = lister_rapports()
    if not fichiers:
        print("Aucun rapport trouvé dans le dossier 'rapports/'.")
        return
    print(f"=== Historique des rapports — {len(fichiers)} rapport(s) ===")
    for nom_fichier in fichiers:
        chemin = os.path.join("rapports", nom_fichier)
        with open(chemin, "r", encoding="utf-8") as f:
            rapport = json.load(f)
        nombre_alertes = sum(1 for s in rapport["sites"] if s["alertes"])
        print(f"{nom_fichier} — {rapport['horodatage']} — {nombre_alertes} alerte(s) sur {len(rapport['sites'])} site(s)")
    if len(fichiers) >= 2:
        chemin_avant_dernier = os.path.join("rapports", fichiers[-2])
        with open(chemin_avant_dernier, "r", encoding="utf-8") as f:
            avant_dernier = json.load(f)
        dernier = charger_dernier_rapport()
        alertes_avant = sum(1 for s in avant_dernier["sites"] if s["alertes"])
        alertes_dernier = sum(1 for s in dernier["sites"] if s["alertes"])
        print()
        print(f"Comparaison avec le rapport précédent ({avant_dernier['horodatage']} -> {dernier['horodatage']}) :")
        if alertes_dernier > alertes_avant:
            print(f" Dégradation : {alertes_avant} -> {alertes_dernier} alertes.")
        elif alertes_dernier < alertes_avant:
            print(f" Amélioration : {alertes_avant} -> {alertes_dernier} alertes.")
        else:
            print(f" Stable : {alertes_dernier} alertes.")
def main():
    parser = argparse.ArgumentParser(description="TerangaNet Ops Toolkit")
    parser.add_argument("commande", choices=["inventaire", "show", "meteo", "audit", "rapport", "historique"])
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
    elif args.commande == "audit":
        commande_audit()
    elif args.commande == "rapport":
        commande_rapport()
    elif args.commande == "historique":
        commande_historique()
if __name__ == "__main__":
    main()