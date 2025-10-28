from datetime import date
from core.dates import intervalo_sobrepoe, noites
from core.models import Estado, Hotel, Room, Reserva
from core.availability import quarto_disponivel
from core.operations import reservar, cancelar, QuartoIndisponivel
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



def test_intervalo():
    assert intervalo_sobrepoe(date(2025,1,1), date(2025,1,5), date(2025,1,4), date(2025,1,10))
    assert not intervalo_sobrepoe(date(2025,1,1), date(2025,1,5), date(2025,1,5), date(2025,1,7))


def test_noites():
    assert noites(date(2025,1,1), date(2025,1,4)) == 3


def test_reserva_sem_sobreposicao():
    h = Hotel(id="H", nome="H", cidade="X", rooms=(Room(id="R", hotel_id="H", capacidade=2, preco_base=100.0),))
    e = Estado(hoteis=(h,), reservas=tuple())
    r = Reserva(id="RES", room_id="R", checkin=date(2025,1,1), checkout=date(2025,1,3))
    e2 = reservar(e, r)
    assert len(e.reservas) == 0
    assert len(e2.reservas) == 1


def test_reserva_com_sobreposicao():
    h = Hotel(id="H", nome="H", cidade="X", rooms=(Room(id="R", hotel_id="H", capacidade=2, preco_base=100.0),))
    r1 = Reserva(id="RES1", room_id="R", checkin=date(2025,1,1), checkout=date(2025,1,3))
    e = Estado(hoteis=(h,), reservas=(r1,))
    r2 = Reserva(id="RES2", room_id="R", checkin=date(2025,1,2), checkout=date(2025,1,4))
    try:
        _ = reservar(e, r2)
        assert False, "Deveria ter lançado QuartoIndisponivel"
    except QuartoIndisponivel:
        assert True


def test_cancelar_idempotente():
    h = Hotel(id="H", nome="H", cidade="X", rooms=(Room(id="R", hotel_id="H", capacidade=2, preco_base=100.0),))
    r = Reserva(id="RES", room_id="R", checkin=date(2025,1,1), checkout=date(2025,1,3))
    e = Estado(hoteis=(h,), reservas=(r,))
    e2 = cancelar(e, "RES")
    e3 = cancelar(e2, "RES")
    assert len(e2.reservas) == 0
    assert e2 == e3