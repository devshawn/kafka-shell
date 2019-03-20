import mock

from tests.context import kafkashell
from tests.utilities import setup_config_path_for_test


@mock.patch("prompt_toolkit.application.current.get_app")
@mock.patch('kafkashell.config.get_user_config_path')
@mock.patch("kafkashell.settings.Settings.set_enable_help")
@mock.patch("kafkashell.settings.Settings.set_enable_fuzzy_search")
@mock.patch("kafkashell.settings.Settings.set_next_cluster")
def test_toolbar(mock_set_next_cluster, mock_set_enable_fuzzy_search, mock_set_enable_help, mock_config_path,
                 mock_get_app):
    mock_config_path.return_value = setup_config_path_for_test()
    bindings = kafkashell.bindings.get_bindings(kafkashell.settings.Settings())

    assert bindings.bindings is not None
    for binding in bindings.bindings:
        binding.handler({})
        key = binding.keys[0]

        if key == "f2":
            mock_set_next_cluster.assert_called_once()

        elif key == "f3":
            mock_set_enable_fuzzy_search.assert_called_once_with(False)

        elif key == "f9":
            mock_set_enable_help.assert_called_once_with(False)

        elif key == "f10":
            mock_get_app.assert_called_once()
            mock_get_app.return_value.exit.assert_called_once_with(exception=EOFError)
