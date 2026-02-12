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


def test_employee_record_with_detailed_fields() -> None:
    """Test EmployeeRecord with optional detailed fields populated."""
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

    assert employee.email == "chase.pettet@example.com"
    assert employee.manager_email == "mel.masterson@example.com"
    assert employee.employment_status == "FTE"
    assert employee.name == "Chase Pettet"
    assert employee.title == "Principal Security Engineer"
    assert employee.department == "IT"
    assert employee.division == "Engineering"
    assert employee.eng_team == "Security"
    assert employee.operating_group == "Security"
    assert employee.start_date == "2025-06-02"
    assert employee.state == "Missouri"
    assert employee.employment_type == "Full Time"
    assert employee.manager_name == "Mel Masterson"


def test_employee_record_with_partial_detailed_fields() -> None:
    """Test EmployeeRecord with only some optional detailed fields populated."""
    employee = EmployeeRecord(
        email="john.doe@example.com",
        manager_email="jane.smith@example.com",
        employment_status="FTE",
        name="John Doe",
        title="Software Engineer",
    )

    assert employee.email == "john.doe@example.com"
    assert employee.name == "John Doe"
    assert employee.title == "Software Engineer"
    assert employee.department is None
    assert employee.division is None
    assert employee.eng_team is None
    assert employee.operating_group is None
    assert employee.start_date is None
    assert employee.state is None
    assert employee.employment_type is None
    assert employee.manager_name is None
