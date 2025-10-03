import frappe
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from frappe.utils import (
    ceil,
    flt
)

from erpnext.manufacturing.doctype.production_plan.production_plan import get_item_details
from frappe.utils import (
	add_days,
	ceil,
	cint,
	comma_and,
	flt,
	get_link_to_form,
	getdate,
	now_datetime,
	nowdate,
)

def custom_get_material_request_items(
	doc,
	row,
	sales_order,
	company,
	ignore_existing_ordered_qty,
	include_safety_stock,
	warehouse,
	bin_dict,
):
    total_qty = row["qty"]
    required_qty = 0
    if ignore_existing_ordered_qty or bin_dict.get("projected_qty", 0) < 0:
        required_qty = total_qty
    elif total_qty > bin_dict.get("projected_qty", 0):
        required_qty = total_qty - bin_dict.get("projected_qty", 0)

    if (
        doc.get("consider_minimum_order_qty")
        and required_qty > 0
        and required_qty < row["min_order_qty"]
    ):
        required_qty = row["min_order_qty"]

    item_group_defaults = get_item_group_defaults(row.item_code, company)

    if not row["purchase_uom"]:
        row["purchase_uom"] = row["stock_uom"]

    if row["purchase_uom"] != row["stock_uom"]:
        if not (row["conversion_factor"] or frappe.flags.show_qty_in_stock_uom):
            frappe.throw(
                _("UOM Conversion factor ({0} -> {1}) not found for item: {2}").format(
                    row["purchase_uom"], row["stock_uom"], row.item_code
                )
            )

            required_qty = required_qty / row["conversion_factor"]

    if frappe.db.get_value("UOM", row["purchase_uom"], "must_be_whole_number"):
        required_qty = ceil(required_qty)

    if include_safety_stock:
        required_qty += flt(row["safety_stock"])

    item_details = frappe.get_cached_value(
        "Item", row.item_code, ["purchase_uom", "stock_uom"], as_dict=1
    )
    conversion_factor = 1.0
    if (
        row.get("default_material_request_type") == "Purchase"
        and item_details.purchase_uom
        and item_details.purchase_uom != item_details.stock_uom
    ):
        conversion_factor = (
            get_conversion_factor(row.item_code, item_details.purchase_uom).get("conversion_factor") or 1.0
        )
    total_stock=get_total_stock_in_all_warehose(row.item_code,company)
    if required_qty > 0:
        return {
            "item_code": row.item_code,
            "item_name": row.item_name,
            "quantity": required_qty / conversion_factor,
            "conversion_factor": conversion_factor,
            "required_bom_qty": total_qty,
            "stock_uom": row.get("stock_uom"),
            "warehouse": warehouse
            or row.get("source_warehouse")
            or row.get("default_warehouse")
            or item_group_defaults.get("default_warehouse"),
            "safety_stock": row.safety_stock,
            "actual_qty": bin_dict.get("actual_qty", 0),
            "projected_qty": bin_dict.get("projected_qty", 0),
            "ordered_qty": bin_dict.get("ordered_qty", 0),
            "reserved_qty_for_production": bin_dict.get("reserved_qty_for_production", 0),
            "min_order_qty": row["min_order_qty"],
            "material_request_type": row.get("default_material_request_type"),
            "sales_order": sales_order,
            "description": row.get("description"),
            "uom": row.get("purchase_uom") or row.get("stock_uom"),
            "custom_total_stock":total_stock[0].actual_qty if total_stock else 0

        }

def get_total_stock_in_all_warehose(item_code,company):
    warehouse=frappe.db.get_value("Warehouse",{"warehouse_name":"All Warehouses","company":company},"name")
    get_data=frappe.db.sql("""select sum(bin.actual_qty) as actual_qty from
                         `tabBin` bin,`tabWarehouse` wh
                         where wh.parent_warehouse='{warehouse}'
                         and bin.item_code='{item_code}'
                         and bin.warehouse = wh.name""" .format(warehouse=warehouse,item_code=item_code),as_dict=1)
    return get_data



def custom_add_items(self, items):
    refs = {}
    for data in items:
        if not data.pending_qty:
            continue

        item_details = get_item_details(data.item_code, throw=False)
        custom_so_qty = frappe.db.get_value('Sales Order Item', data.name, 'custom_so_qty_')   # Fetch custom_so_qty_ value
        if self.combine_items:
            if item_details.bom_no in refs:
                refs[item_details.bom_no]["so_details"].append(
                    {"sales_order": data.parent, "sales_order_item": data.name, "qty": data.pending_qty, "custom_so_qty": custom_so_qty}
                )
                refs[item_details.bom_no]["qty"] += data.pending_qty
                continue
            else:
                refs[item_details.bom_no] = {
                    "qty": data.pending_qty,
                    "po_item_ref": data.name,
                    "so_details": [],
                }
                refs[item_details.bom_no]["so_details"].append(
                    {"sales_order": data.parent, "sales_order_item": data.name, "qty": data.pending_qty, "custom_so_qty": custom_so_qty}
                )

        pi = self.append(
            "po_items",
            {
                "warehouse": data.warehouse,
                "item_code": data.item_code,
                "description": data.description or item_details.description,
                "stock_uom": item_details and item_details.stock_uom or "",
                "bom_no": data.bom_no or item_details and item_details.bom_no or "",
                "planned_qty": custom_so_qty,
                "pending_qty": data.pending_qty,
                "planned_start_date": now_datetime(),
                "product_bundle_item": data.parent_item,
                "custom_sales_order_qty": data.pending_qty  # Assign custom_so_qty to custom_sales_order_qty
            },
        )
        pi._set_defaults()

        if self.get_items_from == "Sales Order":
            pi.sales_order = data.parent
            pi.sales_order_item = data.name
            pi.description = data.description

        elif self.get_items_from == "Material Request":
            pi.material_request = data.parent
            pi.material_request_item = data.name
            pi.description = data.description

    if refs:
        for po_item in self.po_items:
            po_item.planned_qty = refs[po_item.bom_no]["qty"]
            po_item.pending_qty = refs[po_item.bom_no]["qty"]
            po_item.sales_order = ""
        self.add_pp_ref(refs)



def custom_prepare_data_for_sub_assembly_items(self, row, wo_data):
    
    # Populate wo_data with specified fields from row
    for field in [
        "production_item",
        "item_name",
        "qty",
        "fg_warehouse",
        "description",
        "bom_no",
        "stock_uom",
        "bom_level",
        "schedule_date",
    ]:
        if row.get(field):
            wo_data[field] = row.get(field)
    
    # Assuming self.po_items is a list of items related to the production order
    for d in self.po_items:
        print(d,"+++++++++++++++++++++++++++++++++++")
        wo_data.update(
            {
                "use_multi_level_bom": 0,
                "production_plan": self.name,
                "production_plan_sub_assembly_item": row.name,
                "custom_fg_sales_order": d.sales_order,
            }
        )
