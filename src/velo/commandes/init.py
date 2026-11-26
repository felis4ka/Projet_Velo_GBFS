from pathlib import Path
import requests

def init():
    config_dir = Path.home() / ".config" / "velo"
    config_fichier = config_dir / "config.yaml"
    data_dir = Path.home() / ".local" / "share" / "velo"

    config_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    if config_fichier.exists():
        print(f"La configuration existe déjà : {config_fichier}")
    else:
        print(f"Configuration créée : {config_fichier}")

    print(f"Dossier de données créé : {data_dir}/")

    url = "https://media.ilevia.fr/opendata/"    
    data = [
        "system_information.json",
        "station_information.json",
        "vehicle_types.json"
    ]

    nb_stations = 0
    connexion_ok = True

    for donnees in data:
        try:
            reponse = requests.get(url + donnees)
            reponse.raise_for_status()

            (data_dir / donnees).write_text(reponse.text, encoding='utf-8')
            if donnees == "station_information.json":
                donnees_json = reponse.json()
                nb_stations = len(donnees_json["data"]["stations"])

        except Exception:
            connexion_ok = False

    if connexion_ok:
        print(f"Connexion à V'Lille : OK ({nb_stations} stations)")
    else:
        print("Echec de la connexion à V'Lille")



