import frappe
from frappe.utils import add_days, now_datetime

from datetime import datetime, timedelta

def send_notification():
    today = datetime.today().date()
    quotations = frappe.get_all("Quotation", filters={"custom_expiry_date": (">", today)}, fields=["name", "custom_expiry_date", "owner", "customer_name"])
    
    for quotation in quotations:
        doc_name = quotation.name
        customer_name = quotation.customer_name
        expiry_date = quotation.custom_expiry_date
        two_days_before = expiry_date - timedelta(days=2)
        if today == two_days_before:
            for_user = quotation.owner
            message = f"Reminder for Quotation {doc_name}: This Customer {customer_name} Quotation has an expiry date of {expiry_date}. Please take necessary action."
            subject = message
            make_notification_log(subject, for_user, message, "Quotation", doc_name)

def make_notification_log(subject, for_user, message, doctype, doc_name):
    new_notification_log = frappe.new_doc("Notification Log")
    new_notification_log.subject = subject
    new_notification_log.for_user = for_user
    new_notification_log.email_content = message
    new_notification_log.document_type = doctype
    new_notification_log.document_name = doc_name
    new_notification_log.save(ignore_permissions=True)


def validate_custom_expiry_date(doc, method):
    today = datetime.today().date()
    custom_expiry_date = datetime.strptime(doc.custom_expiry_date, '%Y-%m-%d').date()
    
    if custom_expiry_date < today:
        frappe.throw("You cannot select a past date for the custom expiry date.")