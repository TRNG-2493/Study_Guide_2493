"""Test-report system: TestResult, Suite, Reporter (+ subclasses).

Fill in every TODO. Run `python3 check_exercise.py N` after each part.
Until a method is finished it raises NotImplementedError; that is normal.
"""


class TestResult:
    """One test outcome. Validated, with two alternative constructors."""

    # Class variables (shared by every TestResult). Given to you.
    VALID_STATUSES = ("PASS", "FAIL", "SKIPPED", "ERROR")
    total_created = 0

    def __init__(self, test_id, status, duration=0.0, message=""):
        # TODO 1.1: validate test_id with TestResult.is_valid_id (ValueError if bad)
        #           and store it in self._test_id
        # TODO 1.2: set self.status and self.duration THROUGH the properties below,
        #           so validation runs. Store message as a plain attribute.
        # TODO 1.3: increase TestResult.total_created ONLY after everything above
        #           succeeded (an object that fails validation must not be counted)
        raise NotImplementedError("TODO 1.1-1.3: write __init__")

    # ---- static helper ----------------------------------------------------
    @staticmethod
    def is_valid_id(test_id):
        """True for text like 'TC-001': 'TC-' followed by one or more digits."""
        # TODO 1.4: return True/False. Never raise, even for None or numbers.
        raise NotImplementedError("TODO 1.4: write is_valid_id")

    # ---- encapsulated attributes -------------------------------------------
    @property
    def test_id(self):
        # TODO 1.5: return the stored id. Read-only: do NOT write a setter.
        raise NotImplementedError("TODO 1.5: test_id getter")

    @property
    def status(self):
        # TODO 1.6: return the stored status
        raise NotImplementedError("TODO 1.6: status getter")

    @status.setter
    def status(self, value):
        # TODO 1.6: must be text; strip and upper-case it; it must be in
        #           VALID_STATUSES, otherwise raise ValueError (include the bad
        #           value in the message). Only then store it in self._status.
        raise NotImplementedError("TODO 1.6: status setter")

    @property
    def duration(self):
        # TODO 1.7: return the stored duration
        raise NotImplementedError("TODO 1.7: duration getter")

    @duration.setter
    def duration(self, value):
        # TODO 1.7: not int/float (or a bool) -> TypeError; negative -> ValueError;
        #           otherwise store float(value) in self._duration
        raise NotImplementedError("TODO 1.7: duration setter")

    @property
    def is_passed(self):
        # TODO 1.8: True only when the status is "PASS". Read-only.
        raise NotImplementedError("TODO 1.8: is_passed")

    # ---- class methods ------------------------------------------------------
    @classmethod
    def how_many(cls):
        # TODO 1.9: return the class-level counter
        raise NotImplementedError("TODO 1.9: how_many")

    @classmethod
    def from_dict(cls, data):
        # TODO 1.10: keys "test_id" and "status" are required (ValueError naming the
        #            missing key); "duration" (default 0.0) and "message"
        #            (default "") are optional. Build the object with cls(...),
        #            NOT TestResult(...).
        raise NotImplementedError("TODO 1.10: from_dict")

    @classmethod
    def from_csv_line(cls, line):
        # TODO 1.11: "TC-001,PASS,1.2,Timeout after 30s" -> TestResult.
        #            Only the first two fields are required. The message may
        #            itself contain commas (hint: split with a limit).
        #            Strip spaces around each field. Too few fields -> ValueError.
        raise NotImplementedError("TODO 1.11: from_csv_line")

    # ---- text forms ----------------------------------------------------------
    def __str__(self):
        # TODO 1.12: "TC-001 PASS 1.2s"  (add " - <message>" only if there is one)
        raise NotImplementedError("TODO 1.12: __str__")

    def __repr__(self):
        # TODO 1.12: "TestResult('TC-001', 'PASS', 1.2)"; use the REAL class name
        #            via type(self).__name__ so subclasses print correctly
        raise NotImplementedError("TODO 1.12: __repr__")


class Suite:
    """A named collection of TestResult objects (has-a, not is-a list)."""

    def __init__(self, name):
        # TODO 2.1: name must be non-empty text after strip() (else ValueError);
        #           store the stripped name in self.name
        # TODO 2.2: create the per-object list self._results here (NOT in the class body)
        raise NotImplementedError("TODO 2.1-2.2: Suite.__init__")

    @classmethod
    def from_rows(cls, name, rows):
        # TODO 2.3: build a suite and add TestResult.from_dict(row) for every row
        raise NotImplementedError("TODO 2.3: from_rows")

    def add(self, result):
        # TODO 2.4: not a TestResult -> TypeError; a test_id already in the suite
        #           -> ValueError (mention the id); otherwise append
        raise NotImplementedError("TODO 2.4: add")

    @property
    def results(self):
        # TODO 2.5: return a COPY of the internal list
        raise NotImplementedError("TODO 2.5: results")

    def count(self):
        # TODO 2.5: number of results
        raise NotImplementedError("TODO 2.5: count")

    @property
    def pass_rate(self):
        # TODO 2.6: percent (0-100) of results whose status is PASS, out of ALL
        #           results (SKIPPED counts in the total). Empty suite -> 0.0
        raise NotImplementedError("TODO 2.6: pass_rate")

    @property
    def total_duration(self):
        # TODO 2.7: sum of all durations
        raise NotImplementedError("TODO 2.7: total_duration")

    def counts_by_status(self):
        # TODO 2.7: dict with EVERY valid status as a key, e.g.
        #           {"PASS": 2, "FAIL": 1, "SKIPPED": 1, "ERROR": 0}
        raise NotImplementedError("TODO 2.7: counts_by_status")

    def failures(self):
        # TODO 2.8: list of results whose status is FAIL or ERROR (suite order)
        raise NotImplementedError("TODO 2.8: failures")

    def slowest(self, n=1):
        # TODO 2.8: the n slowest results, slowest first (sorted with a key)
        raise NotImplementedError("TODO 2.8: slowest")


class Reporter:
    """Base class: presentation only. Subclasses override render()."""

    def __init__(self, suite):
        # TODO 3.1: suite must be a Suite (else TypeError); store it as self.suite
        raise NotImplementedError("TODO 3.1: Reporter.__init__")

    @staticmethod
    def pad(text, width):
        # TODO 3.2: str(text) left-justified in `width` characters. Never cut text.
        raise NotImplementedError("TODO 3.2: pad")

    @staticmethod
    def format_percent(value):
        # TODO 3.2: 66.666 -> "66.7%"
        raise NotImplementedError("TODO 3.2: format_percent")

    def render(self):
        # TODO 3.3: the base class has no format: raise NotImplementedError with a
        #           helpful message naming the class (type(self).__name__)
        pass

    def line_count(self):
        # TODO 3.4: number of lines in self.render(). Write it ONCE here;
        #           subclasses inherit it.
        raise NotImplementedError("TODO 3.4: line_count")


class TextReporter(Reporter):
    def render(self):
        # TODO 3.5: see README for the exact layout (header, one row per result,
        #           "Pass rate: 50.0%"). Use self.pad and self.format_percent.
        raise NotImplementedError("TODO 3.5: TextReporter.render")


class CsvReporter(Reporter):
    HEADER = "test_id,status,duration,message"

    @staticmethod
    def clean_cell(text):
        # TODO 3.6: commas -> ";" and newlines -> " " so one cell stays one cell
        raise NotImplementedError("TODO 3.6: clean_cell")

    def render(self):
        # TODO 3.6: see README for the exact layout
        raise NotImplementedError("TODO 3.6: CsvReporter.render")


# STRETCH 1: add class MarkdownReporter(Reporter) here (see README).
