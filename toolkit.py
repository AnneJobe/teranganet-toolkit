import argparse
import sys

from teranganet.inventaire import charger_inventaire, trouver_equipement


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


def main():
    parser = argparse.ArgumentParser(description="TerangaNet Ops Toolkit")
    parser.add_argument("commande", choices=["inventaire", "show"])
    parser.add_argument("argument", nargs="?", default=None)
    args = parser.parse_args()

    if args.commande == "inventaire":
        commande_inventaire()
    elif args.commande == "show":
        if args.argument is None:
            print("Erreur : la commande 'show' nécessite un nom d'équipement.")
            return
        commande_show(args.argument)


if __name__ == "__main__":
    main()