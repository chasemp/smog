"""Pydantic data models for employee records."""

from typing import Optional

from pydantic import BaseModel, Field


class EmployeeRecord(BaseModel):
    """Represents an employee record from Airtable."""

    email: str = Field(..., description="Employee email address")
    manager_email: Optional[str] = Field(None, description="Manager's email address")
    employment_status: str = Field(..., description="Employment status (FTE, Contractor, etc.)")


class EmployeeLookupResult(BaseModel):
    """
    Result of an employee lookup including management chain.

    Contains the employee, their manager, and their manager's manager.
    """

    employee: EmployeeRecord = Field(..., description="The employee being looked up")
    manager: Optional[EmployeeRecord] = Field(None, description="The employee's manager")
    managers_manager: Optional[EmployeeRecord] = Field(None, description="The manager's manager")
