from src.infrastructure.bcb_scraper import PlaywrightBCBScraper
from src.infrastructure.sqlite_repository import SQLiteQuotationRepository
from src.infrastructure.sqlite_log_repository import SQLiteLogRepository
from src.use_cases.get_ptax_quotation import GetPtaxQuotationUseCase

_log_repo = SQLiteLogRepository()


def get_ptax_use_case() -> GetPtaxQuotationUseCase:
    provider = PlaywrightBCBScraper()
    repository = SQLiteQuotationRepository()
    return GetPtaxQuotationUseCase(
        provider=provider,
        repository=repository,
        log_repository=_log_repo,
    )
