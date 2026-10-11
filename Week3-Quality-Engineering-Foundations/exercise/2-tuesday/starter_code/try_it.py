"""Console runner for the Account Profile and Password Reset service.

Usage: python try_it.py [--build 0.5.0|0.5.1] [--state FILE] <command> [arguments]
Run "python try_it.py help" for the command list. State is kept in a small JSON file
(default: .try_it_state.json in the current folder) so one command can build on the last.
"""
import json
import os
import sys

from account_service import AccountService

HELP = """Commands:
  reset-state                              start again with the two seed accounts
  register EMAIL NAME PASSWORD             create an account
  login EMAIL PASSWORD                     log in
  logout                                   log out
  profile                                  show the logged-in user's profile
  set-name NAME                            change the display name
  set-email EMAIL                          change the email address
  reset-request EMAIL                      ask for a password-reset link
  mailbox EMAIL                            read the simulated emails sent to EMAIL
  reset-complete TOKEN NEW CONFIRM         set a new password using a token
  advance-clock MINUTES                    move the simulated clock forward
Seed accounts: anna@example.com (Anna Lee) and ben@example.com (Ben Carter), both Pass@1234.
Use quotes around values that contain spaces."""

COMMANDS = {  # name: (method, number of arguments)
    "register": ("register", 3), "login": ("login", 2), "logout": ("logout", 0),
    "profile": ("profile", 0), "set-name": ("set_name", 1), "set-email": ("set_email", 1),
    "reset-request": ("request_reset", 1), "mailbox": ("read_mailbox", 1),
    "reset-complete": ("complete_reset", 3),
}


def main(argv):
    build, state = "0.5.0", ".try_it_state.json"
    args = list(argv)
    while args and args[0] in ("--build", "--state") and len(args) >= 2:
        if args[0] == "--build":
            build = args[1]
        else:
            state = args[1]
        args = args[2:]
    if not args or args[0] in ("help", "-h", "--help"):
        print(HELP)
        return 0
    cmd, params = args[0], args[1:]
    if build not in ("0.5.0", "0.5.1"):
        print("Unknown build %s (use 0.5.0 or 0.5.1)" % build)
        return 2
    print("[Project 1 | Account Profile and Password Reset | build %s]" % build)
    if cmd == "reset-state":
        if os.path.exists(state):
            os.remove(state)
        print("State reset. Seed accounts: anna@example.com, ben@example.com (password Pass@1234)")
        return 0
    data = None
    if os.path.exists(state):
        with open(state, encoding="utf-8") as f:
            data = json.load(f)
    svc = AccountService(data, build)
    if cmd == "advance-clock":
        if len(params) != 1 or not params[0].isdigit():
            print("Usage: advance-clock MINUTES (a whole number)")
            return 2
        ok, msg = svc.advance_clock(int(params[0]))
    elif cmd in COMMANDS:
        method, count = COMMANDS[cmd]
        if len(params) != count:
            print("Usage error: %s needs %d argument(s). Run: python try_it.py help" % (cmd, count))
            return 2
        ok, msg = getattr(svc, method)(*params)
    else:
        print("Unknown command: %s. Run: python try_it.py help" % cmd)
        return 2
    with open(state, "w", encoding="utf-8") as f:
        json.dump(svc.to_data(), f)
    print(("OK:   " if ok else "ERROR: ") + msg)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
