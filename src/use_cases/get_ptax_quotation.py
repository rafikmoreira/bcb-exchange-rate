from datetime import datetime, timedelta

from src.domain.entities import CurrencyQuotation, ConvertedAmount, LogEntry, CurrencyUsdRate
from src.domain.exceptions import DomainError, QuotationNotFoundError
from src.domain.ports import QuotationProvider, QuotationRepository, LogRepository

def get_closest_business_day(target_date: datetime) -> datetime:
    """Se a data for sábado ou domingo, retrocede para o dia útil mais próximo (sexta-feira)."""
    target = target_date
    while target.weekday() >= 5:
        target -= timedelta(days=1)
    return target

def get_previous_business_day(from_date: datetime) -> datetime:
    """Retorna a data correspondente ao dia útil anterior (considerando apenas sab/dom como não úteis)."""
    return get_closest_business_day(from_date - timedelta(days=1))

class GetPtaxQuotationUseCase:
    """Caso de uso principal para consulta de cotações PTAX do BCB."""

    def __init__(
        self,
        provider: QuotationProvider,
        repository: QuotationRepository | None = None,
        log_repository: LogRepository | None = None,
    ) -> None:
        self.provider = provider
        self.repository = repository
        self.log_repository = log_repository

    def _log(self, level: str, message: str, context: str) -> None:
        """Persiste um registro de log via LogRepository, se disponível."""
        if self.log_repository:
            self.log_repository.save_log(LogEntry(level=level, message=message, context=context))

    async def list_all_quotations(self, reference_date: datetime | None = None) -> list[CurrencyQuotation]:
        """
        Lista todas as moedas e suas cotações para uma data específica.
        Se a data não for fornecida, utiliza o último dia útil disponível.
        Recupera do repositório local caso exista, senão busca do BCB e salva no repositório.
        """
        if reference_date is None:
            target_date = get_previous_business_day(datetime.now())
        else:
            target_date = get_closest_business_day(reference_date)
            
        formatted_date = target_date.strftime("%Y-%m-%d")
        
        if self.repository:
            saved_quotations = self.repository.get_quotations_by_date(formatted_date)
            if saved_quotations:
                return saved_quotations

        try:
            quotations = await self.provider.get_all_quotations_for_date(formatted_date)
        except DomainError as e:
            self._log("ERROR", str(e), "list_all_quotations")
            raise
            
        if self.repository:
            self.repository.save_quotations(formatted_date, quotations)

        self._log(
            "INFO",
            f"Cotações consultadas com sucesso para {formatted_date}. Total: {len(quotations)} moedas.",
            "list_all_quotations",
        )
            
        return quotations

    async def _resolve_currency_usd_rates(
        self, currency_code: str, reference_date: datetime | None, context: str,
    ) -> tuple[CurrencyQuotation, float, float]:
        """
        Busca cotações e calcula as taxas de conversão USD para a moeda informada.
        :return: Tupla com (cotação da moeda alvo, taxa de compra em USD, taxa de venda em USD).
        """
        all_quotations = await self.list_all_quotations(reference_date)

        target_quotation = next(
            (q for q in all_quotations if q.currency == currency_code.upper()), None,
        )
        usd_quotation = next(
            (q for q in all_quotations if q.currency == "USD"), None,
        )

        if not target_quotation or not usd_quotation:
            error_msg = f"Não foi possível encontrar as cotações para {currency_code} ou USD."
            self._log("ERROR", error_msg, context)
            raise QuotationNotFoundError(error_msg)

        rate_buy = target_quotation.buy_rate_brl / usd_quotation.buy_rate_brl
        rate_sell = target_quotation.sell_rate_brl / usd_quotation.sell_rate_brl

        return target_quotation, rate_buy, rate_sell

    async def get_currency_in_usd(
        self, currency_code: str, reference_date: datetime | None = None,
    ) -> CurrencyUsdRate:
        """Retorna a cotação de 1 unidade da moeda informada equivalendo em Dólares (USD)."""
        target_quotation, rate_buy, rate_sell = await self._resolve_currency_usd_rates(
            currency_code, reference_date, "get_currency_in_usd",
        )

        self._log(
            "INFO",
            f"Cotação de {currency_code.upper()} em USD consultada para {target_quotation.date}.",
            "get_currency_in_usd",
        )

        return CurrencyUsdRate(
            currency=currency_code.upper(),
            date=target_quotation.date,
            buy_rate_usd=round(rate_buy, 6),
            sell_rate_usd=round(rate_sell, 6),
            brl_buy=target_quotation.buy_rate_brl,
            brl_sell=target_quotation.sell_rate_brl,
        )

    async def convert_amount_in_usd(
        self, currency_code: str, amount: float, reference_date: datetime | None = None,
    ) -> ConvertedAmount:
        """Calcula o total equivalente em dólares para um montante da moeda escolhida."""
        target_quotation, rate_buy, rate_sell = await self._resolve_currency_usd_rates(
            currency_code, reference_date, "convert_amount_in_usd",
        )

        total_usd_buy = amount * rate_buy
        total_usd_sell = amount * rate_sell

        self._log(
            "INFO",
            f"Conversão de {amount} {currency_code.upper()} para USD realizada para {target_quotation.date}.",
            "convert_amount_in_usd",
        )

        return ConvertedAmount(
            currency=currency_code.upper(),
            amount=amount,
            usd_value_buy=round(total_usd_buy, 4),
            usd_value_sell=round(total_usd_sell, 4),
            reference_date=target_quotation.date,
            rate_used_buy=round(rate_buy, 6),
            rate_used_sell=round(rate_sell, 6),
        )
