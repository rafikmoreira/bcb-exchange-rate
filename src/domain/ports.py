from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities import CurrencyQuotation, LogEntry


class QuotationProvider(ABC):
    """
    Interface (Port) que define o contrato para buscar a cotação de todas as moedas.
    """

    @abstractmethod
    async def get_all_quotations_for_date(
        self, target_date: str
    ) -> List[CurrencyQuotation]:
        """
        Busca a cotação de todas as moedas para uma data específica.
        :param target_date: Data alvo no formato DD/MM/YYYY.
        :return: Lista de objetos CurrencyQuotation do dia contendo paridades USD.
        """
        pass


class QuotationRepository(ABC):
    """
    Interface (Port) que define o contrato para persistência das cotações (repositório).
    """

    @abstractmethod
    def save_quotations(
        self, target_date: str, quotations: List[CurrencyQuotation]
    ) -> None:
        """
        Salva uma lista de cotações para uma dada data.
        :param target_date: Data alvo no formato DD/MM/YYYY.
        :param quotations: Lista de objetos CurrencyQuotation do dia.
        """
        pass

    @abstractmethod
    def get_quotations_by_date(self, target_date: str) -> List[CurrencyQuotation]:
        """
        Busca a cotação de todas as moedas salvas para uma data específica.
        :param target_date: Data alvo no formato DD/MM/YYYY.
        :return: Lista de objetos CurrencyQuotation do dia contendo paridades USD, ou lista vazia se não  encontrado.
        """
        pass


class LogRepository(ABC):
    """
    Interface (Port) que define o contrato para persistência de logs (repositório).
    """

    @abstractmethod
    def save_log(self, entry: LogEntry) -> None:
        """
        Persiste um registro de log.
        :param entry: Objeto LogEntry com nível, mensagem e contexto.
        """
        pass

    @abstractmethod
    def get_logs(self, level: Optional[str] = None, limit: int = 100) -> List[LogEntry]:
        """
        Busca os registros de log mais recentes, com filtragem opcional por nível.
        :param level: Nível do log para filtrar (INFO, WARNING, ERROR). None retorna todos.
        :param limit: Quantidade máxima de registros retornados.
        :return: Lista de objetos LogEntry.
        """
        pass
