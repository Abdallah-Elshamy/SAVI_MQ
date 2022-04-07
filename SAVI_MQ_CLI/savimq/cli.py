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