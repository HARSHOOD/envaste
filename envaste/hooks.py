app_name = "envaste"
app_title = "Envaste "
app_publisher = "Ajay Kumar"
app_description = "Envaste Medical Instruments"
app_email = "ajay.kumar@nestorbird.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/envaste/css/envaste.css"
app_include_js = ["envaste.bundle.js"]

# include js, css files in header of web template
# web_include_css = "/assets/envaste/css/envaste.css"
# web_include_js = "/assets/envaste/js/envaste.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "envaste/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}
doctype_js = {
    "Sales Order" : "public/js/sales_order.js",
    "Workstation": "public/js/workstation.js",
    "Stock Entry":"public/js/stock_entry.js",
    "Lot":"public/js/lot_batch.js",
    # "Sales Invoice": "public/js/sales_invoice.js", 
    # "Purchase Invoice":"public/js/purchase_invoice.js",
    # "Purchase Order":  "public/js/purchase_order.js",
    # "Quality Inspection Template":"public/js/custom_qit.js",
    # "Quality Inspection":"public/js/custom_quality_inspection.js"
    
    }

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "envaste/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "envaste.utils.jinja_methods",
# 	"filters": "envaste.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "envaste.install.before_install"
# after_install = "envaste.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "envaste.uninstall.before_uninstall"
# after_uninstall = "envaste.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "envaste.utils.before_app_install"
# after_app_install = "envaste.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "envaste.utils.before_app_uninstall"
# after_app_uninstall = "envaste.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "envaste.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Quotation": {
		"validate": "envaste.envaste.scheduler.scheduler.validate_custom_expiry_date",
		# "on_cancel": "method",
		# "on_trash": "method"
	},
    "Job Card":{
        "before_insert":"envaste.envaste.scheduler.job_card.before_insert",
        "on_submit":["envaste.envaste.scheduler.job_card.update_subsequent_job_cards",
                    "envaste.envaste.scheduler.job_card.update_time_logs"]
        # "on_submit":"envaste.envaste.scheduler.job_card.update_time_logs"
        },
    "Purchase Order": {
            "validate": "envaste.overrides.purchase_order_override.validate_multi_currency"
        }    
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"envaste.tasks.all"
	# ],
	"daily": [
		"envaste.envaste.scheduler.scheduler.send_notification"
	],
	# "hourly": [
	# 	"envaste.tasks.hourly"
	# ],
	# "weekly": [
	# 	"envaste.tasks.weekly"
	# ],
	# "monthly": [
	# 	"envaste.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "envaste.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
"erpnext.stock.get_item_details.get_item_details": "envaste.overrides.custom_get_item_details.custom_get_item_details",
# "erpnext.accounts.utils.get_children" : "envaste.overrides.custom_accounts.custom_get_children",
# "erpnext.accounts.utils.get_account_balances": "envaste.overrides.custom_accounts.get_account_balances"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "envaste.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["envaste.utils.before_request"]
# after_request = ["envaste.utils.after_request"]

# Job Events
# ----------
# before_job = ["envaste.utils.before_job"]
# after_job = ["envaste.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"envaste.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


fixtures = [
    {
        "dt":"Custom Field",
        "filters":[
            [
                "module" , "in",
                [
                    "Envaste"
				]
			]
		]
	},
        {
        "dt":"Property Setter",
        "filters":[
            [
                "module" , "in",
                [
                    "Envaste"
				]
			]
		]
	},
    {
        "dt":"Item Attribute",
        "filters":[
            [
                "name" , "in",
                [
                    "Dimension"
				]
			]
		]
	},
    {
        "dt":"Item Group",
        "filters":[
            [
                "name" , "in",
                [
                    "Production Supply",
                    "Finished Products"
				]
			]
		]
	},
    {
        "dt":"Translation",
        "filters":[
            [
                "name" , "in",
                [
                    "9af925d2d7",
                    "0e6e9ecec2",
                    "7f77eeac4e",
                    "77d1aad441",
                    "c2fd627a8b",
                    "241ab080aa",
                    "afc460d98f",
                    "cf5dcc5c26",
                    "09e486756b"
				]
			]
		]
	},
    {
        "dt":"Quality Inspection Template",
        "filters":[
            [
                "name" , "in",
                [
                    "Balloon Catheters",
                    "Ureteral Access Sheath",
                   
				]
			]
		]
	},
    {
        "dt":"Quality Inspection Parameter",
        "filters":[
            [
                "name" , "in",
                [
                    "Default"
				]
			]
		]
	},
        {
        "dt":"Letter Head",
        "filters":[
            [
                "name" , "in",
                [
                    "Envaste"
				]
			]
		]
	},
    {
        "dt":"Client Script",
        "filters":[
            [
                "name" , "in",
                [
                    "WorkOrder"
				]
			]
		]
	},
    {
        "dt":"Address Template",
        "filters":[
            [
                "name" , "in",
                [
                   "Mauritius"
				]
			]
		]
	},
    {
        "doctype": "Print Format",
        "filters": [
            ["name", "in", ["LHR Rev -03 for FG", "Main LHR Rev-03","LHR Rev- 03 SubAssembley","New LHR Rev- 03 SubAssembley","Delivery Note Packing Slip","PO FORMAT","Order Confirmation PF","Proforma Invoice Print Format","Credit Note PF","Sales Invoice PF" ]]
        ]
    }

] 



