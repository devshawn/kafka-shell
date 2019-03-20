import pytest

from .context import kafkashell

test_data = [
    "0.0.1",
    "1.0.1",
    "2.3.4"
]


@pytest.mark.parametrize("test_input", test_data)
def test_get_version(test_input):
    old_version = kafkashell.version.__version__
    kafkashell.version.__version__ = test_input
    assert kafkashell.version.get_version() == test_input
    kafkashell.version.__version__ = old_version
