#!/usr/bin/env python
from email import header
from json import tool
from operator import itemgetter
from time import sleep
from typing import Any
import docker, webbrowser, click, re
from pandas import notnull
from tabulate import tabulate
import os

client = docker.from_env()
localhost = "http://localhost"
image     = None
tag       = "latest"
port      = None

def startTool(image,tag,port):
    imageName = "{0}:{1}".format(image,tag)
    print('Container Started')
    tool = client.containers.run(imageName, ports={port:port}, detach=True)
    sleep(4)
    launchUrl = "{0}:{1}".format(localhost,port)
    webbrowser.open(launchUrl)
    return(tool)
@click.group()
@click.version_option("0.1.0")
def ds():
    """A Local Data Science Tool Manager"""
    try:
        client = docker.from_env()
    except:
        print("Docker is not installed! Visit https://docs.docker.com/get-docker/")

@click.command()
def menu():
    """Lists the DS Tools"""
    #d=[[1,'afcai2c/jlab-cv'],[2,'afcai2c/jlab-eda']]
    #print(tabulate(d,headers=["S. No.", "Data Science Tool Name"]))
    excluded_containers=['afcai2c/openjdk11','afcai2c/studio.ai','afcai2c/jlab-nlp','afcai2c/r-studio-valex']
    tools_list=client.images.search('afcai2c')
    tools_list=sorted(tools_list,key=itemgetter('name'))
    for ds_tools in tools_list:
        if ds_tools['name'] not in excluded_containers:
            print(ds_tools['name'])


@click.command()
#@click.argument('ToolID')
def CallTool():
    """Start the Tool"""
    #print("Please Enter the Tool Name")
    toolname=click.prompt('Please enter a tool name',default=Any)
    #print("Please Provide the Port")
    #port=input()
    port=click.prompt('Please Provide the Port', default=Any)
    print(toolname)
    startTool(toolname,tag,port)

@click.command()
def containers_running():
    """Lists the Docker Containers Actively Running"""
    containers=client.containers.list()
    print(containers)
    #for container in client.containers.list():
     #   print(container.id)

@click.command()
def container_stop_all():
    """Be Careful! This Command Will Stop All the Containers"""
    if (client.containers.list(filters={'status':'running'})):
        print("Following containers are running")
        print(client.containers.list())
        if click.confirm('Are You Sure You Want To Stop All Containers?'):
           for container in client.containers.list():
                container.stop()
                click.echo("Containers Stopped")
               
    else:
        print("No Containers are Running")

@click.command()
def stop_tools():
    """Prompts User to Stop and Remove the Docker Containers"""
    print("Following Containers are Running: ")
    containers=client.containers.list()
    print(containers)
    containerid=click.prompt('Please Provide the Container Id:',default=Any)
    containerstop=client.containers.get(containerid)
    containerstop.stop()  
    print("Container Stopped")  
    if click.confirm('Do You also Want to Remove Containers?'):
        #container_removeid=click.prompt('Please Provide the Container Id to remove',default=Any)
        containerremove=client.containers.get(containerid)
        containerremove.remove()
        print("Container Removed!!") 
    

@click.command()
def pull_dstool():
    """Use this Command to Pull DS Tools Containers Locally"""
    toolname=str(click.prompt('Enter the DS Tool Name:',default=any))
    pull=client.images.pull(toolname)
def complete_env_vars(ctx,param,incomplete):
    return[k for k in os.environ if k.startswith(incomplete)]
@click.command()
@click.argument("name", shell_complete=complete_env_vars)
def local_docker_images(name):
    #click.echo(f"Name:{name}")
    #click.echo(f"Value:{os.environ[name]}")
    """This Command Shows Local Docker Images"""
    print(client.images.list())

ds.add_command(menu)
ds.add_command(CallTool)
ds.add_command(containers_running)
ds.add_command(stop_tools)
ds.add_command(container_stop_all)
ds.add_command(pull_dstool)
ds.add_command(local_docker_images)
if __name__ == '__main__':
    ds()

