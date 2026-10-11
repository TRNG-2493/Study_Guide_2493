"""Run one test case by hand against the target.

Examples (run from this folder):
  python run_cases.py reset
  python run_cases.py register --email a@b.com --username bob --password 'Abcdef1!' --confirm 'Abcdef1!' --terms yes
  python run_cases.py login --id a@b.com --password 'Abcdef1!' --remember yes
  python run_cases.py mask --password 'Abcdef1!' --visible no
  python run_cases.py show

State (registered users, failed-attempt counters) is kept in .qea_state.json,
so several commands in a row behave like one session. Use 'reset' to start clean.
"""
import argparse
import os
import sys

from registration_login import AuthService, mask_password

STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".qea_state.json")


def yes(v):
    return str(v).lower() in ("yes", "y", "true", "1")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("reset", help="delete all users and counters")
    sub.add_parser("show", help="print how many users are registered")
    r = sub.add_parser("register")
    r.add_argument("--email", default="")
    r.add_argument("--username", default="")
    r.add_argument("--password", default="")
    r.add_argument("--confirm", default="")
    r.add_argument("--terms", default="no", help="yes or no")
    lg = sub.add_parser("login")
    lg.add_argument("--id", default="", help="email or username")
    lg.add_argument("--password", default="")
    lg.add_argument("--remember", default="no", help="yes or no")
    m = sub.add_parser("mask")
    m.add_argument("--password", default="")
    m.add_argument("--visible", default="no", help="yes or no")
    a = p.parse_args(argv)

    if a.cmd == "reset":
        if os.path.exists(STATE):
            os.remove(STATE)
        print("State cleared. Users registered: 0")
        return 0
    svc = AuthService(STATE)
    if a.cmd == "register":
        res = svc.register(a.email, a.username, a.password, a.confirm, yes(a.terms))
    elif a.cmd == "login":
        res = svc.login(a.id, a.password, yes(a.remember))
    elif a.cmd == "mask":
        print("Displayed value: %r" % mask_password(a.password, yes(a.visible)))
        return 0
    else:
        res = None
    if res is not None:
        for k, v in res.items():
            print("%-9s: %s" % (k, v))
    print("Users registered: %d" % svc.user_count())
    return 0


if __name__ == "__main__":
    sys.exit(main())
