# Cyber-Physical Systems Project: Vision-Based Cooperative Driving with Centralized Coordination

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Simulations / Demos](#simulations--demos)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Data Logging & Evaluation](#data-logging--evaluation)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project presents a cost effective centralized cooperative driving using ArUco marker-based vision tracking. It includes:

- Real time vehicle position and speed estimation using overhead camera
- Central base station decision-making logic
- Cooperative behavior like change track and proximity alerts
- Communication with vehicles over TCP sockets

The goal is to test the feasibility of centralized coordination using low cost vision systems in academic testbeds.


## System Architecture

The system consists of:

- **Vehicles**: Each vehicle includes a Raspberry Pi 5, a BLDC motor for propulsion, and a servo motor for steering .
- **Central Base Station**: A laptop running Python + OpenCV, which uses an overhead camera to detect ArUco markers and coordinate vehicle actions.
- **Communication**: TCP socket communication between each vehicle and the base station.
- **Tracking**: ArUco-based 2D localization .



![System Diagram](img/full%20system%20architecture.png "System architecture")

![System Diagram](img/full%20Autonomous%20car.png "Autonomous car")



## Installation 

Clone and Setup:

```bash

git clone https://github.com/yourusername/Cooperative-Autonomous-Driving.git
cd Cooperative-Autonomous-Driving
pip install -r requirements.txt
```

Run Base Station
```bash
python code/central_basestation.py

```

Run Vehicle Client

Configure SERVER_IP in vehicle.py and then run:

```bash
python code/vehicle_client.py

```
Each vehicle will connect and act based on received commands. 

A motor calibration code is also  included to calibrate the brushless dc motor with ESC.


## Simulations / Demos

This project operates on physical hardware as shown on system architecture; however, testbed evaluations using ArUco have been conducted.

Demo Scenarios:

    Two vehicle proximity alert test

    Speed based track change

    vehicle current status moving/ stopped



![System Diagram](img/full%20Autonomous%20car.png " Autonomous car")


[![Autonomous cooperative driving](https://markdown-videos-api.jorgenkh.no/url?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DttnMoTqzJSg)](https://www.youtube.com/watch?v=ttnMoTqzJSg)

## Configuration

Modify constants in the Python scripts:

    PROXIMITY_THRESHOLD: Distance (pixels) to trigger alert

    SPEED_THRESHOLD: Minimum speed (pixels/s) to classify vehicle as moving

    STATUS_UPDATE_INTERVAL: time (seconds) to update speed estimate frequency.

    
## Dependencies

List core software and versions used.

Python 3.11

OpenCV 4.9

NumPy

gpiozero 

adafruit-circuitpython-servokit

A webcam camera module

## Data Logging & Evaluation

This system logs and displays live tracking and control information for ArUco-marked RC vehicles, using computer vision and socket communication.
Data Logged to Console:
 - Client connections — when vehicles connect to the central base station via Wi-Fi.
 - Motion status updates — when a vehicle changes from moving to stopped, or vice versa.
 - Command dispatches — when a vehicle receives a control instruction.
 - Proximity alerts cleared — when vehicles are no longer in close range.

 On-Screen Visualization:
    Real-time video feed with:

        - ArUco marker detection.
        - Marker IDs.
        - Movement status (moving/stopped).
        - Proximity lines and distance between vehicles.

## Contributing

We welcome contributions that improve the coordination and cooperative decision logic.
To Contribute:

    Fork this repo

    Make changes in a branch

    Submit a Pull Request

## License

This project is open-source. Feel free to use it for academic and research purposes.
