# Introduction

This code uses python yolo to detect (toy) trucks from a camera input (1) and creates a symphony activation on a k8s cluster. This workflow will then read vehicle properties and check driver status. If a driver was on the road for more than 10 hours, an email notification will be triggered with the help of an Azure logic app. Then, the symphony dock workflow will connect to a fuel pump (2) to check the fuel state and waits until target state of 100% fuel will be reached.

1. [Truck Detection](/truck_detection/README.md)
2. [Fuel Pump](/docker/fuel-pump/README.md)

## Setup 

*If WSL is used, make sure docker context is set to default. Rootless (convenience script installation) context does not work.*

1. Install prerequisites from https://github.com/Eclipse-SDV-Hackathon-Chapter-Two/challenge-maestro/blob/main/eclipse-symphony/README.md
2. Run startup.sh to start the necessary processes

Run showdown.sh to kill all started processes