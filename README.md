# pytest-optional-tests

[![PyPI version](https://img.shields.io/pypi/v/pytest-optional-tests.svg)](https://pypi.org/project/pytest-optional-tests)

[![Python versions](https://img.shields.io/pypi/pyversions/pytest-optional-tests.svg)](https://pypi.org/project/pytest-optional-tests)

Enables the declaration of optional tests that are run only on request via the config file or command line

## Motivation

It is often useful to declare that certain tests that are run only when
requested, such as tests that are computationally expensive or slow, require
network access, or work only in certain environments.

This plugin enables certain markers to be declared as "optional test markers".
When tests are decorated with one or more optional test markers, the test is
skipped by default.  Optional tests may be enabled in the pytest ini file or the
command line.  Tests may be decorated with multiple markers, including multiple
optional markers.

## Installation

You can install "pytest-optional-tests" from [PyPI](https://pypi.org/project/pytest-optional-tests/):

    pip install pytest-optional-tests

## Usage

Optional markers must be declared in a [config
file](https://docs.pytest.org/en/stable/reference/customize.html) using the same
syntax as the markers option.  For example:

    [pytest]
    markers=
      regression: tests against previous bugs

    optional_tests=
      slow: slow tests
      network: network tests

Optional markers will be added to pytest's list of markers:

    $ pytest --markers
    regression: tests against previous bugs
    slow: slow tests
    network: network tests

Optional markers should NOT be declared using the `markers` config attribute,
even when using pytest's `strict` mode.

Optional test markers are pytest markers and the semantics are nearly
identical except that they cause a test to be skipped by default and run only when requested.  If a test is decorated with multiple optional markers, the test will be executed when *any* of the markers is requested. For
example:

    @pytest.mark.network
    @pytest.mark.slow
    def test_slow_network_function(): ...

will be tested if either or both of the optional `slow` or `network`
tests are requested.  Optional tests may be requested in pytest.ini:

    run_optional_tests=network,slow

or on the command line:

    pytest --run-optional-tests=network,slow

## Development

    python3 -m venv
    source venv/bin/activate
    uv pip install -U setuptools pip uv pytest
    uv pip install -e '.[dev]'

## Motivation and Design

Pytest [markers](https://docs.pytest.org/en/stable/reference/reference.html#marks) make it easy to run a subset of tests, but doesn't skip those tests. The pytest [skip](https://docs.pytest.org/en/stable/reference/reference.html#pytest-skip) and [skipif](https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif) marks provide skipping functionality, but such tests can't be re-enabled.  That is, a test that is marked with both `@pytest.mark.skip()` (or `skipif`) and `@pytest.mark.network` will *not* be run with `-m network`.

This plugin augments [pyteest markers](https://docs.pytest.org/en/stable/example/markers.html) functionality to provide for optional tests, which means that it inherits existing marker functionality, like listing declared markers and checking strictness.

Currently, there's one unfortunate consequence of this choice: an optional test is enabled ONLY with `--run-optional-test=` with an optional test name.  Specifically, `-m` does not enable a test when the argument is an optional test name OR is the name of another mark on the same test. Both of these could be addressed.

## License

Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license.

## Issues

If you encounter any problems, please [file an issue](https://github.com/reece/pytest-optional-tests/issues) along with a detailed description.
