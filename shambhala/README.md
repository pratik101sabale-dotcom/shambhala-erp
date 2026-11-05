# Shambhala ERP

This repository keeps ERPNext's application identifier and adds the Shambhala ERP product identity through application hooks and supported Frappe settings.

## Existing ERPNext site

After installing this checkout as the `erpnext` app in your bench, run:

```sh
bench --site YOUR_SITE execute erpnext.shambhala.branding.apply_branding
bench --site YOUR_SITE clear-cache
```

Restart the bench processes and reload the browser. New installations and migrations also apply the branding automatically.

The customization changes the application title, icon, login heading, favicon, and website branding. It does not rename the site's Company records or alter accounting data.

## Development

Use a Frappe version-16 bench with Python 3.14, Node.js 24, MariaDB 11.8, and Redis. The branding code is in `erpnext/shambhala/branding.py`, the hooks are in `erpnext/hooks.py`, and the browser assets are in `erpnext/public/shambhala`.

The laptop deployment uses Ubuntu 24.04 under WSL 2. Its launcher starts the local development services before opening the application.

For an existing bench installation at `/opt/erpnext-dev/frappe-bench` owned by the Linux user `frappe`, the development service examples are in `shambhala/linux`. Install the service with administrator access inside that Linux environment and install the accompanying `run-development.sh` and `keep-alive.sh` files in `/opt/erpnext-dev`. The Windows launchers in `shambhala/windows` expect that service and the `Ubuntu-24.04` WSL distribution. They open the local application in a dedicated browser window.

The source repository is [pratik101sabale-dotcom/shambhala-erp](https://github.com/pratik101sabale-dotcom/shambhala-erp), on its `shambhala` branch.

## Attribution

ERPNext is developed by Frappe Technologies and contributors and is licensed under GPL v3. Frappe Framework is licensed separately under MIT. All upstream copyright notices and licenses remain in place.

This repository contains application source only. Site databases, login passwords, backups, and private configuration must stay outside the repository.
