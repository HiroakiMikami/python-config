import pytest

from python_config import parse


def test_constant():
    assert parse("x = 10") == {"x": 10}
    assert parse("x = 'y'") == {"x": 'y'}
    assert parse("x = True") == {"x": True}
    assert parse("x = None") == {"x": None}
    assert parse("x = ...") == {"x": Ellipsis}
    assert parse("x = \"\"\"\nfoobar\n\"\"\"") == {"x": "\nfoobar\n"}
    assert parse("x = (\"foo\"\n     \"bar\")") == {"x": "foobar"}
    assert parse("x = -10") == {"x": -10}


def test_reference():
    assert parse("x = 10\ny = x") == {"x": 10, "y": "@/x"}
    assert parse("x = 10\ny = x.y") == {"x": 10, "y": "@/x.y"}
    assert parse("x = 10\ny = x/y") == {"x": 10, "y": "@/x/y"}


def test_function_call():
    assert parse("x = foo()") == {"x": {"type": "foo"}}
    assert parse("x = foo(arg=0, arg2=y, arg3=bar())") == {
        "x": {"type": "foo", "arg": 0, "arg2": "@/y", "arg3": {"type": "bar"}}
    }


def test_collections():
    assert parse("x = [1, y]") == {"x": [1, "@/y"]}
    assert parse("x = {'y': 1}") == {"x": {"y": 1}}


def test_unsupported_python():
    with pytest.raises(RuntimeError):
        parse("x = 1 + 1")
