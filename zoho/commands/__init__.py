"""
Main command groups for Zoho Books CLI
"""

import click

from .. import __version__
from ..settings import settings


from .config import config
from .invoices import invoices



@click.group()
@click.version_option(version=__version__)
@click.option('--client-id', help='Zoho Client ID', envvar='ZOHO_CLIENT_ID')
@click.option('--client-secret', help='Zoho Client Secret', envvar='ZOHO_CLIENT_SECRET')
@click.option('--refresh-token', help='Zoho Refresh Token', envvar='ZOHO_REFRESH_TOKEN')
@click.option('--org-id', help='Zoho Organization ID', envvar='ZOHO_ORG_ID')
def cli(client_id, client_secret, refresh_token, org_id):
    """Zoho Books CLI - Manage your Zoho Books account."""

    settings.client_id = client_id
    settings.client_secret = client_secret
    settings.refresh_token = refresh_token
    settings.org_id = org_id


# Add command groups to the main zoho group
cli.add_command(config)
cli.add_command(invoices)
