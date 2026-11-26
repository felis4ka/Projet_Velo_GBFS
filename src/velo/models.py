from dataclasses import dataclass
from datetime import datetime 

@dataclass
class Station :
    "Les infos fixes d'une station"

    station_id: str
    name : str
    capacity : int

@dataclass
class StationStatus : 
    "Etat en temps réel d'une station"

    station_id : str
    bikes: int
    docks: int
    is_installed : bool
    is_renting : bool 
    is_returning : bool
    last_reported : datetime