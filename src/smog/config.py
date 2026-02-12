"""Configuration loading for Airtable client."""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field


class AirtableConfig(BaseModel):
    """Configuration for Airtable API access."""

    api_key: str = Field(..., description="Airtable API key")
    base_id: str = Field(..., description="Airtable base ID")
    table_name: str = Field(..., description="Name of the users table")


def load_config(secrets_path: Optional[Path] = None) -> AirtableConfig:
    """
    Load Airtable configuration from secrets.yaml.

    Args:
        secrets_path: Path to secrets.yaml file. If None, uses default location.

    Returns:
        AirtableConfig instance with loaded configuration.

    Raises:
        FileNotFoundError: If secrets file doesn't exist.
        KeyError: If required configuration keys are missing.
    """
    if secrets_path is None:
        secrets_path = Path(__file__).parent.parent.parent / "secrets.yaml"

    with open(secrets_path) as f:
        secrets = yaml.safe_load(f)

    airtable_config = secrets["airtable"]

    return AirtableConfig(
        api_key=airtable_config["api_key"],
        base_id=airtable_config["base_id"],
        table_name=airtable_config["table_name"],
    )


def load_app_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load application configuration from config.yaml.

    Args:
        config_path: Path to config.yaml file. If None, uses default location.

    Returns:
        Dictionary with application configuration.
        Returns empty dict with default values if config file doesn't exist.
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config.yaml"

    # Return defaults if config file doesn't exist
    if not config_path.exists():
        return {"default_email_domain": ""}

    with open(config_path) as f:
        config = yaml.safe_load(f) or {}

    return {
        "default_email_domain": config.get("default_email_domain", ""),
    }
