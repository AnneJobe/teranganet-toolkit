import requests


def meteo_actuelle(lat, lon):
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,wind_speed_10m"
            },
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        print("Erreur : impossible de se connecter à l'API météo (vérifiez votre connexion).")
        return None
    except requests.exceptions.Timeout:
        print("Erreur : l'API météo met trop de temps à répondre.")
        return None

    if 400 <= response.status_code < 500:
        print(f"Erreur : requête invalide (code HTTP {response.status_code}). Vérifiez les paramètres envoyés.")
        return None
    elif response.status_code >= 500:
        print(f"Erreur : problème côté serveur météo (code HTTP {response.status_code}). Réessayez plus tard.")
        return None

    data = response.json()
    data["status_code"] = response.status_code
    return data