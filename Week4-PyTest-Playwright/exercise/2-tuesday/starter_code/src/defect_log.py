"""Code under test: a tiny defect log in the style of the Project 1 bug-report work.

You do NOT edit files in src/. You only write tests for them.
"""
import csv

SEVERITIES = ("low", "medium", "high", "critical")


class DefectLog:
    def __init__(self):
        self._defects = {}  # id -> {"title", "severity", "status"}
        self._next_id = 1

    def add(self, title, severity="medium"):
        """Add a defect, return its integer id."""
        if not title or not title.strip():
            raise ValueError("title must not be empty")
        if severity not in SEVERITIES:
            raise ValueError(f"unknown severity: {severity}")
        defect_id = self._next_id
        self._next_id += 1
        self._defects[defect_id] = {"title": title.strip(), "severity": severity, "status": "open"}
        return defect_id

    def close(self, defect_id):
        """Close a defect. KeyError if unknown, ValueError if already closed."""
        defect = self._defects[defect_id]
        if defect["status"] == "closed":
            raise ValueError("defect already closed")
        defect["status"] = "closed"

    def total_count(self):
        return len(self._defects)

    def open_count(self):
        return sum(1 for d in self._defects.values() if d["status"] == "open")

    def titles_by_severity(self, severity):
        """Titles of OPEN defects with the given severity, in insertion order."""
        return [d["title"] for d in self._defects.values()
                if d["status"] == "open" and d["severity"] == severity]

    def export_csv(self, path):
        """Write all defects to a CSV file with columns id,title,severity,status."""
        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["id", "title", "severity", "status"])
            for defect_id, d in self._defects.items():
                writer.writerow([defect_id, d["title"], d["severity"], d["status"]])
