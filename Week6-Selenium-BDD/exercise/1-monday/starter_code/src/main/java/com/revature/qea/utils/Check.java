package com.revature.qea.utils;

/**
 * GIVEN - do not edit. A tiny assertion helper so your flows can print PASS/FAIL.
 * (In Thursday's Cucumber work you will switch to real JUnit assertions.)
 */
public final class Check {

    private Check() { }

    /** Prints "PASS  label" or "FAIL  label" and returns the result so you can count failures. */
    public static boolean that(String label, boolean condition) {
        System.out.println((condition ? "PASS  " : "FAIL  ") + label);
        return condition;
    }

    public static boolean equal(String label, Object expected, Object actual) {
        boolean ok = expected == null ? actual == null : expected.equals(actual);
        System.out.println((ok ? "PASS  " : "FAIL  ") + label
                + (ok ? "" : "  (expected: [" + expected + "] but was: [" + actual + "])"));
        return ok;
    }
}
