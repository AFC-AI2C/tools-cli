import docker

#first need to check if we have docker installed and running
try:
    client = docker.from_env()
except:
    print("[!] Docker is not running or is not installed!\n[!] Please ensure Docker is running or visit https://docs.docker.com/get-docker\n")
    quit()