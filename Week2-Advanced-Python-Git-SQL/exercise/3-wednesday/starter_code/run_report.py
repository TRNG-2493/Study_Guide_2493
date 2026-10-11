"""
run_report.py -- reproduce each bug ticket, and (Part B) the place to configure logging.

Usage (from the starter_code folder):
    python run_report.py            # runs every ticket, shows OK / WRONG / CRASH
    python run_report.py 3          # runs ONE ticket and lets a crash show its full traceback
    python -m pdb run_report.py 3   # runs ticket 3 under the debugger
(Windows: use `py` instead of `python` if `python` opens the Microsoft Store.)

You may edit this file. Add your breakpoint() calls to run_stats.py instead.
"""
import sys

import run_stats

DURATIONS = [120, 80, 340, 95, 210, 150]          # ms, in the order the tests ran
RESULTS = [
    {"test": "t1", "suite": "login",  "status": "pass"},
    {"test": "t2", "suite": "login",  "status": "fail"},
    {"test": "t3", "suite": "login",  "status": "pass"},
    {"test": "t4", "suite": "search", "status": "pass"},
]


def ticket_1():
    """BUG-1: median of an even-sized list"""
    return run_stats.median([4, 1, 3, 2])


def ticket_2():
    """BUG-2: top 3 slowest tests"""
    return run_stats.slowest(list(DURATIONS), 3)


def ticket_3():
    """BUG-3: counting outcomes per suite"""
    return run_stats.group_by_suite(RESULTS)


def ticket_4():
    """BUG-4: two separate reports each keep a flaky list"""
    first = run_stats.note_flaky("t2")
    second = run_stats.note_flaky("t9")
    return first, second


def ticket_5():
    """BUG-5: the id for the first report"""
    return run_stats.next_run_id()


def ticket_6():
    """BUG-6: the dashboard summary, 'latest' test duration"""
    run_stats.run_counter = 0
    return run_stats.summarise_run(RESULTS, list(DURATIONS))


def ticket_7():
    """BUG-7: a night where no tests produced a timing"""
    run_stats.run_counter = 0
    return run_stats.summarise_run(RESULTS, [])


TICKETS = {1: ticket_1, 2: ticket_2, 3: ticket_3, 4: ticket_4, 5: ticket_5, 6: ticket_6, 7: ticket_7}


def main(argv):
    # ---- Part B: configure logging HERE (the entry point), not inside run_stats.py ----
    # TODO (Part B): set up console (INFO) + file (DEBUG, run_report.log) handlers.

    if len(argv) > 1:
        number = int(argv[1])
        print(f"BUG-{number}: {TICKETS[number].__doc__}")
        print(TICKETS[number]())          # a crash shows the full traceback on purpose
        return
    for number, func in TICKETS.items():
        try:
            print(f"BUG-{number} ({func.__doc__.strip()}): {func()!r}")
        except Exception as exc:          # demo only: the point is to SEE every ticket
            print(f"BUG-{number} ({func.__doc__.strip()}): CRASH {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main(sys.argv)
