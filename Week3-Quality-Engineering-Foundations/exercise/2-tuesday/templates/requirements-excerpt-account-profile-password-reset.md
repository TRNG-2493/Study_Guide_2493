# Requirements excerpt: Account Profile and Password Reset (draft v0.1)

Project 1 - QE Foundations. This is a **draft** written by the Product Owner before any review. Treat it like a real document: it may contain problems. Your job in Part 1 is to find them.

Background: Registration and login (Monday and Tuesday's demo) already exist. This release adds a profile page and a password reset. Registered test users: `anna@example.com` and `ben@example.com`.

| ID | Requirement (draft text) | Priority |
|---|---|---|
| REQ-PROF-01 | A logged-in user shall be able to view their profile page, which shows their name and email address. | Must |
| REQ-PROF-02 | A logged-in user shall be able to change their display name. The name must be a reasonable length. | Must |
| REQ-PROF-03 | A logged-in user shall be able to change their email address. The new address must be valid and must not already belong to another account. | Must |
| REQ-PROF-04 | The system shall save profile changes without noticeable delay and tell the user that the change was made. | Should |
| REQ-PROF-05 | Email addresses are not case-sensitive. | Must |
| REQ-RESET-01 | A user who has forgotten their password shall be able to request a password reset by entering their email address. The user can request a reset as many times as needed. | Must |
| REQ-RESET-02 | The system shall find the account using the exact email address as typed by the user. | Must |
| REQ-RESET-03 | If the email address belongs to a registered account, the system shall send a reset link that contains a token. If it does not belong to a registered account, the system shall tell the user that the email address was not found. | Must |
| REQ-RESET-04 | The system shall not reveal whether an email address is registered. | Must |
| REQ-RESET-05 | The reset link shall expire soon after it is sent and can be used only once. | Must |
| REQ-RESET-06 | The user shall enter the new password twice, as "new password" and "confirm password". | Must |
| REQ-RESET-07 | The new password must be strong. | Must |
| REQ-RESET-08 | After the reset, the user shall be able to log in with the new password. | Must |
| REQ-RESET-09 | The reset process shall be user-friendly and safe. | Should |

Priorities use MoSCoW: Must, Should, Could.
