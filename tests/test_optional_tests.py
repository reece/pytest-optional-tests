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


@pytest.mark.parametrize("config_style", [
    "ini",
    "toml_multiline",
    "toml_list",
    pytest.param(
        "native_toml",
        marks=pytest.mark.skipif(
            int(pytest.__version__.split(".")[0]) < 9,
            reason="Native TOML configuration requires pytest 9",
        ),
    ),
])
@pytest.mark.parametrize("requested,args,enabled", [
    ("", [], set()),
    ("opt1, opt2\nopt3", [], {"opt1", "opt2", "opt3"}),
    ("opt1 opt2", [], {"opt1", "opt2"}),
    ("opt1", ["--run-optional-tests=opt2"], {"opt2"}),
    ("opt1", ["--run-optional-tests=opt2 opt3", "--run-optional-tests=opt1,"],
     {"opt1", "opt2", "opt3"}),
])
def test_config_parsing(pytester, config_style, requested, args, enabled):
    definitions = ["", "  opt1: optional test 1", "   ",
                   "opt2: optional test 2", "opt3: optional test 3", ""]
    if config_style == "ini":
        pytester.makeini(
            "[pytest]\noptional_tests =\n    " + "\n    ".join(definitions)
            + "\nrun_optional_tests =\n    " + requested.replace("\n", "\n    ")
        )
    else:
        section = "tool.pytest" if config_style == "native_toml" else "tool.pytest.ini_options"
        if config_style == "toml_multiline":
            options = 'optional_tests = """\n' + "\n".join(definitions) + '\n"""\n'
            options += 'run_optional_tests = """\n' + requested + '\n"""\n'
        else:
            options = f"optional_tests = {definitions!r}\n"
            options += f"run_optional_tests = {requested.splitlines()!r}\n"
        pytester.makefile(".toml", pyproject=f"[{section}]\n{options}")
    pytester.makepyfile(test_config="""
        import pytest

        def test_unmarked():
            pass

        @pytest.mark.opt1
        def test_opt1():
            pass

        @pytest.mark.opt2
        def test_opt2():
            pass

        @pytest.mark.opt3
        def test_opt3():
            pass
    """)

    result = pytester.runpytest("-v", "--strict-markers", "-W", "error", *args)
    assert result.ret == 0
    result.assert_outcomes(passed=1 + len(enabled), skipped=3 - len(enabled))
    for marker in ("opt1", "opt2", "opt3"):
        status = "PASSED" if marker in enabled else "SKIPPED"
        result.stdout.fnmatch_lines([f"*test_config.py::test_{marker} {status}*"])


def test_skip_reason(pot_testdir):
    result = pot_testdir.runpytest("-rs")
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*Optional test; activate with `--run-optional-tests=`*"])
