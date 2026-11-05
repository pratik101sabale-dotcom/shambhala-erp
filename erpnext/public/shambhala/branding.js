/* Shambhala ERP product identity. GPL-3.0; see license.txt. */
(() => {
	const title = "Shambhala ERP";
	const apply = () => {
		document.documentElement.dataset.shambhalaBrand = "erp";
		if (window.location.pathname.replace(/\/$/, "") !== "/login") return;
		document.title = `Sign In | ${title}`;
		for (const card of document.querySelectorAll(".for-login, .for-email-login, .for-login-with-email-link")) {
			const heading = card.querySelector(".page-card-head h4");
			const subtitle = card.querySelector(".page-card-subtitle");
			const logo = card.querySelector(".app-logo");
			if (heading) heading.textContent = title;
			if (subtitle) subtitle.textContent = "Sign in to your business workspace.";
			if (logo) logo.alt = title;
		}
	};
	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", apply, { once: true });
	} else {
		apply();
	}
})();
