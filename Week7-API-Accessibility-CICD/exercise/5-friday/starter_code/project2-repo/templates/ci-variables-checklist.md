# CI/CD variables checklist

Settings > CI/CD > Variables. NEVER commit values. Fill the table as you create each one.

| Key | Purpose | Masked | Protected | Environment scope | Created? |
|---|---|---|---|---|---|
| BASE_URL | API base URL the tests call | no (not secret) | no | * | [ ] |
| API_USER | test user | no | no | * | [ ] |
| API_PASSWORD | test user password | YES | decide + justify | * | [ ] |
| API_ADMIN_USER | admin user | no | no | * | [ ] |
| API_ADMIN_PASSWORD | admin password | YES | decide + justify | * | [ ] |

Masking rules to check before saving: value is a single line, at least 8 characters, and only characters from the allowed set (letters, digits and `+ _ - = : @ . ~ /`; no spaces). If the value does not fit, GitLab refuses to mask it.

Protected variables exist only on protected branches/tags. A merge-request pipeline from an unprotected branch will NOT see them. Write down which jobs need which variables and what the others do instead.

Proof checklist (tick when verified, do not paste values):
- [ ] a job fails with a clear message when a required variable is missing
- [ ] no job log shows a password in clear text
- [ ] `git grep -n "password\|token"` finds no real secret in the repo
