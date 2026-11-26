from pathlib import Path
import requests


def refresh():
    data_dir = Path.home() / ".local" / "share" / "velo"

    url = "https://media.ilevia.fr/opendata/gbfs.json"
    data = [
        "system_information.json",
        "station_information.json",
        "vehicle_types.json"
    ]

    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        donnees_json = reponse.json()

        for donnees in data:
            for fichier in donnees_json["data"]["en"]["feeds"]:
                if fichier["name"] == donnees.replace(".json", ""):
                    reponse = requests.get(fichier["url"])
                    reponse.raise_for_status()

                    (data_dir / donnees).write_text(
                        reponse.text,
                        encoding="utf-8"
                    )

        print("Les données ont été actualisées.")

    except Exception:
        print("Les données ne se sont pas actualisées.")

