"""Tests for Pydantic data models."""

from smog.models import EmployeeRecord, EmployeeLookupResult


def test_employee_record_with_all_fields() -> None:
    """Test EmployeeRecord with all fields populated."""
    employee = EmployeeRecord(
        email="john.doe@example.com",
        manager_email="jane.smith@example.com",
        employment_status="FTE",
    )

    assert employee.email == "john.doe@example.com"
    assert employee.manager_email == "jane.smith@example.com"
    assert employee.employment_status == "FTE"


def test_employee_record_without_manager() -> None:
    """Test EmployeeRecord without manager (e.g., CEO)."""
    employee = EmployeeRecord(
        email="ceo@example.com",
        manager_email=None,
        employment_status="FTE",
    )

    assert employee.email == "ceo@example.com"
    assert employee.manager_email is None
    assert employee.employment_status == "FTE"


def test_employee_lookup_result_with_full_chain() -> None:
    """Test EmployeeLookupResult with employee, manager, and manager's manager."""
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

    result = EmployeeLookupResult(
        employee=employee,
        manager=manager,
        managers_manager=managers_manager,
    )

    assert result.employee.email == "john.doe@example.com"
    assert result.manager is not None
    assert result.manager.email == "jane.smith@example.com"
    assert result.managers_manager is not None
    assert result.managers_manager.email == "ceo@example.com"


def test_employee_lookup_result_without_managers() -> None:
    """Test EmployeeLookupResult for employee without any manager."""
    employee = EmployeeRecord(
        email="ceo@example.com",
        manager_email=None,
        employment_status="FTE",
    )

    result = EmployeeLookupResult(
        employee=employee,
        manager=None,
        managers_manager=None,
    )

    assert result.employee.email == "ceo@example.com"
    assert result.manager is None
    assert result.managers_manager is None
