import click

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
