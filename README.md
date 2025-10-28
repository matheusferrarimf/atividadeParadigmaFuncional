# Reservas FP (Programação Funcional em Python)

Demonstração de conceitos funcionais com o tema **Turismo / Reservas de Hotel**.

## Conceitos

* Núcleo 100% funcional em `core/` (sem E/S; funções puras; dados imutáveis com `dataclasses(frozen=True)`).
* Regras de preço como **funções** combináveis (`compose`) em `core/pricing.py`.
* Disponibilidade com verificação de **intervalos** imutáveis em `core/availability.py`.
* Operações `reservar`/`cancelar` retornam **novo** `Estado` (não há mutação) em `core/operations.py`.
* E/S isolada nos **adaptadores** em `adapters/` (`io_json.py`, `cli.py`).

---

## 💻 Como rodar no Windows (PowerShell)

1️⃣ **Criar o ambiente virtual**

```powershell
python -m venv .venv
```

2️⃣ **Ativar o ambiente**

```powershell
.venv\Scripts\Activate.ps1
```

3️⃣ **Instalar dependências**

```powershell
pip install -U pytest
```

4️⃣ **Executar o programa**

```powershell
python main.py
```

Isso criará (ou atualizará) o arquivo `estado.json`, mostrando:

* Cotação de reserva
* Criação da reserva
* Cancelamento da reserva (demonstrando imutabilidade)

---

## 🧪 Executar os testes

```powershell
python -m pytest -q
```

> Dica: usar `python -m pytest` garante que o Python configure o caminho de importação corretamente no Windows, evitando erros como `ModuleNotFoundError: core`.

---

## 📂 Estrutura do projeto

```
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
```

---

## 🌐 Adaptador Flask (sem lógica de negócio)

### 🔧 Instalação extra

```bash
pip install Flask
```

### ▶️ Como rodar o Flask

**Use o Python do ambiente atual para garantir o `pip`/`flask` certos.**

Opção A (recomendada — módulo):

```powershell
# dentro da pasta do projeto, com .venv ATIVADO
python -m pip install Flask
python -m flask --app adapters.flask_app run --debug
```

Opção B (executando o arquivo diretamente):

```powershell
python adapters/flask_app.py
```

Opção B (variáveis do Flask):

```bash
$env:FLASK_APP="adapters/flask_app.py"   # PowerShell no Windows
flask run --debug
```

A aplicação vai rodar em `http://127.0.0.1:5000/`.

---

---

## 🌐 Fluxo do site (localhost)

1. **Página inicial (`/`)**

   * Exibe formulário de **busca de quartos** e **cancelamento** de reserva.
   * Inputs: cidade, check-in, check-out, capacidade.

2. **Busca (`POST /buscar`)**

   * Valida entradas e datas.
   * Usa `core.availability` para encontrar hotéis e quartos disponíveis.
   * Renderiza `resultados.html` com os quartos livres e botão de cotar.

3. **Cotação (`POST /cotar`)**

   * Monta o pipeline de preço com `tarifa_base`, `desconto_fim_de_semana` e cupom `PROMO10` (opcional).
   * Calcula o valor final via `core.operations.cotar`.
   * Mostra `cotacao.html` com o total e botão de confirmação.

4. **Reserva (`POST /reservar`)**

   * Cria objeto `Reserva` e chama `core.operations.reservar`.
   * Gera um novo `Estado` e grava em `estado.json`.
   * Exibe mensagem de sucesso e retorna à home.

5. **Cancelamento (`POST /cancelar`)**

   * Remove reserva por ID com `core.operations.cancelar`.
   * Demonstra imutabilidade (operação idempotente).
   * Atualiza `estado.json` e mostra mensagem.

Todo o ciclo acontece sem o core conhecer o Flask ou o arquivo JSON — o **Flask apenas orquestra** as chamadas.

---

### 🔍 Onde está a Programação Funcional aqui?

* **Core intocado**: toda a lógica de negócio permanece em `core/` com funções puras e dados imutáveis.
* **Flask só orquestra**: converte `request.form` → tipos do domínio (`date`, `int`), chama `core`, e renderiza.
* **Estado como valor**: após `reservar`/`cancelar`, o Flask recebe **novo** `Estado` e persiste via `io_json`.
* **Regras como funções**: pipeline com `compose(...)` cria cotações configuráveis sem `ifs` espalhados no handler.
