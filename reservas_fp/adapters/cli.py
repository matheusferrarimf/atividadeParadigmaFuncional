#Interface de Linha de Comando minimalista (somente orquestra o core).
from datetime import date
from core import (
    Estado,
    Hotel,
    Room,
    Reserva,
    buscar_hoteis_por_cidade,
    quartos_disponiveis_no_hotel,
    compose,
    tarifa_base,
    desconto_percentual,
    desconto_fim_de_semana,
    cotar,
    reservar,
    cancelar,
)
from .io_json import carregar_estado, salvar_estado


def seed_estado_demo() -> Estado:
    h1 = Hotel(
        id="H1",
        nome="Hotel Centro",
        cidade="Florianópolis",
        rooms=(
            Room(id="R1", hotel_id="H1", capacidade=2, preco_base=200.0),
            Room(id="R2", hotel_id="H1", capacidade=4, preco_base=320.0),
        ),
    )
    h2 = Hotel(
        id="H2",
        nome="Pousada Praia",
        cidade="Florianópolis",
        rooms=(
            Room(id="R3", hotel_id="H2", capacidade=3, preco_base=250.0),
        ),
    )
    return Estado(hoteis=(h1, h2), reservas=tuple())


def executar_demo(caminho_json: str = "estado.json") -> None:
    # Carrega (ou cria) estado
    estado = carregar_estado(caminho_json)
    if not estado.hoteis:
        estado = seed_estado_demo()
        salvar_estado(estado, caminho_json)

    # Consulta
    checkin, checkout = date(2025, 11, 7), date(2025, 11, 10)
    hoteis = buscar_hoteis_por_cidade(estado, "Florianópolis")
    rooms = quartos_disponiveis_no_hotel(estado, hoteis[0], checkin, checkout, capacidade_min=2)

    if not rooms:
        print("Nenhum quarto disponível.")
        return

    regra = compose(
        tarifa_base(rooms[0].preco_base),
        desconto_fim_de_semana(valor_por_noite=20.0),
        desconto_percentual(0.05),
    )

    preco = cotar(rooms[0], checkin, checkout, regra)
    print(f"Cotação para {rooms[0].id}: R$ {preco:.2f}")

    # Efetiva a reserva (gera novo estado)
    res = Reserva(id="RES1", room_id=rooms[0].id, checkin=checkin, checkout=checkout)
    estado2 = reservar(estado, res)
    salvar_estado(estado2, caminho_json)
    print("Reserva criada. Total de reservas:", len(estado2.reservas))

    # Cancela (demonstra não mutabilidade)
    estado3 = cancelar(estado2, res.id)
    salvar_estado(estado3, caminho_json)
    print("Reserva cancelada. Total de reservas:", len(estado3.reservas))