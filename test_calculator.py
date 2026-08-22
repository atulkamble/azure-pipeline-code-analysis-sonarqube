from calculator import add, divide


def test_add():
    assert add(10, 20) == 30


def test_divide():
    assert divide(10, 2) == 5
