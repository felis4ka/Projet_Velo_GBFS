import re
from velo.models import Station, StationStatus


def is_out_of_service(status: StationStatus) -> bool:
    """Retourne True si la station est hors service."""
    return not (status.is_installed and status.is_renting and status.is_returning)


def is_empty(status: StationStatus) -> bool:
    """Retourne True si la station est en service mais n'a aucun vélo disponible."""
    return not is_out_of_service(status) and status.bikes == 0


def is_full(status: StationStatus) -> bool:
    """Retourne True si la station est en service mais n'a plus de places libres."""
    return not is_out_of_service(status) and status.docks == 0


def compute_network_status(
    stations: list[Station],
    statuses: list[StationStatus],
) -> dict[str, int | float]:
    """Calcule les statistiques globales du réseau pour la commande 'velo status'."""
    status_by_id = {s.station_id: s for s in statuses}

    total_stations = len(stations)
    out_of_service = 0
    empty = 0
    full = 0
    available_bikes = 0
    available_docks = 0

    for station in stations:
        status = status_by_id.get(station.station_id)
        if status is None or is_out_of_service(status):
            out_of_service += 1
            continue

        if is_empty(status):
            empty += 1
        if is_full(status):
            full += 1

        available_bikes += status.bikes
        available_docks += status.docks

    in_service = total_stations - out_of_service
    total_slots = available_bikes + available_docks
    fill_rate = round((available_bikes / total_slots) * 100, 1) if total_slots > 0 else 0.0

    return {
        "total_stations": total_stations,
        "in_service": in_service,
        "out_of_service": out_of_service,
        "empty": empty,
        "full": full,
        "available_bikes": available_bikes,
        "available_docks": available_docks,
        "fill_rate": fill_rate,
    }


def list_stations(stations: list[Station]) -> list[Station]:
    """Retourne la liste des stations triée par nom (pour 'velo station list')."""
    return sorted(stations, key=lambda s: s.name.lower())


def search_stations(stations: list[Station], pattern: str) -> list[Station]:
    """Recherche les stations dont le nom correspond au motif regex (insensible à la casse)."""
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error as exc:
        raise ValueError(f"Expression régulière invalide : {pattern!r}") from exc

    matches = [s for s in stations if regex.search(s.name)]
    return sorted(matches, key=lambda s: s.name.lower())