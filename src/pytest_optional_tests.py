# -*- coding: utf-8 -*-
"""implements declaration of optional tests using pytest markers

"""


import logging
import re

import pytest

_logger = logging.getLogger(__name__)

marker_re = re.compile(r"^(?P<marker>\w+)(:\s*(?P<description>.*))?")


def pytest_addoption(parser):
    group = parser.getgroup("collect")
    group.addoption(
        "--run-optional-tests",
        action="append",
        dest="run_optional_tests",
        default=None,
        help="Optional test markers to run, space and/or comma separated okay",
    )
    parser.addini(
        'run_optional_tests',
        'Optional test markers to run, multiple and/or comma separated okay',
        type="linelist",
    )
    parser.addini(
        "optional_tests",
        "Declaration of optional tests",
        type="linelist",
    )


def pytest_configure(config):
    # register all optional tests declared in ini file as markers
    # https://docs.pytest.org/en/latest/writing_plugins.html#registering-custom-markers
    ot_ini = [line.strip() for line in config.getini("optional_tests") if line.strip()]
    for ot in ot_ini:
        # ot should be a line like "optmarker: this is an opt marker", as with markers section
        config.addinivalue_line("markers", ot)
    ot_markers = set(marker_re.match(l).group(1) for l in ot_ini)

    # collect requested optional tests
    ot_run = config.getoption("run_optional_tests")
    if not ot_run:
        ot_run = config.getini("run_optional_tests")
    ot_run = {marker for line in ot_run for marker in re.split(r"[,\s]+", line) if marker}

    _logger.info("optional tests to run:", ot_run)
    if ot_run:
        unknown_tests = ot_run - ot_markers
        if unknown_tests:
            raise ValueError("Requested execution of undeclared optional tests: {}".format(", ".join(unknown_tests)))

    config._ot_markers = ot_markers
    config._ot_run = ot_run
    

def pytest_collection_modifyitems(config, items):
    """add skip marks to tests declared as optional when opt mark is disabled (i.e., not requested)"""
    ot_markers = config._ot_markers
    ot_run = config._ot_run

    skip_marks = {}
    for item in items:
        item_markers = set(m.name for m in item.iter_markers())
        if not item_markers:
            continue
        test_otms = item_markers & ot_markers
        if not test_otms:
            # test is not marked with any optional marker
            continue
        if test_otms & ot_run:
            # test is marked with an enabled optional test; don't skip
            continue
        test_otms_str = ",".join(sorted(test_otms))
        if test_otms_str not in skip_marks:
            skip_marks[test_otms_str] = pytest.mark.skip(reason="Optional test; activate with `--run-optional-tests=` and any of " + str(sorted(test_otms)))
        item.add_marker(skip_marks[test_otms_str])
