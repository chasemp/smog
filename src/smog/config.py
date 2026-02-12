"""Configuration loading for Airtable client."""

from pathlib import Path
from typing import Optional

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
