# ShopFront Gherkin house style

The team's feature files follow these rules. Two real files are in `features/`.

1. One Feature per file, a one-line description under it, no Background unless every scenario needs it.
2. Steps are written in the first person ("I"), never "the user".
3. Exact values and exact messages are written in double quotes in the steps.
4. When several cases differ only by data, use one Scenario Outline with an Examples table.
5. Scenario titles describe the behaviour, not the data ("Reject a username that is too short").
6. Every scenario is tagged with the requirement area: `@registration`, `@login`, `@search`.
7. No prose, comments or notes outside the Gherkin.
