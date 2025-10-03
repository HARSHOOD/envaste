import frappe
from frappe.utils import cint, cstr

def custom_get_account_autoname(account_number, account_name, company):
    parts = [account_name.strip()]  
    if cstr(account_number).strip():
        parts.insert(0, cstr(account_number).strip()) 
    return " - ".join(parts) 