"""Tests for CLI interface."""

from unittest.mock import Mock, patch

from click.testing import CliRunner

from smog.cli import main
from smog.models import EmployeeRecord, EmployeeLookupResult


def test_cli_with_full_management_chain() -> None:
    """Test CLI output with employee, manager, and manager's manager."""
    runner = CliRunner()

    employee = EmployeeRecord(
        email="john.doe@example.com",
        manager_email="jane.smith@example.com",
        employment_status="FTE",
    )
    manager = EmployeeRecord(
        email="jane.smith@example.com",
        manager_email="ceo@example.com",
        employment_status="FTE",
    )
    managers_manager = EmployeeRecord(
        email="ceo@example.com",
        manager_email=None,
        employment_status="FTE",
    )

    result_obj = EmployeeLookupResult(
        employee=employee,
        manager=manager,
        managers_manager=managers_manager,
    )

    with patch("smog.cli.AirtableClient") as mock_client_class:
        mock_client = Mock()
        mock_client.get_employee_with_management_chain.return_value = result_obj
        mock_client_class.return_value = mock_client

        result = runner.invoke(main, ["john.doe@example.com"])

    assert result.exit_code == 0
    assert "john.doe@example.com" in result.output
    assert "jane.smith@example.com" in result.output
    assert "ceo@example.com" in result.output
    assert "FTE" in result.output


def test_cli_employee_not_found() -> None:
    """Test CLI output when employee is not found."""
    runner = CliRunner()

    with patch("smog.cli.AirtableClient") as mock_client_class:
        mock_client = Mock()
        mock_client.get_employee_with_management_chain.return_value = None
        mock_client_class.return_value = mock_client

        result = runner.invoke(main, ["nonexistent@example.com"])

    assert result.exit_code == 1
    assert "not found" in result.output.lower()


def test_cli_employee_without_manager() -> None:
    """Test CLI output for employee without manager."""
    runner = CliRunner()

    employee = EmployeeRecord(
        email="ceo@example.com",
        manager_email=None,
        employment_status="FTE",
    )

    result_obj = EmployeeLookupResult(
        employee=employee,
        manager=None,
        managers_manager=None,
    )

    with patch("smog.cli.AirtableClient") as mock_client_class:
        mock_client = Mock()
        mock_client.get_employee_with_management_chain.return_value = result_obj
        mock_client_class.return_value = mock_client

        result = runner.invoke(main, ["ceo@example.com"])

    assert result.exit_code == 0
    assert "ceo@example.com" in result.output
    assert "No manager" in result.output or "N/A" in result.output


def test_cli_employee_with_manager_no_managers_manager() -> None:
    """Test CLI output for employee with manager but no manager's manager."""
    runner = CliRunner()

    employee = EmployeeRecord(
        email="john.doe@example.com",
        manager_email="ceo@example.com",
        employment_status="Contractor",
    )
    manager = EmployeeRecord(
        email="ceo@example.com",
        manager_email=None,
        employment_status="FTE",
    )

    result_obj = EmployeeLookupResult(
        employee=employee,
        manager=manager,
        managers_manager=None,
    )

    with patch("smog.cli.AirtableClient") as mock_client_class:
        mock_client = Mock()
        mock_client.get_employee_with_management_chain.return_value = result_obj
        mock_client_class.return_value = mock_client

        result = runner.invoke(main, ["john.doe@example.com"])

    assert result.exit_code == 0
    assert "john.doe@example.com" in result.output
    assert "ceo@example.com" in result.output
    assert "Contractor" in result.output


def test_cli_appends_example_domain_when_missing() -> None:
    """Test that CLI appends @example.com when email has no domain."""
    runner = CliRunner()

    employee = EmployeeRecord(
        email="cpettet@example.com",
        manager_email="manager@example.com",
        employment_status="FTE",
    )

    result_obj = EmployeeLookupResult(
        employee=employee,
        manager=None,
        managers_manager=None,
    )

    with patch("smog.cli.AirtableClient") as mock_client_class:
        mock_client = Mock()
        mock_client.get_employee_with_management_chain.return_value = result_obj
        mock_client_class.return_value = mock_client

        result = runner.invoke(main, ["cpettet"])

        mock_client.get_employee_with_management_chain.assert_called_with("cpettet@example.com")

    assert result.exit_code == 0


def test_cli_preserves_full_email_address() -> None:
    """Test that CLI doesn't modify email if it already has @example.com."""
    runner = CliRunner()

    employee = EmployeeRecord(
        email="cpettet@example.com",
        manager_email="manager@example.com",
        employment_status="FTE",
    )

    result_obj = EmployeeLookupResult(
        employee=employee,
        manager=None,
        managers_manager=None,
    )

    with patch("smog.cli.AirtableClient") as mock_client_class:
        mock_client = Mock()
        mock_client.get_employee_with_management_chain.return_value = result_obj
        mock_client_class.return_value = mock_client

        result = runner.invoke(main, ["cpettet@example.com"])

        mock_client.get_employee_with_management_chain.assert_called_with("cpettet@example.com")

    assert result.exit_code == 0


def test_cli_preserves_other_domain() -> None:
    """Test that CLI doesn't modify email if it has a different domain."""
    runner = CliRunner()

    employee = EmployeeRecord(
        email="external@example.com",
        manager_email=None,
        employment_status="Contractor",
    )

    result_obj = EmployeeLookupResult(
        employee=employee,
        manager=None,
        managers_manager=None,
    )

    with patch("smog.cli.AirtableClient") as mock_client_class:
        mock_client = Mock()
        mock_client.get_employee_with_management_chain.return_value = result_obj
        mock_client_class.return_value = mock_client

        result = runner.invoke(main, ["external@example.com"])

        mock_client.get_employee_with_management_chain.assert_called_with("external@example.com")

    assert result.exit_code == 0
