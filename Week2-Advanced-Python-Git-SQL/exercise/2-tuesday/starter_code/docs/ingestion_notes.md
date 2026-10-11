# Ingestion module - design notes (Week 2, Day 2)

Answer in your own words, 2-4 sentences each. Replace every line that starts with
`TODO:`. (Delete nothing else.)

## 1. Exceptions or assertions?
In `validate_record` I raise exceptions for a negative duration, but in
`IngestionReport.check_invariants` I use `assert`. Why is each the right tool there?

TODO: your answer

## 2. Stop or collect?
Why is a malformed JSON file a `SourceError` that stops loading, while a record with
a bad status is a `RecordValidationError` that is collected? Who benefits from this split?

TODO: your answer

## 3. What did the context managers buy you?
Name two things that `open_source` / `LoadSession` do for the caller that you would otherwise
have to remember to do at every call site.

TODO: your answer

## 4. Your hardest bad-input case
Which sample file or record took you longest to handle, and what was the cause?

TODO: your answer
