package com.revature.qea.flows;

import com.revature.qea.utils.RepeatRunner;

/**
 * GIVEN - do not edit. Runs every scenario N times and prints a pass-rate table.
 *
 *   mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.FlakinessRun -Dtimes=5 -Dheadless=true
 *
 * Optional: -Donly=1  runs just that scenario number (1..6).
 * Copy the ">>> name: x/y passed" lines into FLAKINESS_REPORT.md (baseline = before your fixes, after = after).
 */
public class FlakinessRun {

    public static void main(String[] args) {
        int times = Integer.getInteger("times", 5);
        String only = System.getProperty("only", "all");

        if (only.equals("all") || only.equals("1"))
            RepeatRunner.run("S1 dynamic loading (hidden element)", times, FlakyScenarios::s1HiddenElement);
        if (only.equals("all") || only.equals("2"))
            RepeatRunner.run("S2 dynamic loading (element added later)", times, FlakyScenarios::s2ElementAddedLater);
        if (only.equals("all") || only.equals("3"))
            RepeatRunner.run("S3 dynamic controls (remove + enable)", times, FlakyScenarios::s3DynamicControls);
        if (only.equals("all") || only.equals("4"))
            RepeatRunner.run("S4 SauceDemo bad-login error", times, FlakyScenarios::s4BadLoginError);
        if (only.equals("all") || only.equals("5"))
            RepeatRunner.run("S5 Monday LoginSearchFlow", times, LoginSearchFlow::happyPathLoginAndSearch);
        if (only.equals("all") || only.equals("6"))
            RepeatRunner.run("S6 SortFlow", times, SortFlow::sortProducts);
    }
}
