# dstools_cli/menu_utils.py
import re
import random
from simple_term_menu import TerminalMenu

ds_tool_dict = [
    {"name": "afcai2c/vs-py-eda", "description": "..."},
    # ...
]
excluded_images = [ "afcai2c/ubi8", "afcai2c/python36", ... ]
ds_tool_menu = []
running_tools = False
stopped_tools = False
last_running_container = None
last_stopped_container = None

prompt_image = "Enter the desired data science tool to start a new container with"
default_image = "afcai2c/jlab-eda"
prompt_tag = "\nRun the latest build or specify a tag"
default_tag = "latest"
prompt_port = """\
   JupyterLab      8888
   Dash            8050
   Label Studio    8080
   Metabase        3000
   nginx (http)    8080
   nginx (https)   8443
   R-Studio        8787
   R-Shiny         3838
   VS Code         8080
"""
default_port = random.randrange(8000,9000)


def ds_tool_terminal_menu(client):
    # This is the old "menu()" logic that used a TerminalMenu
    # to present options to the user. 
    # e.g. "Start new container", "Resume", "Stop", etc.
    pass


