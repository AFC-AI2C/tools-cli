import click
from .commands import cmd1, cmd2

@click.group()
def main():
    """
    An example CLI using Click
    """
    pass

main.add_command(cmd1)
main.add_command(cmd2)
