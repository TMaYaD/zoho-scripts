"""
List command for Zoho Books invoices
"""

import click
import sys
from pathlib import Path

from ...managers import InvoiceManager
from ...settings import settings


@click.command()
@click.option("--status", help="Filter invoices by status (sent, draft, void, etc.)")
@click.option("--limit", type=int, default=20, help="Limit number of results")
def list(status, limit):
    """List invoices in Zoho Books."""

    transaction_manager = InvoiceManager()

    params = {}
    if status:
        params["status"] = status

    invoices = transaction_manager.list_invoices(params)
    invoices = invoices[:limit]

    if not invoices:
        click.echo("No invoices found.")
        return

    click.echo(f"Found {len(invoices)} invoices:")
    click.echo("-" * 80)

    for invoice in invoices:
        click.echo(f"Number: {invoice.get('invoice_number', 'N/A')}")
        click.echo(f"Date: {invoice.get('date', 'N/A')}")
        click.echo(f"Status: {invoice.get('status', 'N/A')}")
        click.echo(f"Customer: {invoice.get('customer_name', 'N/A')}")
        click.echo(f"Amount: {invoice.get('total', 'N/A')}")
        click.echo("-" * 40)
