import click

from ...settings import settings
from ...client import client


@click.command()
@click.argument("org_id", type=str, required=False)
def org(org_id):
    """Select Organisation."""

    if org_id:
        settings.org_id = org_id
        return

    orgs = client.get("organizations").get("organizations")

    click.echo("Select an organisation:")
    for i, org in enumerate(orgs):
        click.echo(f"{i+1}. {org.get('name', 'N/A')}")

    choice = click.prompt("Enter the number of the organisation", type=int)
    settings.org_id = orgs[choice - 1].get("organization_id")
    settings.save()
