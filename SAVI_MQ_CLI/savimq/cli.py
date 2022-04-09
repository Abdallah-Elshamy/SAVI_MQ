from textwrap import indent
from typing import Optional
import typer
from . import __app_name__, __version__
import json

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from savi import launch_mq, list_mqs, delete_mq, get_mq_info

app = typer.Typer()


@app.command()
def launch(
    config_file_path : str = typer.Argument(...),
) -> None:
    """Launches an MQ from a JSON config file."""
    try:
        f = open(config_file_path, "r")
        config = json.loads(f.read())
        launch_mq(config)
        typer.echo("MQ Launched")
    except IOError:
        typer.secho(
            'Could not open the specified file',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    except ValueError:
        typer.secho(
            'The specified config file does not contain valid JSON',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    except:
        typer.secho(
            'An error occured.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    finally:
        f.close()


@app.command()
def list() -> None:
    """Lists the existing MQs"""
    try:
        mqs = list_mqs()
        typer.secho("\nInstances:\n", fg=typer.colors.BLUE, bold=True)
        columns = [
            "Name          ", 
            "| Endpoint           ",
            "| Dashboard URL              ",
            "| Flavor            ",
            "| Key Pair        ",
            "| Engine          ",
            "| Status         ",
        ]
        headers = "".join(columns)
        typer.secho(headers, fg=typer.colors.BLUE, bold=True)
        typer.secho("-" * len(headers), fg=typer.colors.BLUE)
        for mq in mqs:
            typer.secho(
                f"{mq['Name']}{(len(columns[0]) - len(mq['Name'])) * ' '}"
                f"| {mq['Endpoint']}{(len(columns[1]) - len(mq['Endpoint']) - 2) * ' '}"
                f"| {mq['DashboardURL']}{(len(columns[2]) - len(mq['DashboardURL']) - 2) * ' '}"
                f"| {mq['Flavor']}{(len(columns[3]) - len(mq['Flavor']) - 2) * ' '}"
                f"| {mq['KeyPair']}{(len(columns[4]) - len(mq['KeyPair']) - 2) * ' '}"
                f"| {mq['Engine']}{(len(columns[5]) - len(mq['Engine']) - 2) * ' '}"
                f"| {mq['Status']}",
                fg=typer.colors.BLUE,
            )
        typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)
    except:
        typer.secho(
            'An error occured.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def info(
    mq : str = typer.Argument(...),
) -> None:
    """Prints detailed information about an MQ."""
    try:
        server_info = json.dumps(get_mq_info("mq-" + mq), indent=4)
        if server_info != "null\n":
            typer.secho(server_info, fg=typer.colors.BLUE)
        else:
            typer.secho(
                'There is no mq with the given name/id',
                fg=typer.colors.RED,
            )
    except:
        typer.secho(
            'An error occured.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def delete(
    id : str = typer.Argument(...),
) -> None:
    """Deletes the MQ with the given ID"""
    try:
        delete_mq(id)
    except:
        typer.secho(
            'An error occured.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show savimq's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return