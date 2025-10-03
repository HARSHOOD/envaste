frappe.ui.form.on('Batch', {
    refresh: function(frm) {
        if (frm.doc.batch_qty) {
            frm.set_value('custom_produced_quantity', frm.doc.batch_qty);
        }
    },
    batch_qty: function(frm) {
        frm.set_value('custom_produced_quantity', frm.doc.batch_qty);
    }
});
