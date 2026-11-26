from rich.console import Console
from rich.table import Table
from velo.models import Station, StationStatus
from velo.stations import is_empty, is_full, is_out_of_service

console = Console()


def display_network_status(
    network_name: str,
    updated_at: str,
    stats: dict[str, int | float],
) -> None:
    """Affiche le résumé global du réseau (velo status)."""
    console.print(f"[bold]{network_name}[/bold] — données du {updated_at}\n")

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("[bold]Stations[/bold]", "")
    table.add_row("en service", f"{stats['in_service']} / {stats['total_stations']}")
    table.add_row("hors service", str(stats["out_of_service"]))
    table.add_row("vides", str(stats["empty"]))
    table.add_row("pleines", str(stats["full"]))
    table.add_row("", "")
    table.add_row("[bold]Vélos[/bold]", "")
    table.add_row("disponibles", str(stats["available_bikes"]))
    table.add_row("places libres", str(stats["available_docks"]))
    table.add_row("taux de remplissage", f"{stats['fill_rate']}%")

    console.print(table)


def display_stations_list(stations: list[Station]) -> None:
    """Affiche une liste de stations avec leur identifiant (velo station list/search)."""
    if not stations:
        console.print("[yellow]Aucune station trouvée.[/yellow]")
        return

    table = Table()
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Station")

    for station in stations:
        table.add_row(station.station_id, station.name)

    console.print(table)


def display_favorites(
    favorites_details: list[tuple[Station, StationStatus | None]],
) -> None:
    """Affiche l'état des stations favorites (velo favorites)."""
    if not favorites_details:
        console.print(
            "[yellow]Aucune station favorite enregistrée.[/yellow]\n"
            "Utilisez [bold]velo station search <nom>[/bold] pour trouver un identifiant, "
            "puis [bold]velo favorites add <id>[/bold]."
        )
        return

    table = Table()
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Station")
    table.add_column("Vélos", justify="right")
    table.add_column("Places", justify="right")
    table.add_column("État")

    for station, status in favorites_details:
        if status is None or is_out_of_service(status):
            table.add_row(station.station_id, station.name, "-", "-", "[red]hors service[/red]")
        else:
            etat = ""
            if is_empty(status):
                etat = "[yellow]vide[/yellow]"
            elif is_full(status):
                etat = "[blue]pleine[/blue]"
            table.add_row(
                station.station_id,
                station.name,
                str(status.bikes),
                str(status.docks),
                etat,
            )

    console.print(table)