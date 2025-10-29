import frappe
from frappe import _

def validate_multi_currency(doc, method):
    """
    Allow Purchase Orders to use a currency different from Supplier's default.
    Keeps supplier currency unchanged but allows per-transaction flexibility.
    """
    supplier_currency = frappe.db.get_value("Supplier", doc.supplier, "default_currency")
    
    if doc.currency != supplier_currency:
        frappe.logger().info(f"[Envaste] Currency override: {doc.name} using {doc.currency} instead of {supplier_currency}")
        
        # Ensure we have a valid conversion rate
        if not doc.conversion_rate or doc.conversion_rate <= 0:
            doc.conversion_rate = frappe.db.get_value(
                "Currency Exchange",
                {"from_currency": doc.currency, "to_currency": doc.company_currency},
                "exchange_rate"
            ) or 1

        doc.add_comment("Comment", f"Currency overridden from {supplier_currency} to {doc.currency} by Envaste custom logic.")