import click

from controller import LocalSenderController


@click.group()
def cli():
    pass


@cli.command()
def run_local():
    temp_config = {
        "senders": [
            {
                "name": "first",
                "args": {"mean_wait_ms": 10000, "std_wait_ms": 100, "fail_rate": 0.1},
            },
            {
                "name": "second",
                "args": {"mean_wait_ms": 10000, "std_wait_ms": 100, "fail_rate": 0.1},
            },
            {
                "name": "third",
                "args": {"mean_wait_ms": 10000, "std_wait_ms": 100, "fail_rate": 0.1},
            },
            {
                "name": "fourth",
                "args": {"mean_wait_ms": 10000, "std_wait_ms": 100, "fail_rate": 0.1},
            },
        ]
    }
    controller = LocalSenderController(temp_config)
    controller.submit_messages()
    controller.run()


if __name__ == "__main__":
    cli()
