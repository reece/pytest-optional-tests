import pytest

def test_unmarked():
    """test for unmarked functions"""
    pass

@pytest.mark.marked
def test_marked():
    """test for running function marked with non-optional marks"""
    pass

@pytest.mark.opt1
def test_opt1():
    """test for running when opt1 mark is specified"""
    pass

@pytest.mark.opt2
@pytest.mark.marked
def test_opt2_marked():
    """test for running when opt2 mark is specified"""
    pass

@pytest.mark.marked
@pytest.mark.opt3
def test_marked_opt3():
    """test for running when opt3 mark is specified"""
    pass

@pytest.mark.opt1
@pytest.mark.opt2
def test_opt12():
    """test for running when opt1 and/or opt2 marks are specified"""
    pass

