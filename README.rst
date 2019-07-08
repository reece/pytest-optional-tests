=====================
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

Pytest plugin that supports easy declaration of optional
tests. Optional tests are run only on request.

Example:

```
@optional.network
@optional.longrunning
def test_this():
    assert False
```

----

Requirements
------------

* pytest > 3.5.0


Installation
------------

You can install "pytest-optional-tests" via `pip`_ from `PyPI`_::

    $ pip install pytest-optional-tests


Usage
-----

* TODO


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.



This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/reece/pytest-optional-tests/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
