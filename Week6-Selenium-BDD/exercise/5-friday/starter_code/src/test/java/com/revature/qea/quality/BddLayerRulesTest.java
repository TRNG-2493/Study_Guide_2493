package com.revature.qea.quality;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Pattern;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * GIVEN - do not edit. Friday's Definition of Done as an automated test: tags, Background/Rule/Outline, hooks,
 * POM profiles, runner plug-ins, documentation. It never opens a browser.   mvn test -Dtest=BddLayerRulesTest
 * It is RED until the work is finished.
 */
public class BddLayerRulesTest {

    private static final Path POM = Paths.get("pom.xml");
    private static final Path RUNNER = Paths.get("src", "test", "java", "com", "revature", "qea", "runners", "RunCucumberTest.java");
    private static final Path HOOKS = Paths.get("src", "test", "java", "com", "revature", "qea", "steps", "Hooks.java");
    private static final Path CONTEXT = Paths.get("src", "test", "java", "com", "revature", "qea", "support", "TestContext.java");
    private static final Path DOC = Paths.get("docs", "TAGS_AND_RUNS.md");
    private static final Path README = Paths.get("README_PROJECT.md");

    private static final Set<String> TAXONOMY = new HashSet<>(Arrays.asList(
            "@ui", "@login", "@cart", "@sort", "@smoke", "@regression", "@negative", "@positive", "@slow", "@wip",
            "@ignore", "@report-demo"));

    private static final Pattern SCENARIO_START = Pattern.compile("^(Scenario|Scenario Outline|Scenario Template|Example):.*");

    private static String read(Path p) throws IOException {
        return Files.exists(p) ? Files.readString(p) : "";
    }

    /** A scenario with its own tag line(s). */
    private static final class Sc {
        final String file;
        final String title;
        final Set<String> tags;
        Sc(String file, String title, Set<String> tags) {
            this.file = file;
            this.title = title;
            this.tags = tags;
        }
    }

    private static List<Sc> scenarios() throws IOException {
        List<Sc> out = new ArrayList<>();
        for (Path f : FeatureStyleTest.featureFiles()) {
            Set<String> pending = new HashSet<>();
            for (String l : FeatureStyleTest.lines(f)) {
                if (l.startsWith("@")) {
                    pending.addAll(Arrays.asList(l.split("\\s+")));
                } else if (SCENARIO_START.matcher(l).matches()) {
                    out.add(new Sc(f.getFileName().toString(), l, new HashSet<>(pending)));
                    pending.clear();
                } else if (!l.isEmpty() && !l.startsWith("#")) {
                    pending.clear();
                }
            }
        }
        return out;
    }

    @Test
    void everyFeatureStartsWithTagsIncludingUi() throws IOException {
        List<String> problems = new ArrayList<>();
        for (Path f : FeatureStyleTest.featureFiles()) {
            String first = FeatureStyleTest.lines(f).stream()
                    .filter(l -> !l.isEmpty() && !l.startsWith("#")).findFirst().orElse("");
            if (!(first.startsWith("@") && Arrays.asList(first.split("\\s+")).contains("@ui"))) {
                problems.add(f.getFileName() + ": the first line must be a feature-level tag line containing @ui");
            }
        }
        assertTrue(problems.isEmpty(), String.join("\n", problems));
    }

    @Test
    void onlyTagsFromTheTaxonomyAreUsed() throws IOException {
        List<String> problems = new ArrayList<>();
        for (Path f : FeatureStyleTest.featureFiles()) {
            for (String l : FeatureStyleTest.lines(f)) {
                if (l.startsWith("@")) {
                    for (String t : l.split("\\s+")) {
                        if (!TAXONOMY.contains(t)) {
                            problems.add(f.getFileName() + ": tag " + t + " is not in the taxonomy " + TAXONOMY);
                        }
                    }
                }
            }
        }
        assertTrue(problems.isEmpty(), String.join("\n", problems));
    }

    @Test
    void everyScenarioIsClassifiedSmokeRegressionOrWip() throws IOException {
        List<String> problems = new ArrayList<>();
        for (Sc s : scenarios()) {
            if (!(s.tags.contains("@smoke") || s.tags.contains("@regression") || s.tags.contains("@wip"))) {
                problems.add(s.file + " / " + s.title + " needs @smoke, @regression or @wip");
            }
        }
        assertTrue(problems.isEmpty(), String.join("\n", problems));
    }

    @Test
    void smokeSuiteIsSmallButCoversMoreThanOneFeature() throws IOException {
        List<Sc> smoke = new ArrayList<>();
        Set<String> files = new HashSet<>();
        for (Sc s : scenarios()) {
            if (s.tags.contains("@smoke")) {
                smoke.add(s);
                files.add(s.file);
            }
        }
        assertTrue(smoke.size() >= 3 && smoke.size() <= 6,
                "Expected 3 to 6 @smoke scenarios (a smoke suite is small) but found " + smoke.size());
        assertTrue(files.size() >= 3, "@smoke must cover all three features, found it only in " + files);
    }

    @Test
    void atLeastOneWipScenarioExistsAndIsExcludedByDefault() throws IOException {
        boolean wip = scenarios().stream().anyMatch(s -> s.tags.contains("@wip"));
        assertTrue(wip, "Keep at least one @wip scenario (work in progress, not ready) to demonstrate exclusion");
        assertTrue(read(POM).contains("not @wip"), "pom.xml: the default cucumber.filter.tags must exclude @wip (not @wip)");
    }

    @Test
    void backgroundRuleAndOutlineAreUsed() throws IOException {
        int backgrounds = 0;
        boolean rule = false;
        boolean outlineWithFourRows = false;
        for (Path f : FeatureStyleTest.featureFiles()) {
            List<String> ls = FeatureStyleTest.lines(f);
            if (ls.stream().anyMatch(l -> l.startsWith("Background:"))) {
                backgrounds++;
            }
            rule |= ls.stream().anyMatch(l -> l.startsWith("Rule:"));
            boolean inOutline = false, inExamples = false;
            int rows = 0;
            for (String l : ls) {
                if (l.startsWith("Scenario Outline:") || l.startsWith("Scenario Template:")) {
                    inOutline = true;
                    inExamples = false;
                    rows = 0;
                } else if (inOutline && l.startsWith("Examples:")) {
                    inExamples = true;
                    rows = 0;
                } else if (inExamples && l.startsWith("|")) {
                    rows++;
                    if (rows - 1 >= 4) {                    // header row + 4 data rows
                        outlineWithFourRows = true;
                    }
                } else if (SCENARIO_START.matcher(l).matches() && !l.startsWith("Scenario Outline:")) {
                    inOutline = false;
                    inExamples = false;
                }
            }
        }
        assertTrue(backgrounds >= 2, "Use Background in at least 2 features (sort and cart) - found " + backgrounds);
        assertTrue(rule, "Use at least one Rule: (cart feature)");
        assertTrue(outlineWithFourRows, "Use a Scenario Outline with an Examples table of at least 4 data rows (login)");
    }

    @Test
    void backgroundRemovesTheRepeatedLoginStep() throws IOException {
        List<String> problems = new ArrayList<>();
        for (Path f : FeatureStyleTest.featureFiles()) {
            List<String> ls = FeatureStyleTest.lines(f);
            long logins = ls.stream().filter(l -> l.equals("Given the shopper is logged in")).count();
            boolean hasBackground = ls.stream().anyMatch(l -> l.startsWith("Background:"));
            if (hasBackground && logins > 1) {
                problems.add(f.getFileName() + ": 'Given the shopper is logged in' appears " + logins
                        + " times - it belongs once in the Background");
            }
        }
        assertTrue(problems.isEmpty(), String.join("\n", problems));
    }

    @Test
    void hooksClassManagesTheBrowserAndEvidence() throws IOException {
        // comments are stripped: the TODO text in the skeleton must not satisfy the rule
        String h = read(HOOKS).replaceAll("(?s)/\\*.*?\\*/", "").replaceAll("//[^\n]*", "");
        assertTrue(!h.isEmpty(), "Create src/test/java/.../steps/Hooks.java");
        List<String> missing = new ArrayList<>();
        for (String needle : new String[] {"@BeforeAll", "@AfterAll", "@Before(", "@After(order", "isFailed()", "scenario.attach", "quitDriver()"}) {
            if (!h.contains(needle)) {
                missing.add(needle);
            }
        }
        assertTrue(missing.isEmpty(), "Hooks.java is missing: " + missing);
        assertTrue(!h.contains("Thread.sleep"), "No Thread.sleep in hooks");
    }

    @Test
    void testContextNoLongerNeedsThursdaysSafetyNet() throws IOException {
        String c = read(CONTEXT);
        assertTrue(!c.isEmpty() && !c.contains("OPEN_DRIVERS") && !c.contains("addShutdownHook"),
                "TestContext: delete Thursday's static safety net (OPEN_DRIVERS / shutdown hook); the @After hook owns cleanup now");
    }

    @Test
    void pomHasPropertiesSurefireProfilesAndReporting() throws IOException {
        String pom = read(POM).replaceAll("(?s)<!--.*?-->", "");   // comments do not count
        List<String> missing = new ArrayList<>();
        for (String needle : new String[] {"<cucumber.filter.tags>", "<browser>", "<headless>", "systemPropertyVariables",
                "<id>smoke</id>", "<id>regression</id>", "<id>ci</id>", "maven-cucumber-reporting"}) {
            if (!pom.contains(needle)) {
                missing.add(needle);
            }
        }
        assertTrue(missing.isEmpty(), "pom.xml is missing: " + missing);
    }

    @Test
    void runnerWritesReportsAndLeavesTagFilteringToThePom() throws IOException {
        String r = read(RUNNER).replaceAll("(?s)/\\*.*?\\*/", "").replaceAll("//[^\n]*", "");   // comments do not count
        List<String> missing = new ArrayList<>();
        for (String needle : new String[] {"html:", "json:", "junit:", "rerun:", "summary"}) {
            if (!r.contains(needle)) {
                missing.add(needle);
            }
        }
        assertTrue(missing.isEmpty(), "RunCucumberTest plug-ins missing: " + missing);
        assertTrue(!r.contains("FILTER_TAGS"), "No FILTER_TAGS in the runner: one place per setting - the pom property owns the tag expression");
    }

    @Test
    void documentationIsCompleted() throws IOException {
        String doc = read(DOC);
        String readme = read(README);
        assertTrue(!doc.isEmpty(), "Create docs/TAGS_AND_RUNS.md from the template");
        assertTrue(!doc.contains("<<FILL>>"), "docs/TAGS_AND_RUNS.md still contains <<FILL>> placeholders");
        assertTrue(!readme.contains("<<FILL>>"), "README_PROJECT.md still contains <<FILL>> placeholders");
    }
}
