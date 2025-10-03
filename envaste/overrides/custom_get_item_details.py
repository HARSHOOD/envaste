import frappe
import json
from frappe.utils import add_days, add_months, cint, cstr, flt, getdate
from erpnext.stock.get_item_details import process_args,process_string_args,validate_item_details,get_basic_details,get_item_tax_template,get_item_tax_map,get_party_item_code,set_valuation_rate,update_party_blanket_order,get_price_list_rate,get_bin_details,get_pricing_rule_for_item,get_gross_profit,remove_standard_fields

@frappe.whitelist()
def custom_get_item_details(args, doc=None, for_validate=False, overwrite_warehouse=True):
    """
    args = {
            "item_code": "",
            "warehouse": None,
            "customer": "",
            "conversion_rate": 1.0,
            "selling_price_list": None,
            "price_list_currency": None,
            "plc_conversion_rate": 1.0,
            "doctype": "",
            "name": "",
            "supplier": None,
            "transaction_date": None,
            "conversion_rate": 1.0,
            "buying_price_list": None,
            "is_subcontracted": 0/1,
            "ignore_pricing_rule": 0/1
            "project": ""
            "set_warehouse": ""
    }
    """

    args = process_args(args)
    for_validate = process_string_args(for_validate)
    overwrite_warehouse = process_string_args(overwrite_warehouse)
    item = frappe.get_cached_doc("Item", args.item_code)
    validate_item_details(args, item)


    if isinstance(doc, str):
        doc = json.loads(doc)

    if doc:
        args["transaction_date"] = doc.get("transaction_date") or doc.get("posting_date")

        if doc.get("doctype") == "Purchase Invoice":
            args["bill_date"] = doc.get("bill_date")

    out = get_basic_details(args, item, overwrite_warehouse)

    get_item_tax_template(args, item, out)
    out["item_tax_rate"] = get_item_tax_map(
        args.company,
        args.get("item_tax_template")
        if out.get("item_tax_template") is None
        else out.get("item_tax_template"),
        as_json=True,
    )

    get_party_item_code(args, item, out)

    if args.get("doctype") in ["Sales Order", "Quotation"]:
        set_valuation_rate(out, args)

    update_party_blanket_order(args, out)

    # Never try to find a customer price if customer is set in these Doctype
    current_customer = args.customer
    if args.get("doctype") in ["Purchase Order", "Purchase Receipt", "Purchase Invoice"]:
        args.customer = None

    out.update(get_price_list_rate(args, item))

    args.customer = current_customer

    if args.customer and cint(args.is_pos):
        out.update(get_pos_profile_item_details(args.company, args, update_data=True))

    if (
        args.get("doctype") == "Material Request"
        and args.get("material_request_type") == "Material Transfer"
    ):
        out.update(get_bin_details(args.item_code, args.get("from_warehouse")))

    elif out.get("warehouse"):
        if doc and doc.get("doctype") == "Purchase Order":
            # calculate company_total_stock only for po
            bin_details = get_bin_details(
                args.item_code, out.warehouse, args.company, include_child_warehouses=True
            )
        else:
            bin_details = get_bin_details(args.item_code, out.warehouse, include_child_warehouses=True)

        out.update(bin_details)

    # Set quantity to 0 by default
    out["qty"] = 0

    # update args with out, if key or value not exists
    for key, value in out.items():
        if args.get(key) is None:
            args[key] = value

    data = get_pricing_rule_for_item(args, doc=doc, for_validate=for_validate)

    out.update(data)

    if args.transaction_date and item.lead_time_days:
        out.schedule_date = out.lead_time_date = add_days(args.transaction_date, item.lead_time_days)

    if args.get("is_subcontracted"):
        out.bom = args.get("bom") or get_default_bom(args.item_code)

    get_gross_profit(out)
    if args.doctype == "Material Request":
        out.rate = args.rate or out.price_list_rate
        out.amount = flt(args.qty) * flt(out.rate)

    out = remove_standard_fields(out)
    return out