# Workflow: software project

**Lead:** software-engineer · **Factory:** `factories/software.md` · **Ends with:** a `merge` approval

| # | Step | Who | Reviewer | Output |
|---|---|---|---|---|
| 1 | Architecture and plan | `engineering-software-architect`, `engineering-backend-architect` | | Plan in the job folder |
| 2 | Build in small steps on a branch | software-engineer with `engineering-senior-developer` | `engineering-code-reviewer` | Branch, tests |
| 3 | Tests | `testing-test-automation-engineer`, `testing-api-tester` | | Passing test run |
| 4 | Security | `security-appsec-engineer`, `security-secrets-credential-engineer` | | No secrets, no known holes |
| 5 | Docs | `engineering-technical-writer` | | README for the client |
| 6 | Approval queue, type `merge` | software-engineer | | Queue item |
