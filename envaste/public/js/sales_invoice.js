// function to filter expense account in in expense_account filter
frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        frm.fields_dict['items'].grid.get_field('expense_account').get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    "root_type": "Expense",
                    "is_group": 0
                }
            };
        };
        frm.fields_dict['items'].grid.get_field('income_account').get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    "root_type": "Income",
                    "is_group": 0
                }
            };
        };
    }   
});



frappe.ui.form.on("Sales Invoice", { 
    onload: function(frm) {
        if (!frm.doc.customer_address) {
            frm.set_value("address_display", "");
            return;
        }

        frappe.call({
            method: "envaste.envaste.api.fetch_customer_address.get_display_address",
            args: {
                address_name: frm.doc.customer_address
            },
            callback: function(r) {
                if (r.message) {
                    // Wait a bit for ERPNext's own script to run first
                    setTimeout(() => {
                        // Temporarily make read-only field editable
                        frm.fields_dict["address_display"].df.read_only = 0;
                        
                        frm.set_value("address_display", r.message);

                        // Refresh field to show updated value
                        frm.refresh_field("address_display");

                        // Make it read-only again
                        frm.fields_dict["address_display"].df.read_only = 1;
                    }, 500);
                }
            }
        });
    }
});


