import click, re
from simple_term_menu import TerminalMenu

def dsToolTerminalMenu():
    # # os.system('clear')
    print("Make a selection:")
    global optionsMenu
    optionsMenu = [
        "Start         Start a new data science tool - new container", 
        "Resume        Resume a stopped tool so that it is now running", 
        "Launch        Launch a running tool, opens with default browser",
        "Stop          Stop an actively running tool",
        "Remove        Remove a tool that is not running",
        "Pull          Pull the latest version of a tool from Docker Hub",
        "Exit          Exits this menu"
    ]
    terminalMenu = TerminalMenu(optionsMenu)
    global selectedMenuOption
    selectedMenuOption = terminalMenu.show()

@click.command()
def menu():
    dsToolTerminalMenu()
    print('')
    print(f"You have selected:\n   {optionsMenu[selectedMenuOption]}!")
    print('')
    print("  Image Name                     Downloaded      Description")

    if re.compile("^Start").match(optionsMenu[selectedMenuOption]):
        ### Image Selection ###
        terminalToolSelection = TerminalMenu(dsToolMenu)
        selectedTool = terminalToolSelection.show()
        menuStartImage = str(dsToolMenu[selectedTool]).split(' ')[0]
        #menuStartImage = str(input("{0} [{1}]: ".format(promptImage,defaultImage)) or defaultImage)
        
        ### Tag Selection ###
        menuStartTag   = str(input("{0} [{1}]: ".format(promptTag,defaultTag)) or defaultTag)
        
        ### Port Selection ###
        print('')
        print("Select the default tool port or accept random port assignment.")
        print("This will be the local port mapped to the one within the container.")
        print("Note: You cannot map any single local port more than once.")
        promptPortList = promptPort.split("\n")
        randomPortStr = "   Random Port     {0}".format(defaultPort)
        promptPortList.insert(0,randomPortStr)
        terminalPortSelection = TerminalMenu(promptPortList)
        selectedPort = terminalPortSelection.show()
        menuStartPort = str(promptPortList[selectedPort]).strip(' ').split(' ')[-1]

        startDsTool(menuStartImage,menuStartTag,menuStartPort)
    else:        
        if re.compile("^Resume").match(optionsMenu[selectedMenuOption]):
            print("Enter the container ID of the tool to resume: ")
            containerID = selectTools()[0]
            containerSelected = client.containers.get(containerID)
            containerSelected.start()
            # print(containerID)
            # print(containerSelected)
            refreshTools()
            
        elif re.compile("^Launch").match(optionsMenu[selectedMenuOption]):
            print("Enter the container ID of the tool to launch: ")
            containerUrl = selectTools()[1]
            print("Lauching the tool in the default browser: {0}".format(containerUrl))
            webbrowser.open(containerUrl)
            time.sleep(2)
            refreshTools()

        elif re.compile("^Stop").match(optionsMenu[selectedMenuOption]):
            print("Enter the container ID of the tool to stop: ")
            stopDsTool()
            refreshTools()

        elif re.compile("^Remove").match(optionsMenu[selectedMenuOption]):
            print()
            containerID = selectTools()[0]
            containerSelected = client.containers.get(containerID)
            try:
                containerSelected.remove()
            except:
                print("\n[!] Stop the container before attempting removal.\n")
                time.sleep(2)
            refreshTools()

        elif re.compile("^Pull").match(optionsMenu[selectedMenuOption]):
            print()
            ### Image Selection ###
            terminalToolSelection = TerminalMenu(dsToolMenu)
            selectedTool = terminalToolSelection.show()
            menuStartImage = str(dsToolMenu[selectedTool]).split(' ')[0]
            
            print('#############################')
            print(menuStartImage)
            print('#############################')
            # pull the image
            command = "docker pull {0}:{1}".format(menuStartImage,defaultTag)
            os.system(command)

        elif re.compile("^Exit").match(optionsMenu[selectedMenuOption]):
            quit()

    # Reloads the memu
    os.execv(sys.argv[0], sys.argv)
