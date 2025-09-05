"""
Invoices commands for Zoho Books CLI
"""

import click


from .org import org

@click.group()
def config():
    """Manage Configuration."""
    pass


# Add invoice commands to the group
config.add_command(org)
