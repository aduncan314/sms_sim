import json
from json import JSONDecodeError
from os import environ
from pathlib import Path

import yaml

from sms_sim.common import ConfiguredSettings, SingleSenderConfig, RuntimeEnv

DEFAULT_SETTINGS_FILE_PATH = Path(__file__).parent.parent.joinpath("run_config.yml")


def get_settings(cli_settings: dict) -> ConfiguredSettings:
    """
    Return setting for the project. Default values are overridden by (1) a
    config file, followed by (2) environment variables, and (3) variables set
    by CLI options.

    (1) Config file must be a yaml file named 'run_config.yml' found in the
        project root.
    (2) Environment variables are named using the form
        'SMS_SIM_<module>_<name>' where <module> is one of 'PRODUCER', 'SENDER',
        or 'MONITOR' based on the part of the program they effect. <name> is the
        name of the value in `ConfiguredSettings`.
    (3) CLI options are determined in the main file.

    Args:
        cli_settings: Dictionary of settings determined by CLI options
    """
    settings = _get_default_settings()

    settings = _file_override(settings)
    settings = _envvar_override(settings)
    settings = _clivar_override(settings, cli_settings)

    return settings


def _get_default_settings() -> ConfiguredSettings:
    return ConfiguredSettings(
        runtime_env=RuntimeEnv.LOCAL,
        message_count=1000,
        senders=[SingleSenderConfig(name="first", mean_wait_ms=10000, std_wait_ms=10, fail_rate=0.1)],
        monitor_period=5,
    )


def _file_override(
    settings: ConfiguredSettings,
    file_path: Path = DEFAULT_SETTINGS_FILE_PATH,
) -> ConfiguredSettings:
    try:
        file_settings = _read_settings_file(file_path)
    except FileNotFoundError:
        return settings

    sender_list = []
    for name, data in file_settings.get("senders", {}).items():
        data["name"] = name
        _sender = SingleSenderConfig(**{key: data[key] for key in vars(settings.senders[0]).keys()})
        sender_list.append(_sender)

    new_settings = ConfiguredSettings(
        runtime_env=file_settings.get("runtime_env", settings.runtime_env),
        message_count=file_settings.get("producer", {}).get("message_count", settings.message_count),
        monitor_period=file_settings.get("monitor", {}).get("monitor_period", settings.monitor_period),
        senders=sender_list if sender_list else settings.senders,
    )

    return new_settings


def _read_settings_file(file_path: Path) -> dict:
    with file_path.open("r") as f:
        file_settings = yaml.safe_load(f)

    return file_settings if file_settings is not None else {}


def _envvar_override(settings: ConfiguredSettings) -> ConfiguredSettings:
    sender_list = []
    try:
        for sender_info in json.loads(environ.get("SMS_SIM_SENDERS_LIST", "[]")):
            sender_list.append(SingleSenderConfig(**sender_info))
    except (KeyError, JSONDecodeError) as e:
        raise RuntimeError(
            f"Failed to correctly update sender configuration from environment variable 'SMS_SIM_SENDERS_LIST'."
        ) from e

    new_settings = ConfiguredSettings(
        runtime_env=environ.get("RUNTIME_ENV", settings.runtime_env),
        message_count=int(environ.get("SMS_SIM_PRODUCER_MESSAGE_COUNT", settings.message_count)),
        monitor_period=int(environ.get("SMS_SIM_MONITOR_PERIOD", settings.monitor_period)),
        senders=sender_list if sender_list else settings.senders,
    )

    return new_settings


def _clivar_override(settings: ConfiguredSettings, cli: dict) -> ConfiguredSettings:
    update_map = {k: (cli[k] if cli.get(k) is not None else getattr(settings, k)) for k in vars(settings)}
    return ConfiguredSettings(**update_map)
