from math_utilities import add

def test_add1():
    assert add(3, 5) == 8

def test_add2():
    assert add(-1, -4) == -5

def test_add3():
    assert add(-0.5, 0.5) == 0
