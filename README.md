# Symphony Maestro Challenge 2024

This code uses python yolo to detect (toy) trucks from a camera input (1) and creates a symphony activation on a k8s cluster. This workflow will then read vehicle properties and check driver status. If a driver was on the road for more than 10 hours, an email notification will be triggered with the help of an Azure logic app. Then, the symphony dock workflow will connect to a fuel pump (2) to check the fuel state and waits until target state of 100% fuel will be reached.

Follow the setup steps below to prepare for the execution of the project.

## Setup 

*If WSL is used, make sure docker context is set to default. Rootless (convenience script installation) context does not work.*

One feature had to be added on the symphony repo. In order to use the feature "patching symphony targets" it is required to build symphony. This feature allows to observe the fuel state in symphony opera. To get this feature, use option 1.  

### Build and Install Symphony (option 1)
*IMPORTANT: This does not work with any Ubuntu WSL > 20.04. So Ubuntu 20.04 on Win11 WSL2 was used to run this. Even with the help of Haishi, we did not manage to get this to work. He created a custom build for us*

To run custom build of Haishi:
```shell
cd ~/symphony/test/localenv
maestro up -s 0.48-exp.34

# if minikube can not load images, load them manually
docker pull quay.io/jetstack/cert-manager-controller:v1.13.1
docker pull quay.io/jetstack/cert-manager-cainjector:v1.13.1
docker pull quay.io/jetstack/cert-manager-webhook:v1.13.1
docker pull redis/redis-stack-server:7.2.0-v12
docker pull openzipkin/zipkin-slim:2.24.1

minikube image load quay.io/jetstack/cert-manager-controller:v1.13.1
minikube image load quay.io/jetstack/cert-manager-cainjector:v1.13.1
minikube image load quay.io/jetstack/cert-manager-webhook:v1.13.1
minikube image load redis/redis-stack-server:7.2.0-v12
minikube image load openzipkin/zipkin-slim:2.24.1

# all pods should be started now
kubectl get pods
```
Stop here if the commands above worked.


``` shell
# Install Docker
cd ~
sudo apt-get update -y
sudo sh -eux <<EOF
# Install newuidmap & newgidmap binaries
apt-get install -y uidmap
EOF
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
# This does not work!!
# dockerd-rootless-setuptool.sh install
sudo groupadd docker
sudo usermod -aG docker $USER
docker run hello-world

# Install Maestro
wget -q https://raw.githubusercontent.com/eclipse-symphony/symphony/master/cli/install/install.sh -O - | /bin/bash

# Install Go
wget https://go.dev/dl/go1.23.3.linux-amd64.tar.gz
# remove any previous go installation
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.23.3.linux-amd64.tar.gz
# add to PATH variable
# need to set GOPATH to a path I own -> https://groups.google.com/g/golang-nuts/c/U4Erx1_F-bo?pli=1
mkdir ~/my_go
export GOPATH=$HOME/my_go
export PATH=$PATH:/usr/local/go/bin
export PATH=$PATH:$GOPATH/bin
go version

# Install make
sudo apt-get update && sudo apt-get install -y build-essential

# Install Mage
cd ~
git clone https://github.com/magefile/mage
cd mage
go run bootstrap.go
mage 

# Install Kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo chmod +x kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
kubectl config view

# Install Helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
sudo chmod 700 get_helm.sh
sudo ./get_helm.sh

# Install minikube
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo chmod +x minikube
sudo mv minikube /usr/local/bin/
minikube start
kubectl config view

# Build Symphony
cd ~
git clone https://github.com/eclipse-symphony/symphony.git
cd ~/symphony
git checkout sdv-hackathon-portal
git pull
cd ~/symphony/test/localenv
mage build:all
mage test:up

# install k9s
sudo apt-get update -y
sudo snap install k9s
sudo ln -s /snap/k9s/current/bin/k9s /snap/bin/
k9s
```

## Install Symphony (option 2)

### Using Maestro

```shell
wget -q https://raw.githubusercontent.com/eclipse-symphony/symphony/master/cli/install/install.sh -O - | /bin/bash

maestro up 

```

## Post Installation

```shell
cd ~

git clone git@github.com:Eclipse-SDV-Hackathon-Chapter-Two/maestro.git
cd maestro

# deploy mqtt broker
kubectl apply -f eclipse-symphony/mosquitto/mosquitto.yaml
kubectl port-forward svc/mosquitto-service 1884:1883

# apply truck templates
kubectl apply -f eclipse-symphony/truck-templates/.

# Prepare Truck Docking Workflow
kubectl apply -f eclipse-symphony/workflows/docking.yaml

# deploy symphony portal opera
kubectl apply -f eclipse-symphony/portal/opera-deployment.yaml
kubectl port-forward svc/opera-service 3001:3000

# docking a mock-truck
kubectl apply -f - <<EOF
apiVersion: workflow.symphony/v1
kind: Activation
metadata:
  name: mock-truck-docking-activation
spec:
  campaign: "docking:v1"
  stage: ""
  inputs:    
    truck-template: mock-truck:v1
EOF
```

## Install and Run the Project

1. [Truck Detection](/truck_detection/README.md) to read camera input and trigger symphony campaign
2. [Fuel Pump](/docker/fuel-pump/README.md) to build and start docker container that simulates fuel pump
3. A convenience script that configures port forwarding has been added 
 ```shell
 cd ~/maestro
 ./startup.sh
 ```

To shut down all processes, run:
```shell
cd ~/maestro
./showdown.sh
```