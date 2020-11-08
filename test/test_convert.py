from python_config import convert


def test_convert():
    assert convert({
        "x": 1,
        "y": ["str"],
        "z": {"key": "value"},
        "f": {"type": "func", "arg0": "arg0"}
    }) == """x = 1
y = ['str']
z = {'key': 'value'}
f = func(arg0='arg0',)
"""
