package com.revature.qea.utils;

/** GIVEN. Like Runnable, but allowed to throw - handy for flows that declare "throws Exception". */
@FunctionalInterface
public interface ThrowingRunnable {
    void run() throws Exception;
}
