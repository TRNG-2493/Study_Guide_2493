package com.revature.qea.utils;

/**
 * GIVEN - do not edit. A tiny assertion helper so your flows can print PASS/FAIL.
 * Tuesday addition: it now COUNTS failures so RepeatRunner can decide whether a run passed.
 * (In Thursday's Cucumber work you will switch to real JUnit assertions.)
 */
public final class Check {

    private static int failures = 0;

    private Check() { }

    /** Prints "PASS  label" or "FAIL  label" and returns the result so you can count failures. */
    public static boolean that(String label, boolean condition) {
        System.out.println((condition ? "PASS  " : "FAIL  ") + label);
        if (!condition) failures++;
        return condition;
    }

    public static boolean equal(String label, Object expected, Object actual) {
        boolean ok = expected == null ? actual == null : expected.equals(actual);
        System.out.println((ok ? "PASS  " : "FAIL  ") + label
                + (ok ? "" : "  (expected: [" + expected + "] but was: [" + actual + "])"));
        if (!ok) failures++;
        return ok;
    }

    /** Number of FAILed checks since the last reset(). */
    public static int failures() {
        return failures;
    }

    public static void reset() {
        failures = 0;
    }
}
