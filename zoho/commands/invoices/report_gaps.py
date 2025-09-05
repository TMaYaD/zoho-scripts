"""
Renumber command for Zoho Books invoices
"""

import click
import re
import sys
from pathlib import Path

from ...managers import InvoiceManager

class InvoiceRenumberingPlan:
    invoice: dict
    prefix: str
    suffix: str
    new_numeric_index: int

    def __init__(self, invoice, prefix, suffix):
        self.invoice = invoice
        self.prefix = prefix
        self.suffix = suffix

    @property
    def old_number(self):
        return self.invoice.get("invoice_number", None)

    @property
    def old_numeric_index(self):
        if not self.old_number:
            return 0

        # Remove prefix and suffix
        invoice_number = self.old_number.replace(self.prefix, "").replace(self.suffix, "")

        # Try to extract numbers from the invoice number
        numbers = re.findall(r"\d+", str(invoice_number))
        if numbers:
            return int(numbers[0])
        return 0

    @property
    def date(self):
        return self.invoice.get("date", "Unknown date")

    @property
    def new_number(self):
        return f"{self.prefix}{self.new_numeric_index:06d}{self.suffix}"

    def in_range(self, from_number=None, to_number=None):
        if from_number is not None and self.old_numeric_index < from_number:
            return False

        if to_number is not None and self.old_numeric_index > to_number:
            return False

        return True

    def show(self):
        click.echo(
            f"{self.old_numeric_index:3d}. {self.old_number:15s} → {self.new_number:15s} ({self.date})"
        )

    def save(self, invoice_manager):
        invoice_id = self.invoice.get("invoice_id", "Unknown")

        self.invoice = invoice_manager.get(invoice_id)
        if not self.invoice:
            return None

        self.invoice["invoice_number"] = self.new_number
        self.invoice["reason"] = "Invoice renumbering"
        return invoice_manager.update(self.invoice, params={"ignore_auto_number_generation": True})

class InvoiceRenumberer:
    """Handles invoice renumbering operations"""

    def __init__(self, invoice_manager, start_number, prefix, suffix, from_number, to_number):
        self.invoice_manager = invoice_manager
        self.start_number = start_number
        self.prefix = prefix
        self.suffix = suffix
        self.from_number = from_number
        self.to_number = to_number
        self.renumbered_count = 0
        self.errors = []
        self.renumbering_plan = None

    def get_sorted_invoices(self):
        """Get all invoices sorted by date"""
        params = {
            "invoice_number_starts_with": self.prefix,
            "invoice_number_contains": self.suffix,
            "sort_column": "invoice_number",
            "sort_order": "A",
        }

        return self.invoice_manager.list(params)

    def analyze_invoice_numbering(self):
        """Analyze current invoice numbering to identify patterns and gaps"""

        click.echo(f"Prefix: {self.prefix}")
        click.echo(f"Suffix: {self.suffix}")
        click.echo(f"From number: {self.from_number}")
        click.echo(f"To number: {self.to_number}")
        click.echo(f"Start number: {self.start_number}")
        click.echo("-" * 80)

        invoices = self.get_sorted_invoices()
        self.renumbering_plan = []
        for invoice in invoices:
            invoice_renumbering_plan = InvoiceRenumberingPlan(invoice, self.prefix, self.suffix)
            if invoice_renumbering_plan.in_range(self.from_number, self.to_number):
                self.renumbering_plan.append(invoice_renumbering_plan)

        # Find gaps
        gaps = []
        for i in range(len(self.renumbering_plan) - 1):
            next_index = self.renumbering_plan[i + 1].old_numeric_index
            current_index = self.renumbering_plan[i].old_numeric_index
            if next_index - current_index > 1:
                gaps.append((current_index, next_index))

        if gaps:
            click.echo(f"\nGaps found ({len(gaps)}):")
            for gap_start, gap_end in gaps:
                missing_count = gap_end - gap_start - 1
                click.echo(f"  {gap_start} → {gap_end} (missing {missing_count} numbers)")
        else:
            click.echo("\nNo gaps found in numbering.")

        # Assign new numeric indices
        for i, renumbering_plan in enumerate(self.renumbering_plan):
            renumbering_plan.new_numeric_index = i + self.start_number

        # Filter invoices that don't need any changes
        self.renumbering_plan = [plan for plan in self.renumbering_plan if plan.new_numeric_index != plan.old_numeric_index]

        if not self.renumbering_plan:
            click.echo("No invoices need to be renumbered.")
            return

        click.echo("Invoice Numbering Analysis")
        click.echo("=" * 50)

        for plan in self.renumbering_plan:
            plan.show()

    def renumber_invoices(self):
        """Renumber invoices sequentially"""

        if self.renumbering_plan is None:
            click.echo("No renumbering plan found. Attempting to analyze invoice numbering...")
            self.analyze_invoice_numbering()

        if len(self.renumbering_plan) == 0:
            click.echo("No invoices need to be renumbered. Exiting.")
            return

        click.echo("Renumbering invoices...")
        click.echo("-" * 80)
        # Process each invoice
        for i, plan in enumerate(self.renumbering_plan):
            try:
                plan.show()
                result = plan.save(self.invoice_manager)
                if result:
                    self.renumbered_count += 1
                    click.echo("    ✓ Successfully renumbered")
                else:
                    self.errors.append(f"Failed to renumber {plan.old_number}")
                    click.echo("    ✗ Failed to renumber")
            except Exception as e:
                error_msg = f"Error renumbering {plan.old_number}: {str(e)}"
                self.errors.append(error_msg)
                click.echo(f"    ✗ {error_msg}")

        click.echo("-" * 80)

        click.echo("RENUMBERING COMPLETE: Successfully renumbered {} invoices".format(self.renumbered_count))

        if self.errors:
            click.echo("\nErrors encountered ({}):".format(len(self.errors)))
            for error in self.errors:
                click.echo(f"  - {error}")


@click.command()
@click.option("--from_number", type=int, default=1, help="Filter invoices from this number")
@click.option("--to_number", type=int, default=None, help="Filter invoices to this number")
@click.option("--prefix", default="INV-", help="Prefix for invoice numbers")
@click.option("--suffix", default="", help="Suffix for invoice numbers")
@click.option("--start_number", type=int, default=None, help="Starting number for renumbering")
@click.option(
    "--fix",
    is_flag=True,
    default=False,
    help="Fix the gaps by renumbering the invoices",
)
def report_gaps(from_number, to_number, prefix, suffix, start_number, fix):
    """Report gaps in invoice numbering."""
    if start_number is None:
        start_number = from_number

    invoice_manager = InvoiceManager()
    renumberer = InvoiceRenumberer(invoice_manager,
            start_number=start_number,
            prefix=prefix,
            suffix=suffix,
            from_number=from_number,
            to_number=to_number,
    )

    click.echo("Zoho Books Invoice Renumbering Tool")
    click.echo("=" * 50)

    # First, analyze current numbering
    click.echo("\n1. Analyzing current invoice numbering...")
    renumberer.analyze_invoice_numbering()

    click.echo("\n" + "=" * 50)

    if fix:
        # Perform renumbering
        click.echo("\n2. Starting renumbering process...")
        renumberer.renumber_invoices()

    click.echo("\n" + "=" * 50)
    click.echo("Process completed!")
