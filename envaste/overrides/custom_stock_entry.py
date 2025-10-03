import frappe
from frappe import _
from frappe.utils import (
    cint,
    comma_or,
    cstr,
    flt,
    format_time,
    formatdate,
    get_link_to_form,
    getdate,
    nowdate,
)
from erpnext.stock.doctype.stock_entry import stock_entry
from erpnext.stock.doctype.item.item import get_item_defaults


def custom_set_process_loss_qty(self):
    if self.purpose not in ("Manufacture", "Repack"):
        return

    precision = self.precision("process_loss_qty")
    if self.work_order:
        data = frappe.get_all(
            "Work Order Operation",
            filters={"parent": self.work_order},
            fields=["sum(process_loss_qty) as process_loss_qty"]
        )

        if data and data[0].process_loss_qty is not None:
            process_loss_qty = data[0].process_loss_qty
            if flt(self.process_loss_qty, precision) != flt(process_loss_qty, precision):
                self.process_loss_qty = flt(process_loss_qty, precision)
                frappe.msgprint(
                    _("The Process Loss Qty has reset as per job cards Process Loss Qty"), alert=True
                )

    if not self.process_loss_percentage and not self.process_loss_qty:
        self.process_loss_percentage = frappe.get_cached_value(
            "BOM", self.bom_no, "process_loss_percentage"
        )

    if self.process_loss_percentage and not self.process_loss_qty:
        self.process_loss_qty = flt(
            (flt(self.fg_completed_qty) * flt(self.process_loss_percentage)) / 100
        )
    elif self.process_loss_qty and not self.process_loss_percentage:
        self.process_loss_percentage = flt(
            (flt(self.process_loss_qty) / flt(self.fg_completed_qty)) * 100
        )


def custom_load_items_from_bom(self):
    if self.work_order:
        item_code = self.pro_doc.production_item
        to_warehouse = self.pro_doc.fg_warehouse
    else:
        item_code = frappe.db.get_value("BOM", self.bom_no, "item")
        to_warehouse = self.to_warehouse

    item = get_item_defaults(item_code, self.company)

    if not self.work_order and not to_warehouse:
        to_warehouse = item.get("default_warehouse")

    args = {
        "to_warehouse": to_warehouse,
        "from_warehouse": "",
        "qty": flt(self.fg_completed_qty) - flt(self.process_loss_qty),
        "item_name": item.item_name,
        "description": item.description,
        "stock_uom": item.stock_uom,
        "expense_account": item.get("expense_account"),
        "cost_center": item.get("buying_cost_center"),
        "is_finished_item": 1,
    }

    if (
        self.work_order
        and self.pro_doc.has_batch_no
        and not self.pro_doc.has_serial_no
        and cint(
            frappe.db.get_single_value(
                "Manufacturing Settings", "make_serial_no_batch_from_work_order", cache=True
            )
        )
    ):
        self.set_batchwise_finished_goods(args, item)
        for item_data in self.items:
            if item_data.serial_and_batch_bundle:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                frappe.db.set_value(
                    "Serial and Batch Entry",
                    {"parenttype": "Serial and Batch Bundle", "parent": item_data.serial_and_batch_bundle},
                    {"qty": item_data.qty}
                )
                all_list_serial_bundle = frappe.get_all(
                    "Serial and Batch Entry",
                    {"parenttype": "Serial and Batch Bundle", "parent": item_data.serial_and_batch_bundle},
                    ["qty"],
                    pluck="qty"
                )
                frappe.db.set_value(
                    "Serial and Batch Bundle", item_data.serial_and_batch_bundle, "total_qty", flt(sum(all_list_serial_bundle))
                )
    else:
        self.add_finished_goods(args, item)
