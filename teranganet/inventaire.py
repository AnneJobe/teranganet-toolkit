import yaml


class Site:
    def __init__(self, code, nom, latitude, longitude):
        self.code = code
        self.nom = nom
        self.latitude = latitude
        self.longitude = longitude


class Equipement:
    def __init__(self, nom, type, ip, statut, site, exterieur):
        self.nom = nom
        self.type = type
        self.ip = ip
        self.statut = statut
        self.site = site
        self.exterieur = exterieur


def trouver_site(code, sites):
    for site in sites:
        if site.code == code:
            return site


def trouver_equipement(nom, equipements):
    for equipement in equipements:
        if equipement.nom == nom:
            return equipement


def charger_inventaire(chemin_fichier):
    try:
        with open(chemin_fichier, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Erreur : le fichier '{chemin_fichier}' est introuvable.")
        return None, None
    except yaml.YAMLError:
        print(f"Erreur : le fichier '{chemin_fichier}' contient du YAML mal formé.")
        return None, None

    sites = []
    for site_dict in data["sites"]:
        site = Site(
            site_dict["code"],
            site_dict["nom"],
            site_dict["latitude"],
            site_dict["longitude"]
        )
        sites.append(site)

    equipements = []
    for equipement_dict in data["equipements"]:
        site = trouver_site(equipement_dict["site"], sites)
        equipement = Equipement(
            equipement_dict["nom"],
            equipement_dict["type"],
            equipement_dict["ip"],
            equipement_dict["statut"],
            site,
            equipement_dict["exterieur"]
        )
        equipements.append(equipement)

    return sites, equipements