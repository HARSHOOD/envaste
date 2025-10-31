// // function to filter expense account in in expense_account filter
// frappe.ui.form.on('Purchase Invoice', {
//     refresh: function(frm) {
//         frm.fields_dict['items'].grid.get_field('expense_account').get_query = function(doc, cdt, cdn) {
//             return {
//                 filters: {
//                     "root_type": "Expense",
//                     "is_group": 0
//                 }
//             };
//         };
//         frm.fields_dict['items'].grid.get_field('income_account').get_query = function(doc, cdt, cdn) {
//             return {
//                 filters: {
//                     "root_type": "Income",
//                     "is_group": 0
//                 }
//             };
//         };
//     }   
// });

// frappe.ui.form.on("Purchase Invoice", {

//     // Trigger when form is loaded
//     onload: function(frm) {
//         update_supplier_address_display(frm);
//     },

//     // Trigger when supplier_address field changes
//     supplier_address: function(frm) {
//         update_supplier_address_display(frm);
//     }
// });

// // Common function to fetch and set address display
// function update_supplier_address_display(frm) {
//     if (!frm.doc.supplier_address) {
//         console.log("No supplier_address, clearing address_display");
//         frm.set_value("address_display", "");
//         return;
//     }

//     console.log("Fetching address display for:", frm.doc.supplier_address);

//     frappe.call({
//         method: "envaste.envaste.api.fetch_customer_address.get_display_address",
//         args: {
//             address_name: frm.doc.supplier_address,
//             doc_name: "Supplier"
//         },
//         callback: function(r) {
//             if (r.message) {
//                 // Wait a bit for ERPNext's own scripts to finish
//                 setTimeout(() => {
//                     // Temporarily make read-only field editable
//                     frm.fields_dict["address_display"].df.read_only = 0;

//                     frm.set_value("address_display", r.message);
//                     frm.refresh_field("address_display");

//                     // Make it read-only again
//                     frm.fields_dict["address_display"].df.read_only = 1;
//                 }, 500);
//             }
//         }
//     });
// }


