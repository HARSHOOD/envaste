frappe.ui.form.on('Stock Entry', {
    before_save: function(frm) {
        if (frm.doc.stock_entry_type === 'Manufacture') {
            var additionalCostsExist = frm.doc.additional_costs && frm.doc.additional_costs.length > 0;
            if (!additionalCostsExist) {
                frappe.msgprint('Please check <b>Additional Costs</b>');
                frm.set_active_tab('additional_costs_section'); 
                frappe.validated = false;
            }
        }
    }
});
