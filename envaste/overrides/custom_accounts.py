import frappe
from frappe import _
import functools
import math
from json import loads
import re
from erpnext.accounts.utils import get_balance_on
from frappe.utils import (
	cstr,
	flt,
)

# def custom_get_ancestors_of(doctype, name, order_by="lft desc", limit=None):
# 	"""Get ancestor elements of a DocType with a tree structure"""
# 	lft, rgt = frappe.db.get_value(doctype, name, ["lft", "rgt"])
# 	if doctype == "Account":
# 		return frappe.get_all(
# 		doctype,
# 		{"lft": ["<", lft], "rgt": [">", rgt]},
# 		"name",
# 		order_by=order_by,
# 		limit_page_length=limit,
# 		pluck="account_name",
# 		)
# 	return frappe.get_all(
# 		doctype,
# 		{"lft": ["<", lft], "rgt": [">", rgt]},
# 		"name",
# 		order_by=order_by,
# 		limit_page_length=limit,
# 		pluck="name",
# 	)

# def sort_accounts(accounts, is_root=False, key="name"):
# 	"""Sort root types as Asset, Liability, Equity, Income, Expense"""

# 	def compare_accounts(a, b):
# 		if re.split(r"\W+", a[key])[0].isdigit():
# 			# if chart of accounts is numbered, then sort by number
# 			return int(a[key] > b[key]) - int(a[key] < b[key])
# 		elif is_root:
# 			if a.report_type != b.report_type and a.report_type == "Balance Sheet":
# 				return -1
# 			if a.root_type != b.root_type and a.root_type == "Asset":
# 				return -1
# 			if a.root_type == "Liability" and b.root_type == "Equity":
# 				return -1
# 			if a.root_type == "Income" and b.root_type == "Expense":
# 				return -1
# 		else:
# 			# sort by key (number) or name
# 			return int(a[key] > b[key]) - int(a[key] < b[key])
# 		return 1

# 	accounts.sort(key=functools.cmp_to_key(compare_accounts))


# @frappe.whitelist()
# def custom_get_children(doctype, parent, company, is_root=False):

# 	parent_fieldname = "parent_" + doctype.lower().replace(" ", "_")
# 	fields = ["name as value", "is_group as expandable"]
# 	filters = [["docstatus", "<", 2]]
# 	compare_string = " - "+frappe.db.get_value("Company",company,"abbr")
# 	if compare_string in parent:
# 		filters.append(['ifnull(`{0}`,"")'.format(parent_fieldname), "=", "" if is_root else parent])
# 	else:
# 		filters.append(['ifnull(`{0}`,"")'.format(parent_fieldname), "=", "" if is_root else parent+" - "+frappe.db.get_value("Company",company,"abbr")	])

# 	if is_root:
# 		fields += ["root_type", "report_type", "account_currency"] if doctype == "Account" else []
# 		filters.append(["company", "=", company])

# 	else:
# 		fields += ["root_type", "account_currency"] if doctype == "Account" else []
# 		fields += [parent_fieldname + " as parent"]
	
# 	acc = frappe.get_list(doctype, fields=fields, filters=filters)
# 	print(acc,"===")
# 	if doctype == "Account":
# 		sort_accounts(acc, is_root, key="value")
# 	for account in acc:
# 		account["value"] = account["value"][:-5]
# 	return acc

# @frappe.whitelist()
# def get_account_balances(accounts, company):

# 	if isinstance(accounts, str):
# 		accounts = loads(accounts)

# 	if not accounts:
# 		return []

# 	company_currency = frappe.get_cached_value("Company", company, "default_currency")

# 	for account in accounts:
# 		account["company_currency"] = company_currency
# 		account["balance"] = flt(
# 			get_balance_on(account["value"]+" - "+frappe.db.get_value("Company",company,"abbr"), in_account_currency=False, company=company)
# 		)
# 		if account["account_currency"] and account["account_currency"] != company_currency:
# 			account["balance_in_account_currency"] = flt(get_balance_on(account["value"]+" - "+frappe.db.get_value("Company",company,"abbr"), company=company))

# 	return accounts



def custom_get_autoname_with_number(number_value, doc_title, company):
	"""append title with prefix as number and suffix as company's abbreviation separated by '-'"""
	# company_abbr = frappe.get_cached_value("Company", company, "abbr")
	# monkey patch this line for Removing the Abbr from Naming
	# parts = [doc_title.strip(), company_abbr]
	parts = [doc_title.strip()]


	if cstr(number_value).strip():
		parts.insert(0, cstr(number_value).strip())

	return " - ".join(parts)