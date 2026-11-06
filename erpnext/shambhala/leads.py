# License: GNU General Public License v3. See license.txt.

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.utils import get_site_path
from frappe.utils.synchronization import filelock
from frappe.utils.xlsxutils import make_xlsx, xlsxwriter

CONSENT_FIELD = "shambhala_email_updates_opt_in"
WORKBOOK_NAME = "Shambhala-ERP-Leads.xlsx"


def install_fields():
	"""Keep the preference on each account, outside the public application source."""
	create_custom_fields({
		"User": [
			{
				"fieldname": CONSENT_FIELD,
				"label": "Shambhala Email Updates",
				"fieldtype": "Check",
				"default": "0",
				"insert_after": "email",
				"hidden": 1,
				"read_only": 1,
				"no_copy": 1,
			}
		]
	})


def lead_emails():
	"""One email per opted-in, active portal account that has signed in."""
	emails = frappe.get_all(
		"User",
		filters={
			"user_type": "Website User",
			"enabled": 1,
			"last_login": ["is", "set"],
			CONSENT_FIELD: 1,
		},
		pluck="email",
	)
	return sorted({email.strip().lower() for email in emails if email and email.strip()})


def refresh_workbook():
	"""Replace the private workbook atomically so readers always see a complete file."""
	directory = Path(get_site_path("private", "shambhala"))
	directory.mkdir(mode=0o700, parents=True, exist_ok=True)
	destination = directory / WORKBOOK_NAME
	with filelock("shambhala-lead-workbook", timeout=3):
		rows = [["Email"]] + [[email] for email in lead_emails()]
		with NamedTemporaryFile(dir=directory, suffix=".xlsx", delete=False) as tmp:
			staged = Path(tmp.name)
		try:
			with xlsxwriter.Workbook(staged, {
				"constant_memory": True,
				"strings_to_formulas": False,
				"strings_to_urls": False,
			}) as workbook:
				make_xlsx(rows, "Leads", wb=workbook, column_widths=[48])
				workbook.get_worksheet_by_name("Leads").freeze_panes(1, 0)
			os.replace(staged, destination)
		finally:
			staged.unlink(missing_ok=True)
	return destination


def refresh_after_commit():
	"""Keep login available if a concurrent workbook refresh is busy."""
	try:
		refresh_workbook()
	except Exception as error:
		frappe.logger("shambhala_leads").warning("Lead workbook refresh failed: %s", type(error).__name__)


def on_session_creation(login_manager):
	if not frappe.db.has_column("User", CONSENT_FIELD):
		return
	if frappe.db.exists("User", {
		"name": login_manager.user,
		"user_type": "Website User",
		"enabled": 1,
		CONSENT_FIELD: 1,
	}):
		frappe.db.after_commit.add(refresh_after_commit)


@frappe.whitelist(allow_guest=True, methods=["POST"])
def sign_up(email: str, full_name: str, redirect_to: str = ""):
	"""Use Frappe's account creation and welcome email for an opted-in signup."""
	from frappe.core.doctype.user.user import sign_up as native_sign_up

	email = email.strip().lower()
	result = native_sign_up(email, full_name, redirect_to)
	if result[0] in (1, 2):
		frappe.db.set_value("User", email, CONSENT_FIELD, 1, update_modified=False)
	return result


@frappe.whitelist(methods=["POST"])
def save_preference(receive_updates: bool):
	user = frappe.session.user
	if frappe.db.get_value("User", user, "user_type") != "Website User":
		frappe.throw(_("This preference is available to portal accounts."), frappe.PermissionError)
	frappe.db.set_value("User", user, CONSENT_FIELD, int(receive_updates), update_modified=False)
	frappe.db.after_commit.add(refresh_after_commit)
	return {"receive_updates": receive_updates}


@frappe.whitelist(methods=["GET"])
def download_workbook():
	frappe.only_for("System Manager")
	path = refresh_workbook()
	frappe.response.update(filename=WORKBOOK_NAME, filecontent=path.read_bytes(), type="download")


def enable_self_signup():
	"""Enable Frappe's portal signup once welcome emails can be sent."""
	frappe.only_for("System Manager")
	if not frappe.db.exists("Email Account", {"enable_outgoing": 1, "default_outgoing": 1}):
		frappe.throw(_("Set up a default outgoing Email Account before enabling signup."))
	if frappe.db.get_single_value("Portal Settings", "default_role"):
		frappe.throw(_("Clear the default signup role to create portal-only accounts."))
	settings = frappe.get_single("Website Settings")
	settings.disable_signup = 0
	settings.save()
	return {"self_signup_enabled": True}
