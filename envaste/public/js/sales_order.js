frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        frm.fields_dict.items.grid.update_docfield_property('delivery_date', 'hidden', 1);
        frm.add_custom_button(__('Calculate'), function() {
            calculate_quantity(frm);
        });

    }
});






frappe.ui.form.on('Sales Order Item', {
    item_code: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        console.log(child,"++++++++++++=")
        frappe.model.set_value(cdt, cdn, 'qty', 0);
    }
});







var isQtyCalculated = false;

function calculate_quantity(frm) {
    // if (isQtyCalculated) {
    //     frappe.msgprint(__('Quantity is already calculated'));
    //     return;
    // }

    // Get the planned percentage
    var plannedPercentage = parseFloat(frm.doc.custom_planned_percentage) || 0;

    // Check if planned percentage is provided
    if (!plannedPercentage) {
        frappe.msgprint(__('Planned percentage is required for calculation'));
        return;
    }

    // Function to calculate the adjusted quantity for an item
    function calculateItemQuantity(item) {
        // Get the original quantity of the item
        var originalQuantity = item.qty;

        // Get the item group
        var itemGroup = item.item_group;

        // Check if item group is defined
        if (!itemGroup) {
            frappe.msgprint(__('Item group is not defined for item: {0}', [item.item_code]));
            return;
        }

        // Get the custom number of samples for the item group
        getCustomSamples(item, function(customSamples) {
            // Check if customSamples is defined
            if (customSamples === null) {
                frappe.msgprint(__('Custom number of samples is not defined for item group: {0}', [itemGroup]));
                return;
            }

            // Convert customSamples to a number
            customSamples = parseFloat(customSamples);

            // Calculate the percentage increase based on the planned percentage
            var percentageIncrease = originalQuantity * (plannedPercentage / 100);

            // Calculate the adjusted quantity for the item
            var adjustedQuantity = originalQuantity + percentageIncrease + customSamples;

            // Update the qty field with the calculated quantity
            frappe.model.set_value(item.doctype, item.name, 'custom_so_qty_', Math.ceil(adjustedQuantity));
            // Set the original quantity in a custom field for reference
            // frappe.model.set_value(item.doctype, item.name, 'custom_so_qty_', originalQuantity);
        });
    }

    // Iterate through each item and calculate the adjusted quantity
    frm.doc.items.forEach(function(item) {
        calculateItemQuantity(item);
    });

    // Refresh the items field after all calculations are done
    frm.refresh_field('items');
    isQtyCalculated = true;
}

function getCustomSamples(item, callback) {
    if (item.item_group) {
        frappe.db.get_value('Item Group', item.item_group, 'custom_number_of_samples_of_quality_control', function(r) {
            var customSamples = r.custom_number_of_samples_of_quality_control;
            console.log(customSamples,"************")
            console.log(customSamples)
            callback(customSamples);
        });
    } else {
        // If item group is not defined, return null
        callback(null);
    }
}


function parsePlannedPercentage(percentageStr) {
    var match = percentageStr.match(/(\d+(\.\d+)?)%\+(\d+)/);
    if (match && match.length >= 4) {
        var basePercentage = parseFloat(match[1]);
        var additionalQuantity = parseInt(match[3]);
        return [basePercentage, additionalQuantity];
    } else {
        return null;
    }
}



// --------------------- done by harsh rajput ----------------------
// console.log("fomr",frm.doc.customer_address)
// console.log("form",frm.doc.address_display)

frappe.ui.form.on("Sales Order", {

    // Trigger when form loads
    onload: function(frm) {
        update_customer_address_display(frm);
    },

    // Trigger when customer_address changes
    customer_address: function(frm) {
        update_customer_address_display(frm);
    }
});

// Common function to fetch and set address display
function update_customer_address_display(frm) {
    if (!frm.doc.customer_address) {
        frm.set_value("address_display", "");
        return;
    }

    frappe.call({
        method: "envaste.envaste.api.fetch_customer_address.get_display_address",
        args: {
            address_name: frm.doc.customer_address,
            doc_name: "Sales Invoice"
        },
        callback: function(r) {
            if (r.message) {
                setTimeout(() => {
                    // Temporarily make read-only field editable
                    frm.fields_dict["address_display"].df.read_only = 0;

                    frm.set_value("address_display", r.message);
                    frm.refresh_field("address_display");

                    // Make it read-only again
                    frm.fields_dict["address_display"].df.read_only = 1;
                }, 500);
            }
        }
    });
}

// function to filter expense account in in expense_account filter
frappe.ui.form.on('Sales Order', {
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
