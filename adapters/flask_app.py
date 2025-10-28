from __future__ import annotations
from datetime import date
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

from core import (
    Estado, Hotel, Room, Reserva,
    buscar_hoteis_por_cidade, quartos_disponiveis_no_hotel,
    compose, tarifa_base, desconto_percentual, desconto_fim_de_semana,
    cotar, reservar, cancelar,
)
from adapters.io_json import carregar_estado, salvar_estado

# ===== Configuração =====
app = Flask(__name__, template_folder="../templates")
app.secret_key = "teste demo"  # apenas  demo
ESTADO_PATH = Path("estado.json")


def _carregar_estado() -> Estado:
    return carregar_estado(ESTADO_PATH)


def _salvar_estado(estado: Estado) -> None:
    salvar_estado(estado, ESTADO_PATH)


# ===== Rotas =====
@app.get("/")
def home():
    return render_template("home.html")


@app.post("/buscar")
def buscar():
    cidade = request.form.get("cidade", "").strip()
    checkin = request.form.get("checkin")
    checkout = request.form.get("checkout")
    capacidade = int(request.form.get("capacidade") or 1)

    if not (cidade and checkin and checkout):
        flash("Preencha cidade, check-in e check-out.")
        return redirect(url_for("home"))

    ci = date.fromisoformat(checkin)
    co = date.fromisoformat(checkout)
    if ci >= co:
        flash("Check-out deve ser depois do check-in.")
        return redirect(url_for("home"))

    estado = _carregar_estado()
    hoteis = buscar_hoteis_por_cidade(estado, cidade)

    resultados = []
    for h in hoteis:
        rooms = quartos_disponiveis_no_hotel(estado, h, ci, co, capacidade)
        if rooms:
            resultados.append((h, rooms))

    return render_template("resultados.html", cidade=cidade, checkin=ci, checkout=co, resultados=resultados)


@app.post("/cotar")
def cotar_view():
    room_id = request.form.get("room_id")
    checkin = date.fromisoformat(request.form.get("checkin"))
    checkout = date.fromisoformat(request.form.get("checkout"))
    cupom = (request.form.get("cupom") or "").strip().upper()

    estado = _carregar_estado()

    # Localiza o quarto escolhido 
    quarto = None
    for h in estado.hoteis:
        for r in h.rooms:
            if r.id == room_id:
                quarto = r
                break
    if not quarto:
        flash("Quarto não encontrado.")
        return redirect(url_for("home"))

    # Monta o pipeline de preço 
    regras = [
        tarifa_base(quarto.preco_base),
        desconto_fim_de_semana(20.0),
    ]

    # Cupom simples (ex.: PROMO10 ⇒ 10% off)
    if cupom == "PROMO10":
        regras.append(desconto_percentual(0.10))

    pipeline = compose(*regras)
    preco = cotar(quarto, checkin, checkout, pipeline)

    return render_template("cotacao.html", quarto=quarto, checkin=checkin, checkout=checkout, preco=preco, cupom=cupom)


@app.post("/reservar")
def reservar_view():
    room_id = request.form.get("room_id")
    checkin = date.fromisoformat(request.form.get("checkin"))
    checkout = date.fromisoformat(request.form.get("checkout"))

    estado = _carregar_estado()
    nova = Reserva(id=f"RES-{room_id}-{checkin.isoformat()}", room_id=room_id, checkin=checkin, checkout=checkout)

    try:
        estado2 = reservar(estado, nova)
        _salvar_estado(estado2)
        flash("Reserva criada com sucesso!")
    except Exception as e:
        flash(str(e))

    return redirect(url_for("home"))


@app.post("/cancelar")
def cancelar_view():
    reserva_id = request.form.get("reserva_id")
    estado = _carregar_estado()
    estado2 = cancelar(estado, reserva_id)
    _salvar_estado(estado2)
    flash("Reserva cancelada (idempotente).")
    return redirect(url_for("home"))


if __name__ == "__main__":
    
    app.run(debug=True)