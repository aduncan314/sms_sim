import click

from sms_sim.controller import LocalSenderController
from sms_sim.settings import get_settings


@click.group()
def cli():
    pass


@cli.command()
@click.option("--producer-count", "message_count", type=int)
@click.option("--sender-fail-rate", "fail_rate", type=float)
@click.option("--sender-mean-wait", "mean_wait_ms", type=int)
@click.option("--sender-std-wait", "std_wait_ms", type=int)
def run_local(**kwargs):
    settings = get_settings(kwargs)

    controller = LocalSenderController(settings)
    controller.submit_messages()
    controller.run()


if __name__ == "__main__":
    cli()
