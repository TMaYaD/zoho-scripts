from ..client import client

class InvoiceManager():
    """Manages Zoho Books invoices"""

    def list(self, params=None):
        """List invoices with optional filtering"""
        response = client.get("invoices", params=params)
        return response.get("invoices", [])

    def get(self, invoice_id):
        """Get a specific invoice by ID"""
        response = client.get(f"invoices/{invoice_id}")
        return response.get("invoice")

    def update(self, invoice, params=None):
        """Update an invoice"""
        # Remove fields that shouldn't be sent in update
        fields_to_remove = [
            "tax_treatment",
            "billing_address",
            "shipping_address",
            "shipping_charge_account_id",
            "customer_default_billing_address",
            "contact_persons_details",
            "contact",
            "invoice_url",
            "qr_code",
            "sales_channel",
            "transaction_rounding_type",
            "zcrm_potential_name",
        ]

        for field in fields_to_remove:
            invoice.pop(field, None)

        response = client.put(f"invoices/{invoice['invoice_id']}", invoice, params=params)
        print(f"{invoice['invoice_number']}({response.get('code', 0)}): {response.get('message', '')}")
        return response.get("invoice")
