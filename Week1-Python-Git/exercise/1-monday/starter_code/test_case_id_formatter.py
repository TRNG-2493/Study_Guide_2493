# Test-Case ID Formatter - Day 1 (Monday) exercise, starter file
#
# Goal: ask for a few details about ONE test case and print a tidy summary.
# Work through the README parts in order. Replace each TODO with your own code,
# then delete the TODO comment. Commit after each part (see the README).
#
# Only use what you learned today: variables, input(), int(), str methods,
# round(), comparison operators, print() and f-strings.
# (No if/else, loops, functions or lists yet - you do not need them.)

print("=== Test-Case ID Formatter ===")

# ---------------------------------------------------------------------------
# PART 1 - Ask the questions (input)
# ---------------------------------------------------------------------------
# TODO 1a: ask "Module prefix (e.g. login): " and store it in module_prefix.
#          Remove stray spaces and make it UPPER CASE (.strip() and .upper()).
#
# TODO 1b: ask "Test number: " and store it in test_number as an int.
#
# TODO 1c: ask "Test title: " and store it in test_title.
#          Remove stray spaces (.strip()) but keep the original capitals.
#
# TODO 1d: ask "Tests executed: " and store it in total_tests as an int.
#
# TODO 1e: ask "Tests passed: " and store it in passed_tests as an int.


# ---------------------------------------------------------------------------
# PART 2 - Build and print the test-case ID (f-string)
# ---------------------------------------------------------------------------
# TODO 2a: build test_id = prefix + "-" + number padded with zeros to 4 digits.
#          Example: "login" and 42 -> LOGIN-0042
#
# TODO 2b: print  Generated ID: LOGIN-0042   (with your own test_id)
#
# TODO 2c: print  Title: Valid login        (with your own test_title)


# ---------------------------------------------------------------------------
# PART 3 - Summary: failures, pass rate, release decision
# ---------------------------------------------------------------------------
# TODO 3a: failed_tests = total_tests - passed_tests
#
# TODO 3b: pass_rate = passed_tests / total_tests * 100, rounded to 1 decimal
#
# TODO 3c: release_ready = True when pass_rate is 90 or more, else False
#          (use a comparison operator, no if statement needed)
#
# TODO 3d: print these three lines exactly (values change, wording does not):
#              Failed: 6
#              Pass rate: 85.0%
#              Release ready: False
