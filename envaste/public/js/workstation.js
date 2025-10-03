frappe.ui.form.on("Workstation", {
    refresh(frm) {
        cur_frm.fields_dict["custom_production_supply"].grid.get_field("production").get_query = function (doc, cdt, cdn) {
            return {
                filters: {
                    "item_group": "Production Supply"
                }

            };
        }
    },
})