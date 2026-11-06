/* Optional email consent for the standard Frappe signup form. */
(() => {
	function addEmailPreference() {
		const form = document.querySelector(".form-signup");
		const formBody = form?.querySelector(".page-card-body");
		if (!formBody || !window.login?.call || form.elements.shambhala_email_opt_in) return;

		const consent = document.createElement("input");
		consent.type = "checkbox";
		consent.name = "shambhala_email_opt_in";
		const label = document.createElement("label");
		label.append(consent, document.createTextNode(` ${__("Email me Shambhala updates")}`));
		const help = document.createElement("p");
		help.id = "shambhala-email-consent-help";
		help.className = "text-muted small mb-0";
		help.textContent = __("Optional. After you sign in, your email goes into the site owner's lead list for news and follow-up.") + " ";
		const settings = document.createElement("a");
		settings.href = "/shambhala-email-preferences";
		settings.textContent = __("Change your email preference anytime.");
		help.append(settings);
		consent.setAttribute("aria-describedby", help.id);
		const preference = document.createElement("div");
		preference.append(label, help);
		formBody.append(preference);

		form.addEventListener("submit", (event) => {
			if (!consent.checked) return;
			event.preventDefault();
			event.stopImmediatePropagation();
			const email = form.querySelector("#signup_email");
			const name = form.querySelector("#signup_fullname");
			if (!form.reportValidity() || !name.value.trim()) return;
			window.login.call({
				cmd: "erpnext.shambhala.leads.sign_up",
				email: email.value.trim(),
				full_name: frappe.utils.xss_sanitise(name.value.trim()),
				redirect_to: frappe.utils.sanitise_redirect(frappe.utils.get_url_arg("redirect-to")) || "",
			});
		}, { capture: true });
	}
	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", addEmailPreference, { once: true });
	} else {
		addEmailPreference();
	}
})();
