#!/usr/bin/env python3
import docker, click, webbrowser, requests, json, time, re, os, sys, random
from operator import itemgetter
from pathlib import Path


os.system('clear')

# Placeholders
localhost = 'http://localhost'
image = None
tag = None
port = None
start = None
stop = None

client = docker.from_env()


# Generates a list of all dstools already on the system
imagesLocal = client.images.list()
downloadedDsTools = []
pattern = re.compile("afcai2c")
for images in imagesLocal:
    images = str(images).split(': ')[1: ]
    for i1 in images:
        i2 = i1.replace("'","").strip('>').split(',')
        for img in i2:
            img = img.split(':')[0]
            if pattern.search(img):
              downloadedDsTools.append(img)

# This list contains images to exclude from being displayed
excludedImages = [
    'afcai2c/ubi8',
    'afcai2c/python36',
    'afcai2c/python36-ai',
    'afcai2c/python38',
    'afcai2c/python38-ai',
    'afcai2c/python-r-ai',
    'afcai2c/jupyterlab',
    'afcai2c/r-base',
    'afcai2c/r-studio',
    'afcai2c/r-studio-valex',
    'afcai2c/tensorboard',
    'afcai2c/openjdk11'
    ]


### Dynamically Obtains docker images from Docker Hub (online)
### Note: the docker search feature isn't displaying all images within the afcai2c registry
# dsToolDict = client.images.search('afcai2c')
# dsToolDict = sorted(dsToolDict, key=itemgetter('name'))

dsToolDict = [
    {
        'name': 'afcai2c/jlab-eda', 'description': 'Jupyter Lab Exploratory Data Analysis AI/ML packages'
    }, 
    {
        'name': 'afcai2c/jlab-dl', 'description': 'Jupyter Lab with Deep Learning AI/ML packages'
    }, 
    {
        'name': 'afcai2c/jlab-cv', 'description': 'Jupyter Lab with Computer Vision AI/ML packages'
    }, 
    {
        'name': 'afcai2c/jlab-geo', 'description': 'Jupyter Lab with Geospatial AI/ML packages'
    }, 
    {
        'name': 'afcai2c/jlab-nlp', 'description': 'Jupyter Lab with Natural Language Processing AI/ML packages'
    }, 
    {
        'name': 'afcai2c/jlab-network', 'description': 'Jupyter Lab with networking AI/ML packages'
    }, 
    {
        'name': 'afcai2c/r-studio-eda', 'description': 'R Studio with Exploritory Data Analysis AI/ML packages'
    }, 
    {
        'name': 'afcai2c/r-studio-dl', 'description': 'R Studio with Deep Learning AI/ML packages'
    }, 
    {
        'name': 'afcai2c/r-shiny', 'description': 'R Shiny - Build interactive web applications that can execute R code'
    }, 
    {
        'name': 'afcai2c/dash', 'description': 'Ploty Dash - A Python framework for building reactive web-apps'
    }, 
    {
        'name': 'afcai2c/label-studio', 'description': 'Flexible data labeling tool -- Default username/password == username@coeus.mil / password'
    }, 
    {
        'name': 'afcai2c/superset', 'description': 'Apache Superset -- Business Intellligence tool for data exploration and visualization'
    }, 
    {
        'name': 'afcai2c/nginx', 'description': 'A web server that can also be used as a reverse proxy, load balancer, and more.'
    }, 
    {
        'name': 'afcai2c/metabase', 'description': 'Business Intelligence tool for data exploration and visualization'
    }
    ]
dsToolMenu = []
print("%-30s %-15s %s" %('Image Name','Downloaded','Description'))
for tool in dsToolDict:
    if tool['name'] not in excludedImages:
        if tool['name'] in downloadedDsTools:
            toolLine = "%-30s %-15s %s" %(tool['name'],True,tool['description'])
        else:
            toolLine = "%-30s %-15s %s" %(tool['name'],False,tool['description'])
        dsToolMenu.append(toolLine)
        print(toolLine)


containers = client.containers.list(all=True)


def dsToolsDetected():
    print("\nData Science tools detected:")
    print("%-35s %-20s %-20s %s" %('Image','ID','Status','Browser URL'))

    global runningTools
    runningTools = False
    global stoppedTools
    stoppedTools = False
    global lastRunningContainer
    lastRunningContainer = None
    global lastStoppedContainer
    lastStoppedContainer = None
    global containersMenu
    containersMenu = []

    for i in containers:
        c = str(i).split(':')[1].rstrip(">").strip()
        attrs = client.containers.get(c).attrs

        containerStatus = attrs['State']['Running']
        if containerStatus == True:
            showStatus = 'Running'
        elif containerStatus == False:
            showStatus = 'Not Running'

        showImage    = attrs['Config']['Image']
        showHostname = attrs['Config']['Hostname']

        portDict = {
            "jlab":"8888/tcp",
            "r-studio":"8787/tcp",
            "r-shiny":"3838/tcp",
            "dash":"8050/tcp",
            "nginx":"8080/tcp",
            "label-studio":"8080/tcp",
            "metabase":"3000/tcp",            
            "superset":"8088/tcp"
        }

        if containerStatus == True:
            image_name = re.search(r'(?<=afcai2c/)\w*', attrs['Config']['Image']).group()
            showUrl = attrs['HostConfig']['PortBindings'][portDict[image_name]][0]['HostPort']
            message = "%-35s %-20s %-20s http://localhost:%s" %(showImage,showHostname,showStatus,showUrl)
        elif  containerStatus == False:
            showUrl = 'The image is not running'
            message = "%-35s %-20s %-20s %s" %(showImage,showHostname,showStatus,showUrl)

        print(message)
        containersMenu.append(message)

        pattern = re.compile("^afcai2c/*")
        if pattern.match(attrs['Config']['Image']) and containerStatus == True :
            runningTools = True
            lastRunningContainer = attrs['Config']['Hostname']

        if pattern.match(attrs['Config']['Image']) and containerStatus == False:
            stoppedTools = True
            lastStoppedContainer = attrs['Config']['Hostname']

    if not runningTools and not stoppedTools:
            print("%-35s %-20s %-20s %s" %(None,None,None,None))
    return containersMenu

dsToolsDetected()

print('')



def startDsTool(image,tag,port):
    # Volume paths between localhost and tools 
    localhostHome = Path.home()
    dsToolsVolume = "{0}/dsTools".format(localhostHome)
    command = "mkdir -p {0}".format(dsToolsVolume)
    os.system(command)
    command = "chmod 777 {0}".format(dsToolsVolume)
    os.system(command)
    time.sleep(2)
    
    # Auto Ports
    if re.compile("jlab-").search(image):
        portContainer = 8888
    elif re.compile("r-studio").search(image):
        portContainer = 8787
    elif re.compile("dash").search(image):
        portContainer = 8787
    elif re.compile("shiny").search(image):
        portContainer = 8787
    elif re.compile("metabase").search(image):
        portContainer = 8787
    elif re.compile("label-studio").search(image):
        portContainer = 8787
    elif re.compile("superset").search(image):
        portContainer = 8787
    elif re.compile("nginx").search(image):
        portContainer = 8080
    else:
        print("Error...Unable to find the image's default port")

    imageName = "{0}:{1}".format(image,tag)

    # client = docker.APIClient(base_url='unix://var/run/docker.sock')
    # for line in client.pull(
    #     repository = 'afcai2c/jlab-eda',
    #     tag = tag,
    #     stream=True,
    #     decode=True):
    #     print(json.dumps(line, indent=4)['status'])

    tool = client.containers.run(
        image  = imageName,
        ports  = {portContainer:port},
        detach = True,
        volumes = {
            dsToolsVolume: {
                'bind': '/home/localhost/dsTools', 
                'mode': 'rw'
                },
            '/tmp': {
                'bind': '/home/localhost/tmp', 
                'mode': 'rw'}
            },
        working_dir = '/home'
        )
    launchUrl = "{0}:{1}".format(localhost,port)
    webbrowser.open(launchUrl)
    message = "\
\n[!] {0} will be hosted at: {1}\
\n\n[!] The following paths have been mounted within the tool:".format(image,launchUrl)
    print(message)
    print("    %-20s %-10s" %('localhost',"tool (" + image + ")"))
    print("    %-20s %-10s" %(localhostHome,"/home/localhost"))
    print("    %-20s %-10s" %("/tmp","/tmp/localhost"))

    return(tool)



promptImage  = "Enter the desired data science tool to start a new container with"
defaultImage = "afcai2c/jlab-eda"
promptTag    = "\nRun the latest build or specify the tag."
defaultTag   = "latest"
promptPort   = "   JupyterLab      8888\
\n   R-Studio        8787\
\n   Dash            8050\
\n   R-Shiny         3838\
\n   Label Studio    8080\
\n   Metabase        3000\
\n   SuperSet        8088\
\n   nginx (http)    8080\
\n   nginx (https)   8443"
defaultPort  = random.randrange(8000,9000)

@click.group()
@click.version_option("0.1.0")
def dsTools():
    """A Local Data Science Tool Manager"""
    try:
        client = docker.from_env()
    except:
        print("Docker is not isntalled! Visit https://docs.docker.com/get-docker/")
        quit()




@click.command()
@click.option(
    '--image', 
    prompt  = promptImage, 
    default = defaultImage,
    help    = 'Make a selection - each tools has AI/ML packages installed specifically their respetive purposes.'
    )
@click.option(
    '--tag',
    prompt  = promptTag,
    default = defaultTag,
    help    = 'The latest tag is normally your best option.'
    )
@click.option(
    '--port',
    prompt  = "\nList of the default tool ports: \
\n{0} \
\nEnter a port number to bind the tool too or accept random value:".format(promptPort),
    default = defaultPort,
    help    = "The tool will be accessible within the browser at http://localhost:[PORT]"
    )
@click.argument("staaaart", type=click.STRING, autocompletion=start)


def start(image,tag,port):
    startDsTool(image,tag,port)



@click.command()
def stop():
    if runningTools:
        message = "Enter the container ID of the tool to stop: [{0}] ".format(lastRunningContainer)
        containerID = str(input(message) or lastRunningContainer)
        containerSelected = client.containers.get(containerID)
        containerSelected.stop()
        quit()
    else:
        print('No data science tools are running.')


@click.command()
def resume():
    if stoppedTools:
        message = "[!] Enter the container ID of the tool to resume [{0}]: ".format(lastStoppedContainer)
        containerID = str(input(message) or lastStoppedContainer)
        containerSelected = client.containers.get(containerID)
        containerSelected.start()
        quit()


@click.command()
def remove():
    if lastStoppedContainer :
        message = "[!] Enter the container ID of the tool to remove [{0}]: ".format(lastStoppedContainer)
        containerID = str(input(message) or lastStoppedContainer)
        containerSelected = client.containers.get(containerID)
        containerSelected.remove()
    else:
        message = "[!] Enter the container ID of the tool to remove [{0}]: ".format(lastRunningContainer)
        containerID = str(input(message) or lastStoppedContainer)
        if runningTools == True:
            print("\n[!] Be sure to stop the running containers first!")
        #     message = "\n[!] Are you sure you want to remove the running container {0}? [False]: ".format(lastRunningContainer)
        #     verifyRemoval = str(input(message))
        #     if message == True:
        #         containerID = str(input(message) or lastStoppedContainer)
        #         containerSelected = client.containers.get(containerID)
        #         containerSelected.remove(force=True)
    quit()


@click.command()
def menu():
    try:
        from simple_term_menu import TerminalMenu    
    except:
        print("Need to install simple-term-menu:")
        print("   python -m pip install simple-term-menu")
        quit()

    # os.system('clear')
    print("Make a selection:")
    optionsMenu = [
        "Start         Start a new data science tool - new container", 
        "Resume        Resume a stopped tool so that it is now running", 
        "Launch        Launch a running tool, opens with default browser",
        "Stop          Stop an actively running tool",
        "Remove        Remove a tool that is not running",
        "Exit          Exits this menu"
    ]
    terminalMenu = TerminalMenu(optionsMenu)
    selectedMenuOption = terminalMenu.show()
    print('')
    print(f"You have selected:\n   {optionsMenu[selectedMenuOption]}!")
    print('')

    if re.compile("^Start").match(optionsMenu[selectedMenuOption]):
        ### Image Selection ###
        terminalToolSelection = TerminalMenu(dsToolMenu)
        selectedTool = terminalToolSelection.show()
        menuStartImage = str(dsToolMenu[selectedTool]).split(' ')[0]
        #menuStartImage = str(input("{0} [{1}]: ".format(promptImage,defaultImage)) or defaultImage)
        
        ### Tag Selection ###
        menuStartTag   = str(input("{0} [{1}]: ".format(promptTag,defaultTag)) or defaultTag)
        
        ### Port Selection ###
        print("\nSelect the default tool port or accept random port assignment:")
        promptPortList = promptPort.split("\n")
        randomPortStr = "   Random Port     {0}".format(defaultPort)
        promptPortList.insert(0,randomPortStr)
        terminalPortSelection = TerminalMenu(promptPortList)
        selectedPort = terminalPortSelection.show()
        menuStartPort = str(promptPortList[selectedPort]).strip(' ').split(' ')[-1]

        startDsTool(menuStartImage,menuStartTag,menuStartPort)
    else:        
        def showTools():
            os.system('clear')
            print("\nData Science tools detected:")
            print("%-35s %-20s %-20s %s" %('  Image','  ID','  Status','  Browser URL'))
            terminalContainerSelection = TerminalMenu(containersMenu)
            selectedContainer = terminalContainerSelection.show()
            
            toolContainer = str(containersMenu[selectedContainer]).strip(' ')
            containerID = re.split('\s+', toolContainer)[1]
            containerUrl = re.split('\s+', toolContainer)[-1]
            return containerID, containerUrl

        def refreshTools():
            os.system('clear')
            try:
                dsToolsDetected()
            except:
                pass
            # quit()


        if re.compile("^Resume").match(optionsMenu[selectedMenuOption]):
            print("Enter the container ID of the tool to resume: ")
            containerID = showTools()[0]
            containerSelected = client.containers.get(containerID)
            containerSelected.start()
            refreshTools()
            
        elif re.compile("^Launch").match(optionsMenu[selectedMenuOption]):
            print("Enter the container ID of the tool to launch: ")
            containerUrl = showTools()[1]
            print("Lauching the tool in the default browser: {0}".format(containerUrl))
            webbrowser.open(containerUrl)
            time.sleep(2)
            refreshTools()

        elif re.compile("^Stop").match(optionsMenu[selectedMenuOption]):
            print("Enter the container ID of the tool to stop: ")
            containerID = showTools()[0]
            containerSelected = client.containers.get(containerID)
            containerSelected.stop()
            refreshTools()

        elif re.compile("^Remove").match(optionsMenu[selectedMenuOption]):
            print()
            containerID = showTools()[0]
            containerSelected = client.containers.get(containerID)
            try:
                containerSelected.remove()
            except:
                print("\n[!] Stop the container before attempting removal.\n")
                time.sleep(2)
            refreshTools()

        elif re.compile("^Exit").match(optionsMenu[selectedMenuOption]):
            quit()

    # Reloads the memu
    os.execv(sys.argv[0], sys.argv)

dsTools.add_command(menu)
#dsTools.add_command(images)
#dsTools.add_command(tools)
dsTools.add_command(start)
dsTools.add_command(resume)
dsTools.add_command(stop)
dsTools.add_command(remove)


if __name__ == '__main__':
    dsTools()






