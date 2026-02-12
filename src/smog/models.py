"""Pydantic data models for employee records."""

from typing import Optional

from pydantic import BaseModel, Field


class EmployeeRecord(BaseModel):
    """Represents an employee record from Airtable."""

    email: str = Field(..., description="Employee email address")
    manager_email: Optional[str] = Field(None, description="Manager's email address")
    employment_status: str = Field(..., description="Employment status (FTE, Contractor, etc.)")
    name: Optional[str] = Field(None, description="Full name")
    title: Optional[str] = Field(None, description="Job title")
    department: Optional[str] = Field(None, description="Department")
    division: Optional[str] = Field(None, description="Division")
    eng_team: Optional[str] = Field(None, description="Engineering team")
    operating_group: Optional[str] = Field(None, description="Operating group")
    start_date: Optional[str] = Field(None, description="Start date")
    state: Optional[str] = Field(None, description="State/location")
    employment_type: Optional[str] = Field(None, description="Employment type (Full Time, Part Time, etc.)")
    manager_name: Optional[str] = Field(None, description="Manager's full name")


class EmployeeLookupResult(BaseModel):
    """
    Result of an employee lookup including management chain.

    Contains the employee, their manager, and their manager's manager.
    """

    employee: EmployeeRecord = Field(..., description="The employee being looked up")
    manager: Optional[EmployeeRecord] = Field(None, description="The employee's manager")
    managers_manager: Optional[EmployeeRecord] = Field(None, description="The manager's manager")
