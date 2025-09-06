"""
Configuration commands for Zoho Books CLI
"""

import click


from .org import org
from .setup import setup


@click.group()
def config():
    """Manage Configuration."""
    pass


# Add config commands to the group
config.add_command(org)
config.add_command(setup)
