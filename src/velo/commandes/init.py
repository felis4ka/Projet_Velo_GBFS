from pathlib import Path


def init():
    config_dir = Path.home() / ".config" / "velo"
    config_fichier = config_dir / "config.yaml"
    data_dir = Path.home() / ".local" / "share" / "velo"

    config_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    if config_fichier.exists():
        print(f"La configuration existe déjà : {config_fichier}")
    else:
        config = """network:
  name: V'Lille
  gbfs_url: https://media.ilevia.fr/opendata/gbfs.json

data:
  folder: ~/.local/share/velo
"""

        config_fichier.write_text(config, encoding="utf-8")
        print(f"Configuration créée : {config_fichier}")

    print(f"Dossier de données créé : {data_dir}")