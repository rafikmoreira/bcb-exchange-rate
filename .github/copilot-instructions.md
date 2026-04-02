# Copilot Instructions — BCB Exchange Rate API

## Architecture

Clean Architecture with four layers — dependencies flow inward only:

1. **Domain** (`src/domain/`) — Pydantic entities (`CurrencyQuotation`, `CurrencyUsdRate`, `ConvertedAmount`, `LogEntry`), abstract ports (interfaces), and domain exceptions. No framework imports.
2. **Use Cases** (`src/use_cases/`) — `GetPtaxQuotationUseCase` orchestrates quotation lookup with cache-first strategy: check `QuotationRepository` → fallback to `QuotationProvider` (scraper) → persist results. Contains business-day logic (`get_closest_business_day`, `get_previous_business_day`).
3. **Infrastructure** (`src/infrastructure/`) — Concrete implementations: `PlaywrightBCBScraper` (downloads/parses PTAX CSVs from BCB website via Playwright), `SQLiteQuotationRepository`, `SQLiteLogRepository`. Both repos share a single SQLite DB at `data/db/quotations.db`.
4. **API** (`src/api/`) — FastAPI routes under `/api/v1`. Dependency injection wired in `src/api/dependencies.py`. Entry point: `main.py` → `uvicorn` running `src.api.main:app`.

**No business logic in routes** — routes only parse input, delegate to use cases, and map exceptions to HTTP status codes.

## Key Data Flow

API request → `routes.py` parses `reference_date` (YYYY-MM-DD, optional) → use case adjusts weekends to previous Friday → checks SQLite cache → if miss, Playwright scrapes BCB iframe, downloads CSV → parses semicolon-delimited CSV (`;`) with comma decimals (`5,2188`) → persists to SQLite → returns Pydantic models. CSV files are also cached on disk at `data/csvs/`.

## Developer Commands

```bash
uv sync                              # Install dependencies (lockfile obrigatório)
uv run playwright install chromium   # Required for scraping
uv run python main.py                # Start server on :8000
uv run pytest                        # Run all tests (auto async mode)
```

## Code Style

- **Python 3.14+** — use modern features (pattern matching, modern typing syntax).
- **Static typing is mandatory** — annotate all function signatures and return types.
- **All entities are Pydantic `BaseModel`** with `Field(...)` descriptions. Use abstract base classes (`ABC`) for ports.
- **Functions ≤ 50 lines** — break down larger logic. Prefer early returns over nested ifs.
- **Descriptive names** — avoid generic names like `data`, `temp`, `result`.
- **Lint/format**: use `ruff`. Run before committing.
- **No `print()`** — use `LogRepository` for persistence (see Logging below).
- **No hardcoded secrets** — use `.env` + `python-dotenv` if needed.

## Testing Conventions

- **Framework**: `pytest`. Target **80%+ coverage**.
- **Async tests**: Use `@pytest.mark.asyncio` — `asyncio_mode = "auto"` is set in `pyproject.toml`.
- **Port mocking**: Create concrete classes extending abstract ports (e.g., `MockQuotationProvider(QuotationProvider)`) or use `AsyncMock`/`MagicMock`.
- **API tests**: Use FastAPI's `TestClient` + `app.dependency_overrides[get_ptax_use_case]` to inject mocks. Always call `app.dependency_overrides.clear()` after each test.
- **Infrastructure tests**: Use `tmp_path` fixture for SQLite DB paths to avoid polluting `data/db/`.
- Parser logic (`_parse_all_currencies`) is tested directly without Playwright.
- **Always include tests** when adding or changing functionality. Validate edge cases.

## Conventions & Patterns

- **Language**: Codebase is in Portuguese (docstrings, error messages, API descriptions, log messages). Maintain this convention.
- **Date formats**: API accepts/returns `YYYY-MM-DD`; internal ports use `YYYY-MM-DD`; BCB website expects `DD/MM/YYYY`; CSV filenames use `DDMMYYYY`.
- **Error handling**: Domain exceptions (`QuotationNotFoundError`, `ScrapingError`) extend `DomainError`. Routes catch `DomainError` and map to HTTP 404. Validation errors return custom 422 format with `campo`/`erro` keys. Never use bare `except Exception`.
- **Logging**: Every use case method logs via `LogRepository` — `INFO` on success, `ERROR` on failure. Logs are persisted in SQLite, not stdout. Never use `print()`.
- **USD parity calculation**: `target_currency.buy_rate_brl / usd_currency.buy_rate_brl` — always derived by crossing BRL rates through USD.
- **Async/await**: Scraper and use case methods are `async`. Do not mix sync/async incorrectly — sync repos are called from async use cases without blocking issues because SQLite is local.
- **Document public functions** with docstrings in Portuguese.
