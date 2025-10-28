from dataclasses import dataclass
from datetime import date
from typing import Tuple

HotelId = str
RoomId = str
ReservaId = str

@dataclass(frozen=True)
class Hotel:
    id: HotelId
    nome: str
    cidade: str
    rooms: Tuple["Room", ...]
    
@dataclass(frozen=True)
class Room:
    id: RoomId
    hotel_id: HotelId
    capacidade: int
    preco_base: float 
    
@dataclass(frozen=True)
class Reserva:
    id: ReservaId
    room_id: RoomId
    checkin: date
    checkout: date 
    
@dataclass(frozen=True)
class Estado:
    hoteis: Tuple[Hotel, ...]
    reservas: Tuple[Reserva, ...]