# -*- coding: utf-8 -*-
"""implements declaration of optional tests using pytest markers

"""


import itertools
import logging
import re

import pytest

_logger = logging.getLogger(__name__)

marker_re = re.compile("^(?P<marker>\w+)(:\s*(?P<description>.*))?")


def pytest_addoption(parser):
    group = parser.getgroup('collect')
    group.addoption(
        '--run-optional-tests',
        action='append',
        dest='run_optional_tests',
        default=None,
        help='Optional test markers to run, multiple and/or comma separated okay',
    )
    parser.addini(
        'optional_tests',
        'Optional test markers to run, multiple and/or comma separated okay'
    )


def pytest_configure(config):
    # register all optional tests declared in ini file as markers
    # https://docs.pytest.org/en/latest/writing_plugins.html#registering-custom-markers
    ot_ini = config.inicfg.get("optional_tests")  # None if NA
    if ot_ini:
        ot_ini = ot_ini.split("\n")
    else:
        ot_ini = []
    for ot in ot_ini:
        # ot should be a line like "optmarker: this is an opt marker", as with markers section
        config.addinivalue_line("markers", ot)
    ot_markers = set(marker_re.match(l).group(1) for l in ot_ini)

    # collect requested optional tests
    ot_run = config.getoption("run_optional_tests")
    if ot_run:
        ot_run = list(itertools.chain.from_iterable(a.split(",") for a in ot_run))
    else:
        ot_run = config.inicfg.get("run_optional_tests", [])
        if ot_run:
            ot_run = list(re.split(r"[,\s]+", ot_run))
    ot_run = set(ot_run)

    _logger.info("optional tests to run:", ot_run)
    if ot_run:
        unknown_tests = ot_run - ot_markers
        if unknown_tests:
            raise ValueError("Requested execution of undeclared optional tests: {}".format(", ".join(unknown_tests)))

    config._ot_markers = set(ot_markers)
    config._ot_run = set(ot_run)
    

def pytest_collection_modifyitems(config, items):
    # https://stackoverflow.com/a/50114028/342839
    ot_markers = config._ot_markers
    ot_run = config._ot_run

    skips = {}
    for item in items:
        marker_names = set(m.name for m in item.iter_markers())
        if not marker_names:
            continue
        test_otms = marker_names & ot_markers
        if not test_otms:
            # test is not marked with any optional marker
            continue
        if test_otms & ot_run:
            # test is marked with an enabled optional test; don't skip
            continue
        mns = str(marker_names)
        if mns not in skips:
            skips[mns] = pytest.mark.skip(reason="Skipping; marked with disabled optional tests ({})".format(mns))
        item.add_marker(skips[mns])
