# Reservas FP (Programação Funcional em Python)

Demonstração de conceitos funcionais com o tema **Turismo / Reservas de Hotel**.
# Alunos: Matheus Ferrari dos Santos && Sofya BBS de Andrade

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

## Exemplo de Fluxo

1) Cotar e reservar (com cupom)

Preencha na home

Cidade: Florianópolis

Check-in: 2025-11-07 (sex)

Check-out: 2025-11-10 (seg)

Capacidade mínima: 2 → Buscar

Na lista, no quarto R1 (base R$ 200/noite), clique Cotar e digite o cupom PROMO10, depois Cotar.

Esperado (em Cotação):

Noites: 3 → 3 × 200 = R$ 600,00

Desconto fim de semana: – R$ 40,00 (sáb + dom) → R$ 560,00

Cupom 10%: 560 × 0,9 → R$ 504,00 (total)

Clique Confirmar reserva.

De volta à home, aparece flash: “Reserva criada com sucesso!”

O ID gerado segue o padrão: RES-R1-2025-11-07.

Dica: sem cupom, o total seria R$ 560,00.

2) Ver indisponibilidade por sobreposição

Com a reserva do R1 feita para 07–10/11:

Faça nova busca com os mesmos dados (Florianópolis, 07–10/11, capacidade 2).

O R1 deve sumir dos resultados (está reservado). Se o hotel tiver outro quarto (ex.: R2), ele ainda aparece.

Para ver o erro de conflito de datas (mensagem de flash):

Tente cotar novamente o mesmo quarto R1 para 07–10/11 e Confirmar.

O back chama reservar(...) do core, detecta sobreposição e mostra flash: “Quarto já reservado no período”.

3) Reservar outro quarto com capacidade maior

Busca:

Cidade: Florianópolis

Check-in: 2025-11-07

Check-out: 2025-11-10

Capacidade mínima: 4 → Buscar

Agora deve aparecer R2 (base R$ 320/noite).

Cotar (sem cupom): 3 × 320 = R$ 960,00 → fim de semana – R$ 40,00 = R$ 920,00

Com PROMO10: 920 × 0,9 = R$ 828,00

Confirmar reserva para ver funcionar com outra capacidade.

4) Cancelar uma reserva (idempotência)

Na home, em Cancelar reserva, use o ID exibido quando você reservou.

Ex.: RES-R1-2025-11-07 → Cancelar → flash: “Reserva cancelada (idempotente).”

Clicar Cancelar de novo com o mesmo ID não causa erro e mantém o estado igual (propriedade de idempotência do cancelar).
