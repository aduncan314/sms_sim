# SMS Simulator

## Andrew Duncan interview project

This

## Setup

This project uses `poetry` to manage dependencies. Assuming `poetry` is in stalled, in the project root run

```bash
poetry install
```

### Configurations

Runtime configurations can be set in "run_config.yml". An example configurations is shown in "example_run_config.yml".

This project will run without any configurations being set, however, configuring more than one "sender" requires
configuration. None of the top level blocks are required, but all three values, `fail_rate`, `mean_wait_ms`, and
`std_wait_ms` must be set for any "sender" added.

## Run

To run the project, run

```bash
poetry run sms_sim run-local
```

Further documentation about options can by found by running

```bash
poetry run python sms_sim run-local --help
```

## Tools used

