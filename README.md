# SMS Simulator

## Andrew Duncan interview project

>[!WARNING]
>This project contains a Dockerfile, but running directly is recommended due to issues with multiple processes running.

This is a PoC program written to run on a single machine. While this could be written in fewer lines of code, the components have been broken out so that splitting onto AWS (or similar) infrastructure would be simple.

In a number of places, decisions were made explicitly to facilitate a future use where each component runs on its own without the `LocalController` object managing the queues.

## Setup

This project uses `poetry` to manage dependencies. Assuming `poetry` is in stalled, in the project root run:

```bash
poetry install
```

### Configurations

Runtime configurations can be set in "run_config.yml". An example configurations is shown in "example_run_config.yml".

This project will run without any configurations being set, however, configuring more than one "sender" requires configuration. None of the top level blocks are required, but all three values, `fail_rate`, `mean_wait_ms`, and `std_wait_ms` must be set for any "sender" added.

## Run

To run the project, run:

```bash
poetry run sms-simulate run-all
```

Further documentation about options can be found by running

```bash
poetry run python sms-simulate run-all --help
```

## Tools used

- PyCharm (I rely on tab completion but have "AI" recommendations turned off)
- Python Docs
- Stack Overflow (no specific snippets)
