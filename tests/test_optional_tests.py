# -*- coding: utf-8 -*-

import re

import pytest


def test_help_message(pot_testdir):
    result = pot_testdir.runpytest(
        '--help',
    )
    assert 0 == result.ret
    assert None is result.stdout.re_match_lines([r"\s*--run-optional-tests=RUN_OPTIONAL_TESTS"])


def test_markers(pot_testdir):
    result = pot_testdir.runpytest(
        '--markers',
    )
    assert 0 == result.ret
    assert None is result.stdout.re_match_lines([
        r"@pytest\.mark\.other",
        r"@pytest\.mark\.opt1",
        r"@pytest\.mark\.opt2",
        r"@pytest\.mark\.opt3",
        ])


test_cases = [
    {"args": None,  "exp": set("no_mark                 other".split())},
    {"args": (1,),  "exp": set("no_mark opt1 opt12      other".split())},
    {"args": (2,),  "exp": set("no_mark      opt12 opt2 other".split())},
    {"args": (1,2), "exp": set("no_mark opt1 opt12 opt2 other".split())},
    ]
test_ids = [str(t["args"]) for t in test_cases]


@pytest.mark.parametrize("t", test_cases, ids=test_ids)
def test_collection(pot_testdir, t):
    opts = ['-vs', '--strict']
    if t["args"]:
        ots = ["opt{}".format(n) for n in t["args"]]
        opts += ["--run-optional-tests={}".format(",".join(ots))]

    result = pot_testdir.runpytest(*opts)
    assert 0 == result.ret

    collected_tests = _extract_collected_tests(result.stdout.lines)
    assert t["exp"] == collected_tests


def _extract_collected_tests(lines):
    collected_test_re = re.compile(r"test_pot.py::test_(\w+) PASSED")
    matches = [collected_test_re.search(l) for l in lines]
    return set(m.group(1) for m in filter(None, matches))
