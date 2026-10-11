package com.revature.qea.steps;

import com.revature.qea.support.TestContext;

/**
 * TODO (slot 5) - steps shared by MORE THAN ONE feature live here.
 *
 * Why a separate class? If both SortSteps and CartSteps defined "the shopper is logged in", Cucumber would fail
 * with AmbiguousStepDefinitionsException. One step text = one definition, in one class.
 *
 * Put here: the Given that logs a shopper in (page objects only!).
 */
public class CommonSteps {

    private final TestContext context;

    public CommonSteps(TestContext context) {
        this.context = context;
    }

    // TODO @Given("the shopper is logged in") -> log in as standard_user / secret_sauce with LoginPage.loginAs(...)
}
