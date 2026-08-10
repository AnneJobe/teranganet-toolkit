
import yaml


def charger_config(chemin_fichier):
    with open(chemin_fichier, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["seuils"]


def calculer_alertes(vent, temperature, seuil_vent, seuil_temperature, a_equipement_exterieur):
    alertes = []

    if a_equipement_exterieur and vent >= seuil_vent:
        alertes.append("VENT")

    if temperature >= seuil_temperature:
        alertes.append("TEMPERATURE")

    return alertes
def auditer_site(site, equipements, seuils):
    from teranganet.meteo import meteo_actuelle

    data = meteo_actuelle(site.latitude, site.longitude)
    if data is None:
        return None

    vent = data["current"]["wind_speed_10m"]
    temperature = data["current"]["temperature_2m"]

    a_equipement_exterieur = any(e.exterieur for e in equipements if e.site.code == site.code)

    alertes = calculer_alertes(vent, temperature, seuils["vent_kmh"], seuils["temperature_c"], a_equipement_exterieur)

    return {
        "site": site,
        "vent": vent,
        "temperature": temperature,
        "alertes": alertes
    }


