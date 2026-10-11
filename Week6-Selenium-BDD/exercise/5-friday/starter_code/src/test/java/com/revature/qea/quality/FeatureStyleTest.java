package com.revature.qea.quality;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * GIVEN - do not edit. Thursday's style rules, updated for Friday (Background, Rule, Scenario Outline and tags are
 * now allowed). It never opens a browser:   mvn test -Dtest=FeatureStyleTest
 */
public class FeatureStyleTest {

    private static final Path FEATURES = Paths.get("src", "test", "resources", "features");
    private static final Path STEPS = Paths.get("src", "test", "java", "com", "revature", "qea", "steps");

    private static final Pattern STEP_LINE = Pattern.compile("^(Given|When|Then|And|But)\\s.*");
    private static final Pattern SCENARIO_START = Pattern.compile("^(Scenario|Scenario Outline|Scenario Template|Example):.*");
    /** UI mechanics do not belong in Gherkin: scenarios describe behaviour, not clicks. */
    private static final Pattern UI_WORDS = Pattern.compile(
            "\\b(click|clicks|clicked|button|xpath|css|locator|selector|textbox|dropdown|input field)\\b",
            Pattern.CASE_INSENSITIVE);

    static List<Path> featureFiles() throws IOException {
        if (!Files.isDirectory(FEATURES)) {
            return new ArrayList<>();
        }
        try (Stream<Path> s = Files.walk(FEATURES)) {
            return s.filter(p -> p.toString().endsWith(".feature")).sorted().collect(Collectors.toList());
        }
    }

    static List<String> lines(Path file) throws IOException {
        return Files.readAllLines(file).stream().map(String::trim).collect(Collectors.toList());
    }

    @Test
    void atLeastThreeFeatureFilesAndTenScenarioDefinitions() throws IOException {
        long scenarios = 0;
        for (Path f : featureFiles()) {
            scenarios += lines(f).stream().filter(l -> SCENARIO_START.matcher(l).matches()).count();
        }
        assertTrue(featureFiles().size() >= 3, "Expected at least 3 .feature files but found " + featureFiles().size());
        assertTrue(scenarios >= 10, "Expected at least 10 scenario definitions but found " + scenarios);
    }

    @Test
    void everyFeatureHasAStoryHeader() throws IOException {
        List<String> problems = new ArrayList<>();
        for (Path f : featureFiles()) {
            List<String> ls = lines(f);
            boolean asA = ls.stream().anyMatch(l -> l.toLowerCase().startsWith("as a"));
            boolean iWant = ls.stream().anyMatch(l -> l.toLowerCase().startsWith("i want"));
            boolean soThat = ls.stream().anyMatch(l -> l.toLowerCase().startsWith("so that"));
            if (!(asA && iWant && soThat)) {
                problems.add(f.getFileName() + " needs the 'As a / I want / so that' story lines under Feature:");
            }
        }
        assertTrue(problems.isEmpty(), String.join("\n", problems));
    }

    @Test
    void stepsDescribeBehaviourNotUiMechanics() throws IOException {
        List<String> problems = new ArrayList<>();
        for (Path f : featureFiles()) {
            for (String l : lines(f)) {
                if (STEP_LINE.matcher(l).matches() && UI_WORDS.matcher(l).find()) {
                    problems.add(f.getFileName() + ": UI mechanics in a step -> " + l);
                }
            }
        }
        assertTrue(problems.isEmpty(), String.join("\n", problems));
    }

    @Test
    void everyScenarioHasWhenAndThenAndIsShort() throws IOException {
        List<String> problems = new ArrayList<>();
        for (Path f : featureFiles()) {
            String current = null;
            int steps = 0;
            boolean hasWhen = false, hasThen = false;
            List<String> all = lines(f);
            all.add("Scenario: <end>");                       // sentinel flushes the last scenario
            for (String l : all) {
                if (SCENARIO_START.matcher(l).matches()) {
                    if (current != null) {
                        if (steps > 8) {
                            problems.add(f.getFileName() + " / " + current + " has " + steps + " steps (max 8)");
                        }
                        if (!(hasWhen && hasThen) && !current.contains("@wip")) {
                            problems.add(f.getFileName() + " / " + current + " needs a When and a Then");
                        }
                    }
                    current = l;
                    steps = 0;
                    hasWhen = hasThen = false;
                } else if (STEP_LINE.matcher(l).matches()) {
                    steps++;
                    hasWhen |= l.startsWith("When");
                    hasThen |= l.startsWith("Then");
                }
            }
        }
        assertTrue(problems.isEmpty(), String.join("\n", problems));
    }

    @Test
    void stepClassesUseOnlyPageObjects() throws IOException {
        List<String> problems = new ArrayList<>();
        if (!Files.isDirectory(STEPS)) {
            return;
        }
        try (Stream<Path> s = Files.walk(STEPS)) {
            for (Path f : s.filter(p -> p.toString().endsWith(".java")).collect(Collectors.toList())) {
                // comments may mention these words; only real code counts
                String code = Files.readString(f).replaceAll("(?s)/\\*.*?\\*/|//[^\\n]*", "");
                if (Pattern.compile("\\bBy\\.|findElements?\\(|Thread\\.sleep|WebDriverWait").matcher(code).find()) {
                    problems.add(f.getFileName() + " touches Selenium directly (By / findElement / waits / sleep). "
                            + "Move that into a page object method.");
                }
            }
        }
        assertTrue(problems.isEmpty(), String.join("\n", problems));
    }
}
