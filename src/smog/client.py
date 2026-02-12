"""Airtable client for employee lookups."""

from typing import Any, Dict, List, Optional

from pyairtable import Api

from smog.config import AirtableConfig
from smog.models import EmployeeRecord, EmployeeLookupResult


class AirtableClient:
    """Client for querying employee data from Airtable."""

    def __init__(self, config: AirtableConfig) -> None:
        """
        Initialize the Airtable client.

        Args:
            config: Configuration containing API key, base ID, and table name.
        """
        self._config = config
        api = Api(config.api_key)
        self._table = api.table(config.base_id, config.table_name)

    def find_by_email(self, email: str) -> Optional[EmployeeRecord]:
        """
        Find an employee by email address.

        Args:
            email: Employee email address to search for.

        Returns:
            EmployeeRecord if found, None otherwise.
        """
        formula = f"LOWER({{Email}}) = LOWER('{email}')"
        records = self._table.all(formula=formula)

        if not records:
            return None

        record = records[0]
        fields = record["fields"]

        return EmployeeRecord(
            email=fields.get("Email", ""),
            manager_email=fields.get("Manager Email"),
            employment_status=fields.get("Employee Status", "Unknown"),
        )

    def get_employee_with_management_chain(self, email: str) -> Optional[EmployeeLookupResult]:
        """
        Get employee with their full management chain.

        Looks up the employee, their manager, and their manager's manager.

        Args:
            email: Employee email address to search for.

        Returns:
            EmployeeLookupResult with employee and management chain, or None if employee not found.
        """
        employee = self.find_by_email(email)
        if employee is None:
            return None

        manager = None
        managers_manager = None

        if employee.manager_email:
            manager = self.find_by_email(employee.manager_email)
            if manager and manager.manager_email:
                managers_manager = self.find_by_email(manager.manager_email)

        return EmployeeLookupResult(
            employee=employee,
            manager=manager,
            managers_manager=managers_manager,
        )
