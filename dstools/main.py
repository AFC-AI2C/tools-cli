import docker, click, webbrowser, requests, json, time, re, os, sys, random
from operator import itemgetter
from pathlib import Path
from menu import menu
from start import start
from resume import resume
from stop import stop
from remove import remove

@click.group()
def main():
    """A CLI to start data science environments"""
    pass

main.add_command(menu)
main.add_command(start)
main.add_command(resume)
main.add_command(stop)
main.add_command(remove)

if __name__ == '__main__':
    main()
