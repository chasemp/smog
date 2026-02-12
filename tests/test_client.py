"""Tests for Airtable client."""

from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock

import pytest

from smog.client import AirtableClient
from smog.config import AirtableConfig
from smog.models import EmployeeRecord, EmployeeLookupResult


@pytest.fixture
def mock_config() -> AirtableConfig:
    """Create a mock configuration for testing."""
    return AirtableConfig(
        api_key="test_api_key",
        base_id="appTestBase",
        table_name="Users",
    )


@pytest.fixture
def mock_table() -> Mock:
    """Create a mock Airtable table."""
    return MagicMock()


def test_find_by_email_returns_employee_when_found(
    mock_config: AirtableConfig,
    mock_table: Mock,
) -> None:
    """Test that find_by_email returns EmployeeRecord when email is found."""
    mock_table.all.return_value = [
        {
            "id": "rec123",
            "fields": {
                "Email": "john.doe@example.com",
                "Manager Email": "jane.smith@example.com",
                "Employee Status": "FTE",
            },
        }
    ]

    client = AirtableClient(mock_config)
    client._table = mock_table

    result = client.find_by_email("john.doe@example.com")

    assert result is not None
    assert isinstance(result, EmployeeRecord)
    assert result.email == "john.doe@example.com"
    assert result.manager_email == "jane.smith@example.com"
    assert result.employment_status == "FTE"


def test_find_by_email_returns_employee_with_detailed_fields(
    mock_config: AirtableConfig,
    mock_table: Mock,
) -> None:
    """Test that find_by_email returns EmployeeRecord with detailed fields populated."""
    mock_table.all.return_value = [
        {
            "id": "rec123",
            "fields": {
                "Email": "chase.pettet@example.com",
                "Manager Email": "mel.masterson@example.com",
                "Employee Status": "FTE",
                "Name": "Chase Pettet",
                "Title": "Principal Security Engineer",
                "Department": "IT",
                "Division": "Engineering",
                "Eng Team": "Security",
                "Operating Group": "Security",
                "Start Date": "2025-06-02",
                "State": "Missouri",
                "Employment Type": "Full Time",
                "Manager Name": "Mel Masterson",
            },
        }
    ]

    client = AirtableClient(mock_config)
    client._table = mock_table

    result = client.find_by_email("chase.pettet@example.com")

    assert result is not None
    assert result.email == "chase.pettet@example.com"
    assert result.manager_email == "mel.masterson@example.com"
    assert result.employment_status == "FTE"
    assert result.name == "Chase Pettet"
    assert result.title == "Principal Security Engineer"
    assert result.department == "IT"
    assert result.division == "Engineering"
    assert result.eng_team == "Security"
    assert result.operating_group == "Security"
    assert result.start_date == "2025-06-02"
    assert result.state == "Missouri"
    assert result.employment_type == "Full Time"
    assert result.manager_name == "Mel Masterson"


def test_find_by_email_returns_none_when_not_found(
    mock_config: AirtableConfig,
    mock_table: Mock,
) -> None:
    """Test that find_by_email returns None when email is not found."""
    mock_table.all.return_value = []

    client = AirtableClient(mock_config)
    client._table = mock_table

    result = client.find_by_email("nonexistent@example.com")

    assert result is None


def test_find_by_email_handles_missing_manager(
    mock_config: AirtableConfig,
    mock_table: Mock,
) -> None:
    """Test that find_by_email handles records without manager email."""
    mock_table.all.return_value = [
        {
            "id": "rec123",
            "fields": {
                "Email": "ceo@example.com",
                "Employee Status": "FTE",
            },
        }
    ]

    client = AirtableClient(mock_config)
    client._table = mock_table

    result = client.find_by_email("ceo@example.com")

    assert result is not None
    assert result.email == "ceo@example.com"
    assert result.manager_email is None
    assert result.employment_status == "FTE"


def test_find_by_email_is_case_insensitive(
    mock_config: AirtableConfig,
    mock_table: Mock,
) -> None:
    """Test that find_by_email performs case-insensitive matching."""
    mock_table.all.return_value = [
        {
            "id": "rec123",
            "fields": {
                "Email": "John.Doe@Example.com",
                "Manager Email": "jane.smith@example.com",
                "Employee Status": "FTE",
            },
        }
    ]

    client = AirtableClient(mock_config)
    client._table = mock_table

    result = client.find_by_email("john.doe@example.com")

    assert result is not None
    assert result.email == "John.Doe@Example.com"


def test_get_employee_with_management_chain_full_chain(
    mock_config: AirtableConfig,
    mock_table: Mock,
) -> None:
    """Test getting employee with full management chain (employee → manager → manager's manager)."""
    def mock_all(formula: str) -> List[Dict[str, Any]]:
        """Mock the table.all() method to return different records based on email."""
        if "john.doe@example.com" in formula.lower():
            return [
                {
                    "id": "rec1",
                    "fields": {
                        "Email": "john.doe@example.com",
                        "Manager Email": "jane.smith@example.com",
                        "Employee Status": "FTE",
                    },
                }
            ]
        elif "jane.smith@example.com" in formula.lower():
            return [
                {
                    "id": "rec2",
                    "fields": {
                        "Email": "jane.smith@example.com",
                        "Manager Email": "ceo@example.com",
                        "Employee Status": "FTE",
                    },
                }
            ]
        elif "ceo@example.com" in formula.lower():
            return [
                {
                    "id": "rec3",
                    "fields": {
                        "Email": "ceo@example.com",
                        "Employee Status": "FTE",
                    },
                }
            ]
        return []

    mock_table.all.side_effect = mock_all

    client = AirtableClient(mock_config)
    client._table = mock_table

    result = client.get_employee_with_management_chain("john.doe@example.com")

    assert result is not None
    assert isinstance(result, EmployeeLookupResult)
    assert result.employee.email == "john.doe@example.com"
    assert result.manager is not None
    assert result.manager.email == "jane.smith@example.com"
    assert result.managers_manager is not None
    assert result.managers_manager.email == "ceo@example.com"


def test_get_employee_with_management_chain_no_manager(
    mock_config: AirtableConfig,
    mock_table: Mock,
) -> None:
    """Test getting employee without manager (e.g., CEO)."""
    mock_table.all.return_value = [
        {
            "id": "rec1",
            "fields": {
                "Email": "ceo@example.com",
                "Employee Status": "FTE",
            },
        }
    ]

    client = AirtableClient(mock_config)
    client._table = mock_table

    result = client.get_employee_with_management_chain("ceo@example.com")

    assert result is not None
    assert result.employee.email == "ceo@example.com"
    assert result.manager is None
    assert result.managers_manager is None


def test_get_employee_with_management_chain_only_one_manager(
    mock_config: AirtableConfig,
    mock_table: Mock,
) -> None:
    """Test getting employee with manager but manager has no manager."""
    def mock_all(formula: str) -> List[Dict[str, Any]]:
        if "john.doe@example.com" in formula.lower():
            return [
                {
                    "id": "rec1",
                    "fields": {
                        "Email": "john.doe@example.com",
                        "Manager Email": "ceo@example.com",
                        "Employee Status": "FTE",
                    },
                }
            ]
        elif "ceo@example.com" in formula.lower():
            return [
                {
                    "id": "rec2",
                    "fields": {
                        "Email": "ceo@example.com",
                        "Employee Status": "FTE",
                    },
                }
            ]
        return []

    mock_table.all.side_effect = mock_all

    client = AirtableClient(mock_config)
    client._table = mock_table

    result = client.get_employee_with_management_chain("john.doe@example.com")

    assert result is not None
    assert result.employee.email == "john.doe@example.com"
    assert result.manager is not None
    assert result.manager.email == "ceo@example.com"
    assert result.managers_manager is None


def test_get_employee_with_management_chain_employee_not_found(
    mock_config: AirtableConfig,
    mock_table: Mock,
) -> None:
    """Test getting employee that doesn't exist."""
    mock_table.all.return_value = []

    client = AirtableClient(mock_config)
    client._table = mock_table

    result = client.get_employee_with_management_chain("nonexistent@example.com")

    assert result is None
