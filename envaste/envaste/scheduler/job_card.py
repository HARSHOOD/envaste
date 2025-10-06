import frappe

def update_time_logs(doc, method):
    if doc.docstatus == 1:  
        for time_log in doc.get('time_logs'):
            time_log.custom_good = doc.total_completed_qty
            # time_log.custom_scrap = doc.process_loss_qty
            time_log.save()
            # doc.append('scrap_items', {
            #     'item_code': doc.production_item,
            #     'item_name':frappe.db.get_value('Item', doc.production_item, 'item_name'),
            #     'stock_qty': doc.process_loss_qty
            # }) 


def before_insert(doc, method):
    if doc.workstation:
        workstation = frappe.get_doc('Workstation', doc.workstation)
        doc.custom_tooling = []
        doc.custom_equipment_table = []

        for tooling in workstation.custom_tooling:
            doc.append('custom_tooling', {
                'tooling_name_or_code': tooling.tooling_name_or_code
            })
        for equipment in workstation.custom_equipment:
            doc.append('custom_equipment_table', {
                'equipment': equipment.equipment
            })


def update_subsequent_job_cards(doc, method):
    work_order = doc.work_order
    initial_completed_qty = doc.total_completed_qty
    job_cards = frappe.get_all('Job Card', filters={'work_order': work_order}, order_by='creation')
    update_next = False
    for card in job_cards:
        if update_next:
            job_card_doc = frappe.get_doc('Job Card', card.name)
            job_card_doc.for_quantity = initial_completed_qty  
            job_card_doc.save()
        if card.name == doc.name:
            update_next = True

    return True
