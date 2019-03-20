import mock
import pytest

from .context import kafkashell

test_data = [
    ("local", True, True),
    ("local", False, False),
    ("test-cluster", True, True),
    ("123-cluster", False, False),
]


@mock.patch("kafkashell.settings.Settings")
@pytest.mark.parametrize("cluster,enable_help,enable_fuzzy", test_data)
def test_toolbar(mock_settings, cluster, enable_help, enable_fuzzy):
    settings = mock_settings.return_value
    settings.cluster = cluster
    settings.enable_help = enable_help
    settings.enable_fuzzy_search = enable_fuzzy

    toolbar = kafkashell.toolbar.Toolbar(settings)

    assert toolbar.handler() == [
        ('class:bottom-toolbar', " [F2] Cluster: "),
        ('class:bottom-toolbar-yellow', cluster),
        ('class:bottom-toolbar', " "),
        ('class:bottom-toolbar', "[F3] Fuzzy: "),
        ('class:bottom-toolbar-yellow', "ON" if enable_fuzzy else "OFF"),
        ('class:bottom-toolbar', " "),
        ('class:bottom-toolbar', "[F9] In-Line Help: "),
        ('class:bottom-toolbar-yellow', "ON" if enable_help else "OFF"),
        ('class:bottom-toolbar', " "),
        ('class:bottom-toolbar', "[F10] Exit")
    ]
