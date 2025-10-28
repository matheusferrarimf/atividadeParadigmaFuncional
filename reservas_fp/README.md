#Reservas FP (Programação Funcional em Python)

Demonstração de conceitos funcionais com o tema Turismo / Reservas de Hotel.

#Conceitos

*Núcleo 100% funcional em core/ (sem E/S; funções puras; dados imutáveis com dataclasses(frozen=True)).

*Regras de preço como funções combináveis (compose) em core/pricing.py.

*Disponibilidade com verificação de intervalos imutáveis em core/availability.py.

*Operações reservar/cancelar retornam novo Estado (não há mutação) em core/operations.py.

*E/S isolada nos adaptadores em adapters/ (io_json.py, cli.py).

*Como rodar*
No Windows PowerShell

1️ Criar o ambiente virtual

python -m venv .venv

2️ Ativar o ambiente

.venv\Scripts\Activate.ps1

*Se aparecer erro de “execução de scripts está desabilitada”, abra o PowerShell como Administrador e execute:*

Set-ExecutionPolicy RemoteSigned

Depois confirme com S e tente ativar novamente.

3️ Instalar dependências

pip install -U pytest

4️ Executar o programa

python main.py

Isso criará (ou atualizará) o arquivo estado.json, mostrando:

Cotação de reserva

Criação da reserva

Cancelamento da reserva (demonstrando imutabilidade)

*Executar os testes*

python -m pytest -q

Estrutura do projeto

reservas_fp/
  core/
    models.py
    dates.py
    availability.py
    pricing.py
    operations.py
  adapters/
    io_json.py
    cli.py
  tests/
    test_core.py
  main.py
  README.md

