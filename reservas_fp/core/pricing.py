from functools import reduce
from typing import Callable, Dict
from datetime import date, timedelta
from .dates import noites

PrecoRule = Callable[[float, Dict], float]


def compose(*funcs: PrecoRule) -> PrecoRule:
    """Cria um pipeline: compose(f, g, h)(x) = h(g(f(x))).
    Aqui usamos reduce para aplicar em sequência sobre o valor acumulado.
    """
    def inner(preco: float, ctx: Dict) -> float:
        return reduce(lambda acc, f: f(acc, ctx), funcs, preco)
    return inner


def tarifa_base(preco_base: float) -> PrecoRule:
    def rule(_preco: float, ctx: Dict) -> float:
        return preco_base * noites(ctx["checkin"], ctx["checkout"])
    return rule


def desconto_percentual(pct: float) -> PrecoRule:
    def rule(preco: float, _ctx: Dict) -> float:
        return preco * (1 - pct)
    return rule


def acrescimo_percentual(pct: float) -> PrecoRule:
    def rule(preco: float, _ctx: Dict) -> float:
        return preco * (1 + pct)
    return rule


def desconto_fim_de_semana(valor_por_noite: float) -> PrecoRule:
    def rule(preco: float, ctx: Dict) -> float:
        d: date = ctx["checkin"]
        total = preco
        while d < ctx["checkout"]:
            if d.weekday() >= 5:  # 5=sábado, 6=domingo
                total -= valor_por_noite
            d += timedelta(days=1)
        return max(total, 0.0)
    return rule