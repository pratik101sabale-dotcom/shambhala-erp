# License: GNU General Public License v3. See license.txt.

import frappe

APP_TITLE = "Shambhala ERP"
APP_LOGO = "/assets/erpnext/shambhala/logo.svg"


def apply_branding():
	"""Apply the product identity using Frappe's supported settings."""
	website = frappe.get_single("Website Settings")
	website.update(
		{
			"app_name": APP_TITLE,
			"title_prefix": APP_TITLE,
			"app_logo": APP_LOGO,
			"favicon": APP_LOGO,
			"splash_image": APP_LOGO,
			"brand_html": '<span class="shambhala-brand-name">Shambhala ERP</span>',
		}
	)
	website.save(ignore_permissions=True)

	system = frappe.get_single("System Settings")
	system.app_name = APP_TITLE
	system.save(ignore_permissions=True)

	navbar = frappe.get_single("Navbar Settings")
	navbar.app_logo = APP_LOGO
	navbar.save(ignore_permissions=True)

	frappe.clear_cache()
	return {"app_name": APP_TITLE, "logo": APP_LOGO}
