"""Airtable employee lookup client ."""

from smog.client import AirtableClient
from smog.config import AirtableConfig, load_config
from smog.models import EmployeeRecord, EmployeeLookupResult

__all__ = [
    "AirtableClient",
    "AirtableConfig",
    "load_config",
    "EmployeeRecord",
    "EmployeeLookupResult",
]
