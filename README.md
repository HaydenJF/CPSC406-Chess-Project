# CPSC406-Chess-Project <br/>
## Running the program
### After cloning the repo cd into the folder:
    cd CPSC406-Chess-Project
### Then you need to download docker:
    https://docs.docker.com/get-docker/
### Make sure have it installed:
    docker --version
### Pull ubuntu 22.04 from docker:
    docker pull ubuntu:22.04
### You can then build and run your docker container with the following commands:
    sudo docker build -t chess-app .
    sudo docker run -p 5005:5005 chess-app
### Click the link that flask outputs to open the flask app.