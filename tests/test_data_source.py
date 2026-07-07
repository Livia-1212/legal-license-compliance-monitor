import pytest

from src.db.data_source import get_data_source, load_application_data


def test_get_data_source_defaults_to_csv(monkeypatch):
    monkeypatch.delenv("DATA_SOURCE", raising=False)

    assert get_data_source() == "csv"


def test_get_data_source_reads_env_value(monkeypatch):
    monkeypatch.setenv("DATA_SOURCE", "postgres")

    assert get_data_source() == "postgres"


def test_load_application_data_rejects_invalid_source(monkeypatch):
    monkeypatch.setenv("DATA_SOURCE", "invalid")

    with pytest.raises(ValueError):
        load_application_data()
