---
trigger: always_on
---

# 🧠 Rules para Agente de IA --- Python (Best Practices 2026)

## 1. Princípios Fundamentais

- Priorizar:
  - **Legibilidade \> performance prematura**
  - **Simplicidade \> complexidade desnecessária**
- Seguir:
  - PEP 8 (style guide)
  - PEP 20 (Zen of Python)
- Código deve ser:
  - Determinístico
  - Testável
  - Idempotente (quando aplicável)

---

## 2. Tipagem e Estrutura

- Tipagem estática obrigatória
- Usar:
  - `typing`, `typing_extensions`
  - `TypedDict`, `Protocol`, `dataclass`, `pydantic`
- Validar com:
  - `mypy` ou `pyright`

```python
from typing import List

def sum_values(values: List[int]) -> int:
    return sum(values)
```

---

## 3. Estrutura de Projeto

    project/
    │── src/
    │   └── app/
    │       ├── __init__.py
    │       ├── main.py
    │       ├── services/
    │       ├── domain/
    │       └── infra/
    │
    │── tests/
    │── pyproject.toml
    │── README.md

- Separação:
  - `domain` → regras de negócio
  - `services` → orquestração
  - `infra` → IO, banco, APIs

---

## 4. Gerenciamento de Dependências

- Usar:
  - `uv` (preferido)
  - ou `Poetry`
- Evitar `requirements.txt` puro
- Lockfile obrigatório

---

## 5. Qualidade de Código

- Lint/format:
  - `ruff`
  - `black` (opcional)
- Hooks:
  - `pre-commit`

---

## 6. Testes

- Framework: `pytest`
- Cobertura mínima: **80%+**

```python
def test_sum_values():
    assert sum_values([1, 2, 3]) == 6
```

---

## 7. Tratamento de Erros

- Evitar `except Exception` genérico
- Criar exceções customizadas

```python
class PaymentError(Exception):
    pass
```

- Logar erros críticos

---

## 8. Logging

- Não usar `print`
- Usar `logging` ou `structlog`

---

## 9. Segurança

- Nunca hardcodar:
  - Senhas
  - Tokens
- Usar `.env` (`python-dotenv`)
- Validar e sanitizar inputs

---

## 10. Performance

- Otimizar apenas após medir
- Ferramentas:
  - `cProfile`
  - `timeit`
- Concorrência:
  - `asyncio` (I/O-bound)
  - multiprocessing (CPU-bound)

---

## 11. APIs

- Framework: `FastAPI`
- Usar:
  - Pydantic
  - OpenAPI automático

---

## 12. Banco de Dados

- ORM: `SQLAlchemy 2.x`
- Migrations: `Alembic`

---

## 13. Assincronismo

- Usar `async/await` quando necessário
- Não misturar sync/async incorretamente

---

## 14. Documentação

- Documentar funções públicas

```python
def create_user(name: str) -> str:
    """Create a new user and return its ID."""
```

---

## 15. CI/CD

- Pipeline mínimo:
  - lint
  - type check
  - tests
- Ex: GitHub Actions

---

## 16. Regras do Agente

O agente DEVE:

- Sempre usar tipagem
- Sempre incluir testes
- Evitar libs obsoletas
- Sugerir melhorias
- Validar edge cases
- Considerar escalabilidade

---

## 17. Anti-patterns Proibidos

- Código sem tipagem
- Funções \> 50 linhas
- Variáveis genéricas (`data`, `temp`)
- Lógica no controller
- Classes desnecessárias
- Falta de testes

---

## 18. Estilo de Código

- Funções curtas
- Nomes descritivos
- Early return
- Evitar nested ifs

---

## 19. Versão do Python

- Python **3.12+**
- Usar:
  - pattern matching (`match`)
  - melhorias modernas

---

## 20. Regra Final

> O agente deve agir como um engenheiro sênior, não apenas como um
> gerador de código.
