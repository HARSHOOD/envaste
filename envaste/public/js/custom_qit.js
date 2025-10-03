
frappe.ui.form.on('Quality Inspection Template', {
    refresh: function(frm) {
        frm.fields_dict.item_quality_inspection_parameter.grid.update_docfield_property('specification', 'reqd', 0);
        let hide_fields= ['item_quality_inspection_parameter']
        hide_fields.map(field => frm.set_df_property(field, 'hidden', 1));  
        hide_fields.map(field => frm.set_df_property(field, 'reqd', 0));
    
    }
});