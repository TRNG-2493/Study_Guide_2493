# rr/model.py
"""Model clients. Every client has one method: complete(messages, settings) -> str.
The agent cannot tell them apart; that is the point of the interface. Provided complete.
Lesson: written/5-friday/executing-agents-against-qa-requirements.md, section 4.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def story_id_of(messages: list) -> str:
    return re.search(r"^ID: (US-\d+)$", messages[-1]["content"], re.MULTILINE).group(1)


class ScriptedModel:
    """Offline stand-in: returns replies/<story_id>.txt. The replies are ILLUSTRATIVE,
    written for this course (including typical mistakes); they are not real model output."""

    def __init__(self, folder: str = "replies"):
        self.folder = ROOT / folder
        self.calls = 0

    def complete(self, messages: list, settings: dict) -> str:
        self.calls += 1
        return (self.folder / f"{story_id_of(messages)}.txt").read_text(encoding="utf-8")


class SavedReplyModel:
    """For a live Claude run: you paste the prompt into Claude yourself and save the reply as
    <folder>/<story_id>.reply.txt. This client only reads that file."""

    def __init__(self, folder: str = "live"):
        self.folder = ROOT / folder
        self.calls = 0

    def complete(self, messages: list, settings: dict) -> str:
        self.calls += 1
        path = self.folder / f"{story_id_of(messages)}.reply.txt"
        if not path.exists():
            raise FileNotFoundError(f"save Claude's reply as {path.relative_to(ROOT)} first")
        return path.read_text(encoding="utf-8")
