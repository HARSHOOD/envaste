frappe.ui.form.on('Quality Inspection', {
    refresh: function(frm) {
        frm.fields_dict.readings.grid.update_docfield_property('specification', 'reqd', 0);
        let hide_fields= ['readings']
        hide_fields.map(field => frm.set_df_property(field, 'hidden', 1));  
        hide_fields.map(field => frm.set_df_property(field, 'reqd', 0));
    
    }
});
