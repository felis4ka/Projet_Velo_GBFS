import json 
from pathlib import Path 
from velo.models import Station, StationStatus

MAX_FAVORITES = 10 

def load_favorites(favorites_path: Path) -> list[str]:
    """Charge la liste des indentifiants des stations favorites depuis le fichier JSON."""
    if not favorites_path.exists():
        return[]
    
    try :
        content = favorites_path.read_text(encoding="utf-8")
        data = json.loads(content)
        if not isinstance(data, list):
            raise ValueError("Le format du fichier des favoris est invalide.")
        return [str(item) for item in data]
    except json.JSONDecodeError as exc : 
        raise ValueError(f"Erreur de lecture du fichier des favoris : {exc}") from exc


def save_favorites(favorites_path: Path, favorite_ids: list[str]) -> None:
    """Enregistre la liste des identifiants favoris dans le fichier JSON."""
    favorites_path.parent.mkdir(parents=True, exist_ok=True),
    encoding="utf-8",


def add_favorites(
    favorite_path: Path, station_id: str, stations: list[Station]
) -> list[str]:
    """Ajoute une station aux favoris après vérification des règles métier."""
    valid_ids = {s.station_id for s in stations}
    if station_id not in valid_ids:
        raise ValueError(f"Identifiant de station inconnu : {station_id}")

    
    favorites = load_favorites(favorite_path)

    if station_id in favorites:
        raise ValueError(f"La station {station_id} est déjà dans vos favoris.")
    
    if len(favorites) >= MAX_FAVORITES:
        raise ValueError(f"Limite de {MAX_FAVORITES} favoris atteinte."
        "Retirez un favori avec 'velo favorites remove <id>' avant d'en ajouter.")

    favorites.append(station_id)
    save_favorites(favorites_path, favorites)
    return favorites


def remove_favorite(favorites_path: Path, station_id: str) -> list[str]:
    """Retire une station des favoris."""
    favorites = load_favorites(favorites_path)

    if station_id not in favorites:
        raise ValueError(f"La station {station_id} n'est pas dans vos favoris.")

    favorites.remove(station_id)
    save_favorites(favorites_path, favorites)
    return(favorites)

def get_favorite_details(
    favorites_path: Path,
    stations: list[Station],
    statuses: list[StationStatus],
) -> list[tuple[Station, StationStatus | None ]]: 
    """Retourne les paires (Station, StationStatus) pour chaque station favorite."""
    favorite_ids = load_favorites(favorites_path)
    stations_by_id = {s.station_id: s for s in stations}
    statuses_by_id = {st.station_id: st for st in statuses}

    result: list[tuple[Station, StationStatus | None]] = []
    for fav_id in favorite_ids:
        station = stations_by_id.get(fav_id)
        if station is not None:
            result.append((station, statuses_by_id.get(fav_id)))
    return result
