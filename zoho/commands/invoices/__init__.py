"""
Invoices commands for Zoho Books CLI
"""

import click

from .list import list as invoices_list
from .report_gaps import report_gaps


@click.group()
def invoices():
    """Manage Zoho Books invoices."""
    pass


# Add invoice commands to the group
invoices.add_command(invoices_list)
invoices.add_command(report_gaps)
