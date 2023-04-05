# tools-cli
BLUF: A simple cli utility to launch data science tools locally.

This is designed to be ran from an Linux host or within Windows Subsystem for Linux (WSL).
This python script allows you to pull, launch, and manage various AI/ML tools with currated packages installed sepcific to the intended application's use case.

----------

## How to install required python libraries
pip install -r ./requirements.txt

## How to have the UI automatically launch with default browser
sudo apt install xdg-utils -y
 
----------

## How to run the script

./launch-dsTools.py menu

----------

## General Guide

The menu option will provided you a listing of the avialable data science tools for use, a status if they hav been downloaded, and a brief description. Below the images will be a listing of any detected dsTool images running or stopped.

![Alt text](https://github.com/AFC-AI2C/tools-cli/blob/main/images/screenshot01.jpg)

After you click on start and select a tool to use, you will be prompted with a local port to map it with. A listing of the default tool ports are availabe if you want to do a direct mapping, but do note that you cannot mape any single local port more than once. The default option though is to use a random port.

![Alt text](https://github.com/AFC-AI2C/tools-cli/blob/main/images/screenshot02.jpg)

When a tool is slected to start, it will check if it exists locally. If not, it will download it and provided you the status of the docker image pull.

![Alt text](https://github.com/AFC-AI2C/tools-cli/blob/main/images/screenshot03.jpg)

After the tool has been started, it will provided you a listing of mapped volume locations to the localhost. The various dsTools will have common mapped locations to the localhost to facilitate access to local files and inter-container file sharing. Also, the default browser will be automatically launched to the provide access to the tool.

![Alt text](https://github.com/AFC-AI2C/tools-cli/blob/main/images/screenshot04.jpg)

Notice that within the "Data Science tools detected" section the status if the tool is running or not, as well as a URL you can click on for running images to launch it via the default browser. Lastly, aside from selecting Start for new tools, you can Stop existing running ones, or Resume/Remove any stopped tools.

![Alt text](https://github.com/AFC-AI2C/tools-cli/blob/main/images/screenshot05.jpg)


###  resources used
* [Article for Python Package](https://towardsdatascience.com/how-to-build-and-publish-command-line-applications-with-python-96065049abc1)
* [Article with CLI examples](https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df)
* [Another good article](https://www.davidfischer.name/2017/01/python-command-line-apps/)
