import json
import os
from datetime import datetime

from teranganet.audit import auditer_site


def construire_rapport(sites, equipements, seuils):
    resultats = []
    for site in sites:
        resultat = auditer_site(site, equipements, seuils)
        if resultat is None:
            print(f"Avertissement : site {site.code} ignoré (données météo indisponibles).")
            continue
        resultats.append({
            "site": {
                "code": resultat["site"].code,
                "nom": resultat["site"].nom,
                "latitude": resultat["site"].latitude,
                "longitude": resultat["site"].longitude,
            },
            "vent": resultat["vent"],
            "temperature": resultat["temperature"],
            "alertes": resultat["alertes"],
        })
    return {
        "horodatage": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sites": resultats,
    }


def ecrire_rapport(rapport, dossier="rapports"):
    os.makedirs(dossier, exist_ok=True)
    horodatage = datetime.now().strftime("%Y-%m-%d_%H%M")
    chemin_fichier = os.path.join(dossier, f"audit_{horodatage}.json")
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    return chemin_fichier