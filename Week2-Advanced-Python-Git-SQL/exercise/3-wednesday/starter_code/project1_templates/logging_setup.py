"""
qe_foundations/utils/logging_setup.py   (Project 1 milestone, Part E: copy this file into your repo)

Contract (the self-check script tests exactly this):
    setup_logging(level="INFO", logfile=None) -> logging.Logger
      * configures the logger named "qe_foundations" (the parent of every module logger in the package)
      * console handler at `level`; if `logfile` is given, also a file handler that records DEBUG and up
      * safe to call twice: it must NOT add duplicate handlers
      * returns the "qe_foundations" logger
Call it ONCE, from your entry point (a script or main()), never at import time in a library module.
"""
import logging
import sys


def setup_logging(level="INFO", logfile=None):
    # TODO 1: get the logger named "qe_foundations" and set its level to DEBUG (gate 1)
    # TODO 2: if it already has handlers, return it unchanged (idempotent)
    # TODO 3: build a Formatter: time | level | logger name | message
    # TODO 4: console StreamHandler(sys.stdout) at `level` (gate 2)
    # TODO 5: if logfile: FileHandler(logfile, encoding="utf-8") at DEBUG
    # TODO 6: return the logger
    raise NotImplementedError("finish setup_logging")
