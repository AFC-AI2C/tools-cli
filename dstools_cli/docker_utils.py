# dstools_cli/docker_utils.py
import docker
import os
import re
import time
import webbrowser
import random
import click

def init_docker_client():
    """Initialize the Docker client and ensure Docker is running."""
    try:
        client = docker.from_env()
        return client
    except Exception as e:
        click.echo("[!] Docker is not running or not installed!")
        click.echo("    Please ensure Docker is running or visit https://docs.docker.com/get-docker")
        raise SystemExit(e)


def ds_tools_detected(client):
    """Print out data science tools that are running or stopped."""
    # Example of reusing your old detection logic...
    containers = client.containers.list(all=True)
    click.echo("\nData Science tools detected:")
    click.echo(f"{'Image':35} {'ID':20} {'Status':20} URL")

    for c in containers:
        # process container
        # print info
        pass
    # etc.

def start_ds_tool(client, image, tag, port):
    """Start a Docker container."""
    # old startDsTool() logic here ...
    # e.g. create volumes, run the container, open web browser, etc.
    pass

def stop_ds_tool(client, container_id):
    """Stop a Docker container."""
    # old stopDsTool() logic ...
    pass

def resume_tool(client):
    """Resume a stopped container."""
    pass

def remove_tool(client):
    """Remove a container."""
    pass

def pull_image():
    """Pull a Docker image from Docker Hub."""
    pass
