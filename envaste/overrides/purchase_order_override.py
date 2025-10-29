import frappe

def validate_multi_currency(doc, method):
    """
    Allow Purchase Orders to use a currency different from Supplier's default.
    Keeps supplier currency unchanged but allows per-transaction flexibility.
    """
    supplier_currency = frappe.db.get_value("Supplier", doc.supplier, "default_currency")

    if not supplier_currency:
        return  # Supplier has no default currency set

    if doc.currency != supplier_currency:
        frappe.logger().info(f"[Envaste] Currency override triggered on {doc.name} ({supplier_currency} → {doc.currency})")

        # Ensure we have a valid conversion rate
        if not doc.conversion_rate or doc.conversion_rate <= 0:
            rate = frappe.db.get_value(
                "Currency Exchange",
                {"from_currency": doc.currency, "to_currency": doc.company_currency},
                "exchange_rate"
            )
            doc.conversion_rate = rate or 1

        # Add an informative comment for traceability
        try:
            doc.add_comment("Comment", f"Currency overridden from {supplier_currency} to {doc.currency} by Envaste logic.")
        except Exception as e:
            frappe.logger().warning(f"[Envaste] Could not add comment: {e}")