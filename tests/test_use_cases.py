import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.domain.entities import CurrencyQuotation
from src.domain.ports import QuotationProvider
from src.use_cases.get_ptax_quotation import GetPtaxQuotationUseCase, get_previous_business_day, get_closest_business_day

class MockQuotationProvider(QuotationProvider):
    async def get_all_quotations_for_date(self, target_date: str) -> list[CurrencyQuotation]:
        return [
            CurrencyQuotation(
                currency="USD",
                date=target_date,
                buy_rate_brl=5.00,
                sell_rate_brl=5.00,
                usd_parity_buy=1.0,
                usd_parity_sell=1.0
            ),
            CurrencyQuotation(
                currency="EUR",
                date=target_date,
                buy_rate_brl=5.50,
                sell_rate_brl=5.50,
                usd_parity_buy=1.1,
                usd_parity_sell=1.1
            )
        ]

@pytest.mark.asyncio
async def test_get_currency_in_usd_use_case():
    provider = MockQuotationProvider()
    use_case = GetPtaxQuotationUseCase(provider)
    
    result = await use_case.get_currency_in_usd("EUR", reference_date=datetime(2026, 10, 2))
    
    assert result.currency == "EUR"
    assert result.buy_rate_usd == 1.10
    assert result.sell_rate_usd == 1.10

@pytest.mark.asyncio
async def test_convert_amount_in_usd_use_case():
    provider = MockQuotationProvider()
    use_case = GetPtaxQuotationUseCase(provider)
    
    fake_date = datetime(2026, 10, 2)
    result = await use_case.convert_amount_in_usd("EUR", 13000, reference_date=fake_date)
    
    assert result.currency == "EUR"
    assert result.amount == 13000
    assert result.usd_value_buy == 14300.0
    assert result.usd_value_sell == 14300.0

def test_get_previous_business_day_monday():
    monday = datetime(2026, 10, 5)
    previous = get_previous_business_day(monday)
    assert previous.strftime("%Y-%m-%d") == "2026-10-02"

def test_get_closest_business_day_weekend():
    # 2026-10-04 = Sunday
    sunday = datetime(2026, 10, 4)
    closest = get_closest_business_day(sunday)
    assert closest.strftime("%Y-%m-%d") == "2026-10-02"
    
    # 2026-10-03 = Saturday
    saturday = datetime(2026, 10, 3)
    closest = get_closest_business_day(saturday)
    assert closest.strftime("%Y-%m-%d") == "2026-10-02"

def test_get_closest_business_day_weekday():
    # 2026-10-01 = Thursday
    thursday = datetime(2026, 10, 1)
    closest = get_closest_business_day(thursday)
    assert closest.strftime("%Y-%m-%d") == "2026-10-01"

@pytest.mark.asyncio
async def test_list_all_quotations_uses_fallback_on_weekend():
    provider = MockQuotationProvider()
    provider.get_all_quotations_for_date = AsyncMock(return_value=[])
    
    use_case = GetPtaxQuotationUseCase(provider)
    
    # 2026-10-03 is Saturday
    saturday = datetime(2026, 10, 3)
    
    try:
        await use_case.list_all_quotations(reference_date=saturday)
    except Exception:
        pass # mock list_all_quotations might raise DomainError due to empty returns from Provider, that's fine
        
    # As assert_called_once_with checks the actual arguments passed to get_all_quotations_for_date
    # Since 2026-10-03 is a Saturday, it should fallback and fetch the previous Friday: 2026-10-02
    provider.get_all_quotations_for_date.assert_called_once_with("2026-10-02")
