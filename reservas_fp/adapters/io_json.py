#"Serialização/Deserialização do Estado em JSON (único lugar com E/S).
from __future__ import annotations
import json
from datetime import date
from typing import Any, Dict, Tuple
from pathlib import Path
from dataclasses import replace

from core.models import Estado, Hotel, Room, Reserva



def estado_to_dict(estado: Estado) -> Dict[str, Any]:
    return {
        "hoteis": [
            {
                "id": h.id,
                "nome": h.nome,
                "cidade": h.cidade,
                "rooms": [
                    {"id": r.id, "hotel_id": r.hotel_id, "capacidade": r.capacidade, "preco_base": r.preco_base}
                    for r in h.rooms
                ],
            }
            for h in estado.hoteis
        ],
        "reservas": [
            {
                "id": r.id,
                "room_id": r.room_id,
                "checkin": r.checkin.isoformat(),
                "checkout": r.checkout.isoformat(),
            }
            for r in estado.reservas
        ],
    }


def estado_from_dict(d: Dict[str, Any]) -> Estado:
    hoteis: Tuple[Hotel, ...] = tuple(
        Hotel(
            id=h["id"],
            nome=h["nome"],
            cidade=h["cidade"],
            rooms=tuple(
                Room(
                    id=r["id"], hotel_id=r["hotel_id"], capacidade=int(r["capacidade"]), preco_base=float(r["preco_base"])
                )
                for r in h.get("rooms", [])
            ),
        )
        for h in d.get("hoteis", [])
    )
    reservas: Tuple[Reserva, ...] = tuple(
        Reserva(
            id=r["id"],
            room_id=r["room_id"],
            checkin=_parse_date(r["checkin"]),
            checkout=_parse_date(r["checkout"]),
        )
        for r in d.get("reservas", [])
    )
    return Estado(hoteis=hoteis, reservas=reservas)


def _parse_date(s: str) -> date:
    return date.fromisoformat(s)


# ---------- E/S efetiva (side effects): leitura/gravação ----------

def salvar_estado(estado: Estado, caminho: str | Path) -> None:
    path = Path(caminho)
    data = estado_to_dict(estado)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def carregar_estado(caminho: str | Path) -> Estado:
    path = Path(caminho)
    if not path.exists():
        # estado vazio
        return Estado(hoteis=tuple(), reservas=tuple())
    raw = json.loads(path.read_text(encoding="utf-8"))
    return estado_from_dict(raw)