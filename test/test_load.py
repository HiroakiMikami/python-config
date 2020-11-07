import io

from python_config import load


def test_load():
    assert load(io.StringIO("x = 1")) == {"x": 1}
