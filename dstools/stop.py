import docker, click, webbrowser, requests, json, time, re, os, sys, randomfrom operator import itemgetterfrom pathlib import Pathfrom simple_term_menu import TerminalMenu  
import docker, click, webbrowser, requests, json, time, re, os, sys, randomfrom operator import itemgetterfrom pathlib import Pathfrom simple_term_menu import TerminalMenu  
def stopDsTool():
    containerID = selectTools()[0]
def stop(id):
    if runningTools:
