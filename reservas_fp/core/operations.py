from dataclasses import replace
from .models import Estado, Reserva, Room
from .availability import quarto_disponivel
from .pricing import PrecoRule


class ReservaInvalida(Exception):
    ...


class QuartoIndisponivel(Exception):
    ...


def cotar(room: Room, checkin, checkout, regra_preco: PrecoRule, contexto_extra: dict | None = None) -> float:
    ctx = {"checkin": checkin, "checkout": checkout, "room": room}
    if contexto_extra:
        ctx.update(contexto_extra)
    return regra_preco(0.0, ctx)


def reservar(estado: Estado, reserva: Reserva) -> Estado:
    room = _buscar_room(estado, reserva.room_id)
    if not room:
        raise ReservaInvalida("Quarto inexistente")
    if not quarto_disponivel(estado, room, reserva.checkin, reserva.checkout):
        raise QuartoIndisponivel("Quarto já reservado no período")
    return replace(estado, reservas=estado.reservas + (reserva,))


def cancelar(estado: Estado, reserva_id: str) -> Estado:
    novas = tuple(r for r in estado.reservas if r.id != reserva_id)
    return replace(estado, reservas=novas)


def _buscar_room(estado: Estado, room_id: str) -> Room | None:
    for h in estado.hoteis:
        for r in h.rooms:
            if r.id == room_id:
                return r
    return None