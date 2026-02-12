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


def test_cli_with_details_flag_shows_additional_fields() -> None:
    """Test that CLI shows detailed fields when --details flag is provided."""
    runner = CliRunner()

    employee = EmployeeRecord(
        email="chase.pettet@example.com",
        manager_email="mel.masterson@example.com",
        employment_status="FTE",
        name="Chase Pettet",
        title="Principal Security Engineer",
        department="IT",
        division="Engineering",
        eng_team="Security",
        operating_group="Security",
        start_date="2025-06-02",
        state="Missouri",
        employment_type="Full Time",
        manager_name="Mel Masterson",
    )
    manager = EmployeeRecord(
        email="mel.masterson@example.com",
        manager_email="john.moore@example.com",
        employment_status="FTE",
        name="Mel Masterson",
        title="Director of Security",
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

        result = runner.invoke(main, ["chase.pettet@example.com", "--details"])

    assert result.exit_code == 0
    assert "Chase Pettet" in result.output
    assert "Principal Security Engineer" in result.output
    assert "IT" in result.output
    assert "Engineering" in result.output
    assert "Security" in result.output
    assert "2025-06-02" in result.output
    assert "Missouri" in result.output
    assert "Full Time" in result.output
    assert "Mel Masterson" in result.output


def test_cli_without_details_flag_shows_minimal_fields() -> None:
    """Test that CLI shows only minimal fields when --details flag is not provided."""
    runner = CliRunner()

    employee = EmployeeRecord(
        email="chase.pettet@example.com",
        manager_email="mel.masterson@example.com",
        employment_status="FTE",
        name="Chase Pettet",
        title="Principal Security Engineer",
        department="IT",
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

        result = runner.invoke(main, ["chase.pettet@example.com"])

    assert result.exit_code == 0
    assert "chase.pettet@example.com" in result.output
    assert "FTE" in result.output
    # Detailed fields should not appear without --details flag
    assert "Chase Pettet" not in result.output
    assert "Principal Security Engineer" not in result.output
    assert "IT" not in result.output
