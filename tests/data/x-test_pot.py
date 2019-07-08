import pytest

def test_no_mark():
    pass

@pytest.mark.opt1
def test_opt1():
    pass

@pytest.mark.opt1
@pytest.mark.opt2
def test_opt12():
    pass

@pytest.mark.opt2
def test_opt2():
    pass

@pytest.mark.opt3
def test_opt3():
    pass

@pytest.mark.other
def test_other():
    pass

