# tasks.py
import click


@click.group()
def cli():
    pass


@cli.command()
def lint():
    """Roda flake8."""
    import subprocess

    subprocess.run(["flake8", "app", "tests"])


@cli.command()
def format():
    """Roda black."""
    import subprocess

    subprocess.run(["black", "app", "tests"])


@cli.command()
def test():
    """Roda pytest."""
    import subprocess

    subprocess.run(["pytest", "-v"])


@cli.command()
def run():
    """Roda uvicorn."""
    import subprocess

    subprocess.run(["uvicorn", "main:app", "--reload"])


if __name__ == "__main__":
    cli()
