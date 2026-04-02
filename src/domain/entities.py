from pydantic import BaseModel, Field


class CurrencyQuotation(BaseModel):
    """Cotação de uma moeda extraída do PTAX com taxas em BRL e paridades USD."""

    currency: str = Field(..., description="Sigla da moeda, ex: USD, EUR, GBP")
    date: str = Field(..., description="Data da cotação consultada no formato YYYY-MM-DD")
    buy_rate_brl: float = Field(..., description="Cotação de compra da moeda em Reais")
    sell_rate_brl: float = Field(..., description="Cotação de venda da moeda em Reais")
    usd_parity_buy: float = Field(..., description="Paridade (quantidade de USD para compor 1 unidade, ou vice-versa, dependendo do tipo da moeda) ou conversão direta para dólar de compra")
    usd_parity_sell: float = Field(..., description="Paridade convertida da moeda para venda em Dólar")
    
class CurrencyUsdRate(BaseModel):
    """Taxa de câmbio de uma moeda equivalente em Dólares (USD)."""

    currency: str = Field(..., description="Sigla da moeda, ex: EUR, GBP")
    date: str = Field(..., description="Data de referência da cotação no formato YYYY-MM-DD")
    buy_rate_usd: float = Field(..., description="Taxa de compra equivalente em Dólares")
    sell_rate_usd: float = Field(..., description="Taxa de venda equivalente em Dólares")
    brl_buy: float = Field(..., description="Cotação de compra original em Reais")
    brl_sell: float = Field(..., description="Cotação de venda original em Reais")

class ConvertedAmount(BaseModel):
    """Resultado da conversão de um montante de moeda para Dólares (USD)."""

    currency: str = Field(..., description="Sigla da moeda convertida")
    amount: float = Field(..., description="Quantidade original requisitada")
    usd_value_buy: float = Field(..., description="Total em Dólares baseado na taxa de compra")
    usd_value_sell: float = Field(..., description="Total em Dólares baseado na taxa de venda")
    reference_date: str = Field(..., description="Data de referência da cotação no formato YYYY-MM-DD")
    rate_used_buy: float = Field(..., description="Taxa de compra utilizada na conversão")
    rate_used_sell: float = Field(..., description="Taxa de venda utilizada na conversão")


class LogEntry(BaseModel):
    """Registro de log persistido no banco de dados."""

    level: str = Field(..., description="Nível do log: INFO, WARNING, ERROR")
    message: str = Field(..., description="Mensagem do log")
    context: str | None = Field(None, description="Contexto ou módulo que gerou o log")
    created_at: str | None = Field(None, description="Timestamp do registro no formato ISO 8601")
