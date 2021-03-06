import os
import shutil

import pytest
pytest_plugins = 'pytester'



@pytest.fixture(scope="function")
def pot_testdir(testdir, tmpdir):
    basedir = os.path.dirname(__file__)
    datadir = os.path.join(basedir, "data")
    for f in ["test_pot.py", "pytest.ini"]:
        src = os.path.join(datadir, "x-" + f)
        dst = os.path.join(str(testdir), f)
        shutil.copy(src, dst)
    return testdir
