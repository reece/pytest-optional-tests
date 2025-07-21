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
    # args are run-optional-tests arguments, exp is expected functions to be tested
    {"args": None,             "exp": set("unmarked marked                ".split())},
    {"args": ["opt1"        ], "exp": set("unmarked marked opt1 opt1_opt2".split())},
    {"args": [        "opt2"], "exp": set("unmarked marked opt2_marked marked_opt2 opt1_opt2".split())},
    {"args": ["opt1", "opt2"], "exp": set("unmarked marked opt1 opt2_marked marked_opt2 opt1_opt2".split())},
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
        r"@pytest\.mark\.opt1",
        r"@pytest\.mark\.opt2",
        r"@pytest\.mark\.opt3",
        ])


@pytest.mark.parametrize("t", test_cases, ids=test_ids)
def test_collection(pot_testdir, t):
    def _extract_passed_tests(lines):
        passed_test_re = re.compile(r"test_pot.py::test_([_\w]+) PASSED")
        matches = [passed_test_re.search(line) for line in lines]
        return set(m.group(1) for m in filter(None, matches))

    opts = ["-vs", "--strict"]
    if t["args"]:
        opts += ["--run-optional-tests={}".format(",".join(t["args"]))]

    result = pot_testdir.runpytest(*opts)
    assert 0 == result.ret

    passed_tests = _extract_passed_tests(result.stdout.lines)
    assert t["exp"] == passed_tests


