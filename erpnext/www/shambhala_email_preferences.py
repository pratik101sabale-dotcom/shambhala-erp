# License: GNU General Public License v3. See license.txt.

import frappe

from erpnext.shambhala.leads import CONSENT_FIELD

no_cache = 1


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/shambhala-email-preferences"
		raise frappe.Redirect
	context.no_cache = 1
	context.title = "Shambhala Email Preferences"
	user = frappe.db.get_value("User", frappe.session.user, ["user_type", CONSENT_FIELD], as_dict=True)
	context.can_update = user and user.user_type == "Website User"
	context.receive_updates = user and user.get(CONSENT_FIELD)
