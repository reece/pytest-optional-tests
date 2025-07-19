# -*- coding: utf-8 -*-

import re

import pytest


# There are four invocation cases of the templated tests:
# - with no arguments => 
# - with --run-optional-tests=opt1
# - with --run-optional-tests=opt2
# - with --run-optional-tests=opt1,opt2
# Unmarked and (conventionally) marked functions are always run
# opt1 and opt2 functions are run only when the corresponding optional mark is specified
test_cases = [
    {"args": None,             "exp": set("unmarked marked                ".split())},
    {"args": ["opt1"        ], "exp": set("unmarked marked opt1      opt12".split())},
    {"args": [        "opt2"], "exp": set("unmarked marked      opt2 opt12".split())},
    {"args": ["opt1", "opt2"], "exp": set("unmarked marked opt1 opt2 opt12".split())},
    ]
test_ids = [str(t["args"]) for t in test_cases]


def test_help_message(pot_testdir):
    """test CLI --help string"""
    result = pot_testdir.runpytest(
        "--help",
    )
    assert 0 == result.ret
    result.stdout.re_match_lines([r"\s*--run-optional-tests=RUN_OPTIONAL_TESTS"])


def test_markers(pot_testdir):
    """test generating the list of marks declared in pytest.ini"""
    result = pot_testdir.runpytest(
        "--markers",
    )
    assert 0 == result.ret

    result.stdout.re_match_lines([
        r"@pytest\.mark\.marked",
        r"@pytest\.mark\.opt1",
        r"@pytest\.mark\.opt2",
        r"@pytest\.mark\.opt3",
        ])


@pytest.mark.parametrize("t", test_cases, ids=test_ids)
def test_collection(pot_testdir, t):
    def _extract_collected_tests(lines):
        collected_test_re = re.compile(r"test_pot.py::test_(\w+) PASSED")
        matches = [collected_test_re.search(line) for line in lines]
        return set(m.group(1) for m in filter(None, matches))

    opts = ["-vs", "--strict"]
    if t["args"]:
        opts += ["--run-optional-tests={}".format(",".join(t["args"]))]

    result = pot_testdir.runpytest(*opts)
    assert 0 == result.ret

    collected_tests = _extract_collected_tests(result.stdout.lines)
    assert t["exp"] == collected_tests


