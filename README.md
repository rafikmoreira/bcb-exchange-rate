# BCB Exchange Rate API

[![CI](https://github.com/rafikmoreira/bcb-exchange-rate/actions/workflows/ci.yml/badge.svg)](https://github.com/rafikmoreira/bcb-exchange-rate/actions/workflows/ci.yml)

Uma API construída com **FastAPI** seguindo os princípios da **Clean Architecture** para consultar, de forma automatizada, dados de cotação do **Banco Central do Brasil (BCB)** através da taxa PTAX. O projeto utiliza o **Playwright** para fazer o download automático dos arquivos CSV da cotação e calcula a equivalência das moedas atreladas ao Dólar Americano (USD).

## Principais Funcionalidades

- **Automação (Scraping):** Faz download da cotação PTAX diretamente da página web do BCB usando Playwright e persiste os dados em um banco SQLite local.
- **Cálculo de Paridade USD:** Calcula o lastro de moedas listadas cruzadas pelo Dólar com base na PTAX, considerando Dólar e as respectivas paridades.
- **Cache Local e Lógica de Dias Úteis:** Lida com datas de referência para cotação, ignorando finais de semana e priorizando o cache dos dados armazenados no banco SQLite para maior performance.
- **Persistência de Logs:** Cada requisição à API gera um log de nível `INFO` (sucesso) ou `ERROR` (falha de negócio), armazenado no mesmo banco SQLite.

## Tecnologias e Ferramentas

- Python 3.14+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Playwright](https://playwright.dev/python/)
- [uv](https://github.com/astral-sh/uv) (Gerenciador de pacotes rápido)
- [pytest](https://docs.pytest.org/) para testes automatizados

## Instalação

O projeto utiliza o `uv` como gerenciador de dependências.

1. Clone o repositório e acesse a pasta do projeto:

   ```bash
   git clone https://github.com/rafikmoreira/bcb-exchange-rate.git
   cd bcb-exchange-rate
   ```

2. Sincronize e instale as dependências usando `uv`:

   ```bash
   uv sync
   ```

3. Instale os navegadores do Playwright necessários para baixar as cotações do BCB:

   ```bash
   uv run playwright install chromium
   ```

## Como Executar

Inicie a aplicação localmente utilizando o `uv` via terminal. A API estará acessível por padrão em `http://0.0.0.0:8000`.

```bash
uv run python main.py
```

Você também pode acessar a documentação interativa gerada automaticamente pelo FastAPI via navegador:

- [Swagger UI: http://localhost:8000/docs](http://localhost:8000/docs)
- [ReDoc: http://localhost:8000/redoc](http://localhost:8000/redoc)

## Principais Endpoints da API

O parâmetro `reference_date` é opcional em todos os endpoints. Quando não informado, a data do dia útil anterior é utilizada.

> **Formato de datas:** tanto o parâmetro `reference_date` (entrada) quanto as datas retornadas nas respostas seguem o padrão ISO 8601 `YYYY-MM-DD` (ex: `2026-04-01`).

### 1. Listar todas as cotações

Retorna a lista de todas as moedas extraídas do PTAX, com suas taxas em BRL e as paridades.

```text
GET /api/v1/quotations?reference_date=YYYY-MM-DD
```

Exemplo de resposta:

```json
[
  {
    "currency": "EUR",
    "date": "2026-03-31",
    "buy_rate_brl": 6.01,
    "sell_rate_brl": 6.0117,
    "usd_parity_buy": 1.08,
    "usd_parity_sell": 1.09
  }
]
```

### 2. Equivalência de 1 unidade em USD

Retorna a cotação equivalente a 1 unidade da moeda desejada (ex: EUR, JPY) em Dólares (USD).

```text
GET /api/v1/quotations/{currency}?reference_date=YYYY-MM-DD
```

Exemplo de resposta:

```json
{
  "currency": "EUR",
  "date": "2026-03-31",
  "buy_rate_usd": 1.151606,
  "sell_rate_usd": 1.151799,
  "brl_buy": 6.01,
  "brl_sell": 6.0117
}
```

### 3. Converter um montante para USD

Calcula a equivalência total em Dólares (USD) para o montante informado.

```text
GET /api/v1/quotations/{currency}/convert?amount={valor}&reference_date=YYYY-MM-DD
```

Exemplo: `/api/v1/quotations/EUR/convert?amount=13000&reference_date=2026-03-31`

## Testes Automatizados

O projeto utiliza o framework `pytest` com o plugin assíncrono `pytest-asyncio`. Para executar os testes:

```bash
uv run pytest
```
