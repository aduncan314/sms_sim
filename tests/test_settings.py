from pathlib import Path

from sms_sim import common
from sms_sim import settings


def create_default_settings():
    return common.ConfiguredSettings(
        runtime_env=common.RuntimeEnv.LOCAL,
        monitor_period=100,
        message_count=99,
        senders=[common.SingleSenderConfig(name="default_sender", mean_wait_ms=1000, std_wait_ms=100, fail_rate=0.1)],
    )


def test_default_settings():
    default = create_default_settings()

    assert isinstance(default, common.ConfiguredSettings)
    assert len(default.senders) > 0  # Cascading functions expect not empty
    assert all([v is not None for v in vars(default)])


def test_file_does_not_exist():
    default = create_default_settings()

    non_existent_file = Path("THIS_BETTER_NOT_EXIST.jpg")
    if non_existent_file.exists():
        raise RuntimeError(f'In order to run tests, remove file "{non_existent_file.resolve()}".')

    assert settings._file_override(default, non_existent_file) == default


def test_file_update(monkeypatch):
    full_contents = {
        "runtime_env": "local",
        "producer": {"message_count": 1},
        "senders": {"first": {"fail_rate": 0, "mean_wait_ms": 100, "std_wait_ms": 10}},
        "monitor": {"monitor_period": 10},
    }

    monkeypatch.setattr(settings, "_read_settings_file", lambda x: full_contents)

    default = create_default_settings()
    updated = settings._file_override(default)

    assert default.message_count != updated.message_count, "test definition mistake"
    assert updated.message_count == 1

    # Updates values in file and leaves others untouched
    partial_contents = {"producer": {"message_count": 2}}
    monkeypatch.setattr(settings, "_read_settings_file", lambda x: partial_contents)
    updated = settings._file_override(default)

    assert updated.message_count == 2


def test_envars(monkeypatch):
    monkeypatch.setenv("SMS_SIM_PRODUCER_MESSAGE_COUNT", "4")
    monkeypatch.setenv(
        "SMS_SIM_SENDERS_LIST", '[{"name": "testing_sender", "mean_wait_ms": 0, "std_wait_ms": 0, "fail_rate": 1}]'
    )

    default = create_default_settings()
    updated = settings._envvar_override(default)

    assert default.message_count != updated.message_count, "test definition mistake"
    assert updated.message_count == 4
    assert updated.senders[0].mean_wait_ms == 0
    assert updated.senders[0].std_wait_ms == 0
    assert updated.senders[0].fail_rate == 1


def test_cli():
    # TODO: This is not sufficient to actually test the CLI, just the update function
    default = create_default_settings()
    updated = settings._clivar_override(default, {"message_count": 93})

    assert default.message_count != updated.message_count, "test definition mistake"
    assert updated.message_count == 93
