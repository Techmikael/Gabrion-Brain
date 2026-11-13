# Playbook: Client onboarding

**Owner:** finance-admin (contract and payment) then chief-of-staff (kick-off) · **Client journey:** step 5 · **Approval:** the proposal was already approved; any change to price or terms needs a new one

1. **Contract.** Prepare the contract from the approved proposal plus the data processing agreement (DPA). Send for e-signature.
2. **Deposit.** On signature, raise the deposit invoice at the signed price (`memory/finance/invoices.csv`). Work starts when it is paid.
3. **Vault.** Create `clients/<slug>/` from `clients/_template/`. Create a password-manager vault named `Client – <name>`; the client shares logins there, never by email or chat.
4. **CRM and board.** Lead stage → `won`. Chief of Staff creates the build tasks from the factory, with owners and due dates.
5. **Kick-off email** (founder sends): what happens next, what we need from them (intake form, logins via the vault link), timeline, who to contact.
6. **Intake.** Client completes the intake form; the builder agent checks it is complete within 1 working day.
7. **Managed clients:** set the monthly review date and the direct debit or card subscription.
