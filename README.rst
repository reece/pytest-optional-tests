pytest-optional-tests
=====================

.. image:: https://img.shields.io/pypi/v/pytest-optional-tests.svg
    :target: https://pypi.org/project/pytest-optional-tests
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-optional-tests.svg
    :target: https://pypi.org/project/pytest-optional-tests
    :alt: Python versions

.. image:: https://travis-ci.org/reece/pytest-optional-tests.svg?branch=master
    :target: https://travis-ci.org/reece/pytest-optional-tests
    :alt: See Build Status on Travis CI


Provides easy declaration of optional tests using pytest markers.
Optional tests are run only on request via the config file or command
line.

----

Motivation
----------

Some classes of tests should not be run with every test invocation.
It is often useful to define tests that be run only when specifically
requested, such as tests that are slow, require network access, or
work only in certain environments.

Pytest provides mechanisms to run tests based on test names (`-k`) and
to filter tests based on markers (`-m`).  Neither mechanism makes it
easy to surpress certain tests by default.  For example, one might
decorate tests with `@pytest.mark.network`, but disabling it by
default requires a marker expression like `-m "not network"` with
every invocation.  Markers and marker expressions become unwieldy when
there are many markers.

This plugin enables users to declare that certain markers are
"optional markers".  When tests are decorated with an optional marker,
the test is skipped by default.  Tests may be decorated with multiple
markers, including multiple optional markers.  Optional tests may be
enabled in the pytest ini file or the command line.


Installation
------------

You can install "pytest-optional-tests" via `pip`_ from `PyPI`_::

    $ pip install pytest-optional-tests


Usage
-----

Optional markers must be declared in inicfg using the same syntax as
the markers option.  For example::

  [pytest]
  markers:
    regression: tests against previous bugs
 
  optional_tests:
    slow: slow tests
    network: network tests

Optional markers will be added to pytest's list of markers::

  $ pytest --markers
  regression: tests against previous bugs
  slow: slow tests
  network: network tests

Optional markers should NOT be declared using the `markers` attribute,
even when using pytest's `strict` mode.
 
Optional test decorators are pytest markers, and the semantics are
identical.  If a test is decorated with multiple optional markers, the
test will be executed when *any* of the markers is requested. For
example::

  @pytest.mark.network
  @pytest.mark.slow
  def test_slow_network_function(): ...

will be tested if either or both of the optional `slow` or `network`
tests are requested.

Optional tests may be requested in the inicfg::

  [pytest]
  markers:
    regression: tests against previous bugs
 
  optional_tests:
    slow: slow tests
    network: network tests
  
  run_optional_tests=network,slow

or on the command line::

  pytest --run-optional-tests=network,slow



License
-------

Distributed under the terms of the `MIT`_ license.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/reece/pytest-optional-tests/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project/pytest-optional-tests/
