import pytest
import os
import tempfile
from src.domain.entities import LogEntry
from src.infrastructure.sqlite_log_repository import SQLiteLogRepository


@pytest.fixture
def log_repo(tmp_path):
    db_path = str(tmp_path / "db" / "test_logs.db")
    return SQLiteLogRepository(db_path=db_path)


class TestSQLiteLogRepository:
    def test_save_and_retrieve_log(self, log_repo):
        entry = LogEntry(level="INFO", message="Teste de log", context="test_module")
        log_repo.save_log(entry)

        logs = log_repo.get_logs()
        assert len(logs) == 1
        assert logs[0].level == "INFO"
        assert logs[0].message == "Teste de log"
        assert logs[0].context == "test_module"

    def test_created_at_is_set_automatically(self, log_repo):
        entry = LogEntry(level="INFO", message="Sem timestamp")
        log_repo.save_log(entry)

        logs = log_repo.get_logs()
        assert logs[0].created_at is not None

    def test_filter_by_level(self, log_repo):
        log_repo.save_log(LogEntry(level="INFO", message="Info log"))
        log_repo.save_log(LogEntry(level="ERROR", message="Error log"))
        log_repo.save_log(LogEntry(level="WARNING", message="Warning log"))

        errors = log_repo.get_logs(level="ERROR")
        assert len(errors) == 1
        assert errors[0].level == "ERROR"

    def test_filter_by_level_case_insensitive(self, log_repo):
        log_repo.save_log(LogEntry(level="INFO", message="Info log"))
        log_repo.save_log(LogEntry(level="ERROR", message="Error log"))

        infos = log_repo.get_logs(level="info")
        assert len(infos) == 1
        assert infos[0].level == "INFO"

    def test_limit_results(self, log_repo):
        for i in range(10):
            log_repo.save_log(LogEntry(level="INFO", message=f"Log {i}"))

        logs = log_repo.get_logs(limit=3)
        assert len(logs) == 3

    def test_returns_most_recent_first(self, log_repo):
        log_repo.save_log(LogEntry(level="INFO", message="Primeiro"))
        log_repo.save_log(LogEntry(level="INFO", message="Segundo"))

        logs = log_repo.get_logs()
        assert logs[0].message == "Segundo"

    def test_get_logs_returns_empty_when_no_records(self, log_repo):
        logs = log_repo.get_logs()
        assert logs == []

    def test_context_can_be_none(self, log_repo):
        entry = LogEntry(level="WARNING", message="Sem contexto")
        log_repo.save_log(entry)

        logs = log_repo.get_logs()
        assert logs[0].context is None
