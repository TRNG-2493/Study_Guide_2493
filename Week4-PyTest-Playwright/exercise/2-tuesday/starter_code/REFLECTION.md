# Reflection (answer in your own words, 2-4 sentences each)

Name: ______________________    Date: ______________

1. Fixtures vs copy-paste. Pick one test from `test_defect_log.py`. What would have to change in ten places if you had NOT used a fixture?

2. Scopes. For `big_log` you used module scope and for `populated_log` function scope. Why not the other way round? What would break if two tests CLOSED defects in `big_log`?

3. Scope rule. A function-scoped fixture cannot be used by a session-scoped fixture. Why? (One sentence, then name the error PyTest shows.)

4. Parametrize. What does `ids=` buy you when a case fails in CI at 2 a.m.?

5. Mocking. In your own words, why must you patch `pricing.get_rate` and not `exchange.get_rate`?

6. Mocks lying. Give one way a test with a mock can pass even though the real code is broken. How could `autospec` or a contract test reduce that risk?

7. Project 1 link. Which two of your refactored tests would you keep as the first entries of the Project 1 automated regression suite, and why?
