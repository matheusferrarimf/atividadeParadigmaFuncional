from datetime import date
def intervalo_sobrepoe(a_ini: date, a_fim: date, b_ini: date, b_fim: date) -> bool:
   #Retorna True se [a_ini, a_fim) sobrepõe [b_ini, b_fim)
    return a_ini < b_fim and b_ini < a_fim

def noites(checkin: date, checkout: date) -> int:
    return (checkout - checkin).days