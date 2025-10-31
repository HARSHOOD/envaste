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



// frappe.ui.form.on("Sales Invoice", {
//     onload(frm) {
//         update_customer_address_display(frm);
//     },
//     customer_address(frm) {
//         update_customer_address_display(frm);
//     },
   
// });


// // Common function to fetch and set address display
// function update_customer_address_display(frm) {
//     if (!frm.doc.customer_address) {
//         frm.set_value("address_display", "");
//         return;
//     }

//     frappe.call({
//         method: "envaste.envaste.api.fetch_customer_address.get_display_address",
//         args: {
//             address_name: frm.doc.customer_address,
//             doc_name: "Sales Invoice"
//         },
//         callback: function(r) {
//             if (r.message) {
//                 setTimeout(() => {
//                     if(frm.doc.address_display!=r.message){
//                             // Temporarily make read-only field editable
//                             frm.fields_dict["address_display"].df.read_only = 0;

//                             frm.set_value("address_display", r.message);
//                             frm.refresh_field("address_display");

//                             // Make it read-only again
//                             frm.fields_dict["address_display"].df.read_only = 1;
//                     }
//                 }, 500);
//             }
//         }
//     });
// }






// function update_customer_address_display(frm) {
//     console.log("Before update:", frm.doc.address_display);
//     console.log("Docstatus:", frm.doc.docstatus);

//     if (!frm.doc.customer_address) {
//         frm.set_value("address_display", "");
//         return;
//     }

//     frappe.call({
//         method: "envaste.envaste.api.fetch_customer_address.get_display_address",
//         args: {
//             address_name: frm.doc.customer_address,
//             doc_name: "Sales Invoice"
//         },
//         callback: function(r) {
//             if (!r.message) return;

//             console.log("Fetched:", r.message);

//             // Update only if Draft (0) or New (__islocal)
//             if (frm.doc.docstatus === 0 || frm.is_new()) {
//                 frm.fields_dict["address_display"].df.read_only = 0;
//                 frm.set_value("address_display", r.message);
//                 frm.refresh_field("address_display");
//                 frm.fields_dict["address_display"].df.read_only = 1;
//                 console.log("After update:", frm.doc.address_display);
//             } else {
//                 console.log("Submitted invoice - skipping update");
//             }
//         }
//     });
// }
