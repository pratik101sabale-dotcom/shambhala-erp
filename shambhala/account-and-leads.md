# Self-service accounts and email leads

Shambhala ERP uses Frappe's existing account and password reset flow. A new visitor registers with an email address and follows the welcome link to choose a password. The account is a Website User. System roles are assigned separately by a site administrator.

## Enable registration

1. Configure and verify a **default outgoing Email Account** in ERP. Set the site's canonical URL to the HTTPS address users can actually reach so welcome links go to the correct site.
2. Keep the default role in **Portal Settings** empty for portal-only registration.
3. Run `bench --site YOUR_SITE execute erpnext.shambhala.leads.enable_self_signup` as an administrator, or enable signup in **Website Settings** after the two checks above.
4. Test registration and password setup with an address you control. Each user can manage their choice at `/shambhala-email-preferences`.

Custom fields are added on install and migrate. To apply them to an existing checkout without a full migration, run `bench --site YOUR_SITE execute erpnext.shambhala.leads.install_fields`, clear the site cache, and restart the bench processes.

## Lead workbook

On signup the visitor can opt in to Shambhala updates. After a successful login, the private workbook is rebuilt with one **Email** column and a single row per opted-in, enabled portal account. Changing the preference refreshes the workbook. A System Manager can download the current version at `/api/method/erpnext.shambhala.leads.download_workbook`.

The workbook is stored as `private/shambhala/Shambhala-ERP-Leads.xlsx` inside the site's folder. It is a generated view of account preferences. Store site data, mail credentials and exports outside Git.

## Reuse in future projects

1. Use each application's normal authentication and password setup. Start new accounts with the least access they need.
2. Explain the purpose beside an unchecked email opt-in and offer an account setting to withdraw it.
3. Export the verified account email after successful authentication, once per address. Rebuild the export from current preferences, including after a withdrawal.
4. Keep the workbook private to the owner or an explicitly authorized administrator. Use plain text Excel cells and an atomic write when refreshing the file.

For another Frappe application, use the same signup wrapper and `on_session_creation` hook pattern. For other stacks, connect the export to their authenticated session and account preferences.
