# dstools_cli/cli.py

#!/usr/bin/env python3
import sys
import click
import webbrowser
import re
import time
import random
import os

from .docker_utils import (
    init_docker_client,
    ds_tools_detected,
    start_ds_tool,
    stop_ds_tool,
    resume_tool,
    remove_tool,
    pull_image
)
from .menu_utils import (
    ds_tool_terminal_menu,
    ds_tool_dict,
    ds_tool_menu,
    prompt_image,
    default_image,
    prompt_tag,
    default_tag,
    prompt_port,
    default_port,
    last_running_container,
    last_stopped_container,
    running_tools,
    stopped_tools,
)

# Initialize Docker client (and verify Docker is running)
client = init_docker_client()

@click.group()
def main():
    """Simple CLI tool using click to run Data Science containers."""
    pass

@main.command()
def menu():
    """Interactive, terminal-based menu."""
    ds_tools_detected(client)  # Print tools detected
    ds_tool_terminal_menu(client)

@main.command()
@click.option(
    "--image", 
    prompt=prompt_image, 
    default=default_image,
    help="Select which image to use from the Docker registry.",
)
@click.option(
    "--tag", 
    prompt=prompt_tag, 
    default=default_tag,
    help="Specify a tag (version) to run, defaults to 'latest'."
)
@click.option(
    "--port", 
    prompt=("\nList of default ports:\n" + prompt_port + 
            "\nEnter a port number to bind to (or accept random value)"),
    default=default_port,
    help="The container will be accessible at http://localhost:<port>."
)
def start(image, tag, port):
    """Start a new container with the specified image, tag, and port."""
    start_ds_tool(client, image, tag, port)

@main.command()
@click.option(
    "--id",
    prompt="Enter the ID of a running container/tool",
    default=last_running_container,
    help="Which container ID do you want to stop?"
)
def stop(id):
    """Stop a running container."""
    if running_tools:
        stop_ds_tool(client, id)
    else:
        click.echo("[!] No data science tools are running.")
    ds_tools_detected(client)

@main.command()
def resume():
    """Resume a stopped container."""
    if stopped_tools:
        resume_tool(client)
    else:
        click.echo("[!] No data science tools are stopped.")
    ds_tools_detected(client)

@main.command()
def remove():
    """Remove a stopped container."""
    remove_tool(client)

@main.command()
def pull():
    """Pull the latest version of a tool from Docker Hub."""
    pull_image()

if __name__ == "__main__":
    main()

