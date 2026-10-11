package com.revature.qea.runners;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.GLUE_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.PLUGIN_PROPERTY_NAME;

/**
 * Part 3 - the JUnit 5 Suite runner (junit-integration.md, cucumber-reporting.md).
 * TODO: extend the plug-in list to: pretty, summary, html:target/cucumber-reports/report.html,
 *       json:target/cucumber-reports/cucumber.json, junit:target/cucumber-reports/cucumber.xml, rerun:target/rerun.txt
 * TODO: do NOT put a tag filter here (no tag-filter annotation) - the pom property cucumber.filter.tags owns it.
 */
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.revature.qea.steps,com.revature.qea.support")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty")
public class RunCucumberTest {
}
