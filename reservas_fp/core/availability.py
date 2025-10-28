from typing import Iterable, Tuple
from .models import Estado, Hotel, Room, Reserva
from .dates import intervalo_sobrepoe




def reservas_do_quarto(reservas: Iterable[Reserva], room_id: str) -> Tuple[Reserva, ...]:
    return tuple(r for r in reservas if r.room_id == room_id)




def quarto_disponivel(estado: Estado, room: Room, checkin, checkout) -> bool:
    for r in reservas_do_quarto(estado.reservas, room.id):
        if intervalo_sobrepoe(r.checkin, r.checkout, checkin, checkout):
            return False
    return True




def quartos_disponiveis_no_hotel(
    estado: Estado,
    hotel: Hotel,
    checkin,
    checkout,
    capacidade_min: int = 1,
):
    return tuple(
        room
        for room in hotel.rooms
        if room.capacidade >= capacidade_min and quarto_disponivel(estado, room, checkin, checkout)
)


def buscar_hoteis_por_cidade(estado: Estado, cidade: str) -> Tuple[Hotel, ...]:
    return tuple(h for h in estado.hoteis if h.cidade.lower() == cidade.lower())