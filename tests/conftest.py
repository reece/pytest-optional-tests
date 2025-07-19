import pytest

pytest_plugins = (
    "pytester",               # adds pytester fixture to environment
    "pytest_optional_tests",  # tries import => fast fail if not importable
    )

@pytest.fixture(scope="function")
def pot_testdir(pytester: pytest.Pytester):
    """construct test directory"""
    for f in ["test_pot.py", "pytest.ini"]:
        pytester.copy_example(f)
    return pytester
