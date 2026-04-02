class DomainError(Exception):
    """Exceção base para todos os erros de domínio."""


class QuotationNotFoundError(DomainError):
    """Lançada quando os dados de cotação não estão disponíveis para os parâmetros informados."""


class ScrapingError(DomainError):
    """Lançada quando o scraper falha ao recuperar dados da fonte externa."""
