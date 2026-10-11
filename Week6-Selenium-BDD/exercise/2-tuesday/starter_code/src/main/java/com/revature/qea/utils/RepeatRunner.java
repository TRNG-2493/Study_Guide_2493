package com.revature.qea.utils;

/**
 * GIVEN - do not edit. Runs a flow several times and prints the pass rate.
 *
 * A run PASSES when it throws nothing AND Check.failures() is still 0.
 * Flaky tests reveal themselves here: a stable flow prints 5/5, a flaky one prints 3/5.
 */
public final class RepeatRunner {

    private RepeatRunner() { }

    /** @return number of passed runs */
    public static int run(String name, int times, ThrowingRunnable flow) {
        int passed = 0;
        for (int i = 1; i <= times; i++) {
            Check.reset();
            String outcome;
            try {
                flow.run();
                outcome = Check.failures() == 0 ? "PASS" : "FAIL (" + Check.failures() + " failed check(s))";
            } catch (Throwable t) {
                outcome = "ERROR " + t.getClass().getSimpleName();
            }
            if (outcome.equals("PASS")) passed++;
            System.out.println("  [" + name + "] run " + i + "/" + times + " -> " + outcome);
        }
        System.out.println(">>> " + name + ": " + passed + "/" + times + " passed");
        System.out.println();
        return passed;
    }
}
