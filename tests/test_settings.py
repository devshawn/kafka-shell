import mock
import oyaml as yaml

from .context import kafkashell


@mock.patch("kafkashell.config.save_config")
@mock.patch("kafkashell.config.get_completer")
@mock.patch("kafkashell.config.get_config")
@mock.patch("kafkashell.config.init_history")
@mock.patch("kafkashell.config.init_config")
def test_settings(mock_init_config, mock_init_history, mock_get_config, mock_get_completer, mock_save_config):
    with open("tests/data/test-config.yaml") as f:
        with open("tests/data/test-modified-config.yaml") as fm:
            config_json = yaml.safe_load(f)
            modified_json = yaml.safe_load(fm)
            mock_get_completer.return_value = {"commands": {}}
            mock_get_config.return_value = config_json

            # test init
            settings = kafkashell.settings.Settings()

            mock_init_config.assert_called_once()
            mock_init_history.assert_called_once()
            mock_get_config.assert_called_once()
            mock_get_completer.assert_called_once()
            assert settings.enable_help is True
            assert settings.enable_auto_complete is True
            assert settings.enable_auto_suggest is True
            assert settings.cluster == "local"

            # test set_enable_help
            settings.set_enable_help(False)
            assert settings.enable_help is False

            # test set_enable_fuzzy_search
            settings.set_enable_fuzzy_search(False)
            assert settings.enable_fuzzy_search is False

            # test set_next_cluster & get_cluster_details
            settings.set_next_cluster()
            assert settings.cluster == "test"
            assert settings.get_cluster_details() == config_json["clusters"]["test"]

            # test save_settings
            settings.save_settings()
            mock_save_config.assert_called_once_with(modified_json)

            # test save_settings when enableSaveOnExit is false
            mock_save_config.reset_mock()
            settings.enable_save_on_exit = False
            settings.save_settings()
            assert not mock_save_config.called

            # test things can change back
            settings.set_enable_help(True)
            assert settings.enable_help is True

            settings.set_enable_fuzzy_search(True)
            assert settings.enable_fuzzy_search is True

            settings.set_next_cluster()
            assert settings.cluster == "local"
            assert settings.get_cluster_details() == config_json["clusters"]["local"]


@mock.patch("kafkashell.config.get_completer")
@mock.patch("kafkashell.config.get_config")
@mock.patch("kafkashell.config.init_history")
@mock.patch("kafkashell.config.init_config")
def test_settings_init_history_off(mock_init_config, mock_init_history, mock_get_config, mock_get_completer):
    with open("tests/data/test-history-off-config.yaml") as f:
        config_json = yaml.safe_load(f)
        mock_get_completer.return_value = {"commands": {}}
        mock_get_config.return_value = config_json

        # test init
        kafkashell.settings.Settings()

        mock_init_config.assert_called_once()
        mock_init_history.assert_not_called()
