import frappe
from frappe.utils import cstr

@frappe.whitelist()
def get_display_address(address_name):
    """
    Given an Address name, return a nicely formatted multi-line string.
    """ 
    # print("get_display_address++++++++++++++++++++++++++++++++++++++++++")
    if not address_name:
        return ""
    
    print("get_display_address++++++++++++++++++++++++++++++++++++++++++",address_name)
    try:
        address = frappe.get_doc("Address", address_name)
    except frappe.DoesNotExistError:
        return ""

    # Build formatted address
    lines = [
        address.get("address_display") or "",
        address.get("address_line1") or "",
        address.get("address_line2") or "",
        address.get("city") or "",
        address.get("county") or "",
        address.get("state") or "",
        address.get("pincode") or "",
        address.get("fax") or "",
        address.get("country") or "",
        address.get("email_id") or "",
        address.get("phone") or "",
    ]

    # Join with newlines, removing empty ones
    formatted = "\n".join([cstr(line) for line in lines if line])
    print("formatted\n",formatted)
    return formatted


