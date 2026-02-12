"""CLI interface for employee lookup."""

import sys

import click

from smog.client import AirtableClient
from smog.config import load_app_config, load_config


def normalize_email(email: str, default_domain: str) -> str:
    """
    Normalize email by optionally appending default domain.

    Args:
        email: Email address or username.
        default_domain: Domain to append if email has no @ and domain is configured.

    Returns:
        Normalized email address.
    """
    if "@" not in email and default_domain:
        return f"{email}@{default_domain}"
    return email


@click.command()
@click.argument("email")
@click.option("--details", is_flag=True, help="Show detailed employee information")
def main(email: str, details: bool) -> None:
    """
    Look up an employee by email and display their manager chain.

    Args:
        email: Employee email address or username to look up.
               If no @ is present and default_email_domain is configured,
               the domain will be appended.
        details: Whether to show detailed employee information.
    """
    app_config = load_app_config()
    normalized_email = normalize_email(email, app_config["default_email_domain"])

    config = load_config()
    client = AirtableClient(config)

    result = client.get_employee_with_management_chain(normalized_email)

    if result is None:
        click.echo(f"Employee not found: {normalized_email}", err=True)
        sys.exit(1)

    click.echo("\n=== Employee Information ===")
    click.echo(f"Email:             {result.employee.email}")
    click.echo(f"Employment Status: {result.employee.employment_status}")

    if details:
        if result.employee.name:
            click.echo(f"Name:              {result.employee.name}")
        if result.employee.title:
            click.echo(f"Title:             {result.employee.title}")
        if result.employee.department:
            click.echo(f"Department:        {result.employee.department}")
        if result.employee.division:
            click.echo(f"Division:          {result.employee.division}")
        if result.employee.eng_team:
            click.echo(f"Engineering Team:  {result.employee.eng_team}")
        if result.employee.operating_group:
            click.echo(f"Operating Group:   {result.employee.operating_group}")
        if result.employee.start_date:
            click.echo(f"Start Date:        {result.employee.start_date}")
        if result.employee.state:
            click.echo(f"Location:          {result.employee.state}")
        if result.employee.employment_type:
            click.echo(f"Employment Type:   {result.employee.employment_type}")

    click.echo("\n=== Management Chain ===")
    if result.manager:
        if details and result.employee.manager_name:
            click.echo(f"Manager:           {result.employee.manager_name} ({result.manager.email})")
        else:
            click.echo(f"Manager:           {result.manager.email}")
    else:
        click.echo("Manager:           N/A")

    if result.managers_manager:
        click.echo(f"Manager's Manager: {result.managers_manager.email}")
    else:
        click.echo("Manager's Manager: N/A")

    click.echo()


if __name__ == "__main__":
    main()
