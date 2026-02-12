"""Tests for configuration loading."""

from pathlib import Path
from smog.config import AirtableConfig, load_config


def test_load_config_from_secrets_yaml() -> None:
    """Test that configuration loads API key, base ID, and table name from secrets.yaml."""
    config = load_config()

    assert isinstance(config, AirtableConfig)
    assert config.api_key.startswith("pat")
    assert config.base_id.startswith("app")
    assert config.table_name == "Users"


def test_load_config_with_custom_path() -> None:
    """Test that configuration can load from a custom path."""
    secrets_path = Path(__file__).parent.parent / "secrets.yaml"
    config = load_config(secrets_path)

    assert isinstance(config, AirtableConfig)
    assert config.api_key.startswith("pat")
