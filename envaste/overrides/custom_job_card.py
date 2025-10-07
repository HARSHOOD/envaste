import datetime
import json
from collections import OrderedDict

import frappe
from frappe import _, bold
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.query_builder import Criterion
from frappe.query_builder.functions import IfNull, Max, Min
from frappe.utils import (
	add_days,
	add_to_date,
	cint,
	flt,
	get_datetime,
	get_link_to_form,
	get_time,
	getdate,
	time_diff,
	time_diff_in_hours,
	time_diff_in_seconds,
)

    
    
def custom_validate_job_card(self):

    if self.work_order and frappe.get_cached_value("Work Order", self.work_order, "status") == "Stopped":
        frappe.throw(
            _("Transaction not allowed against stopped Work Order {0}").format(
                get_link_to_form("Work Order", self.work_order)
            )
        )

    if not self.time_logs:
        frappe.throw(
            _("Time logs are required for {0} {1}").format(
                bold("Job Card"), get_link_to_form("Job Card", self.name)
            )
        )

    precision = self.precision("total_completed_qty")
    total_completed_qty = flt(
        flt(self.total_completed_qty, precision) + flt(self.process_loss_qty, precision)
    )

    if self.for_quantity and flt(total_completed_qty, precision) != flt(self.for_quantity, precision):
        total_completed_qty_label = bold(_("Total Completed Qty"))
        qty_to_manufacture = bold(_("Qty to Manufacture"))

        # frappe.throw(
        # 	_("The {0} ({1}) must be equal to {2} ({3})").format(
        # 		total_completed_qty_label,
        # 		bold(flt(total_completed_qty, precision)),
        # 		qty_to_manufacture,
        # 		bold(self.for_quantity),
        # 	)
        # )

def custom_validate_sequence_id(self):

    if self.is_corrective_job_card:
        return

    if not (self.work_order and self.sequence_id):
        return

    current_operation_qty = 0.0
    data = self.get_current_operation_data()
    if data and len(data) > 0:
        current_operation_qty = flt(data[0].completed_qty)

    current_operation_qty += flt(self.total_completed_qty)

    data = frappe.get_all(
        "Work Order Operation",
        fields=["operation", "status", "completed_qty", "sequence_id"],
        filters={"docstatus": 1, "parent": self.work_order, "sequence_id": ("<", self.sequence_id)},
        order_by="sequence_id, idx",
    )

    message = "Job Card {}: As per the sequence of the operations in the work order {}".format(
        bold(self.name), bold(get_link_to_form("Work Order", self.work_order))
    )

    for row in data:
        if row.status != "Completed" and row.completed_qty < current_operation_qty:
            pass
            # frappe.throw(
            #     _("{0}, complete the operation {1} before the operation {2}.").format(
            #         message, bold(row.operation), bold(self.operation)
            #     ),
            #     # OperationSequenceError,
            # )

        if row.completed_qty < current_operation_qty:
            pass
            # msg = f"""The completed quantity {bold(current_operation_qty)}
            # 	of an operation {bold(self.operation)} cannot be greater
            # 	than the completed quantity {bold(row.completed_qty)}
            # 	of a previous operation
            # 	{bold(row.operation)}.
            # """

            # frappe.throw(_(msg))