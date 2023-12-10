# Robotic-project
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/18f3dc17-559d-4c00-8651-ed4b7578514d)

Authors:
  - Yanyin Yao 
  - Kunyang Liang

Supervisors:
 - Joaquin Jorge Rodriguez
 - Raphael Duverne

## Project Goal
The project is based on [TurtleBot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/autonomous_driving/#autonomous-driving)
and [Niryo Ned2](https://docs.niryo.com/product/ned2/v1.0.0/en/index.html)

In this project, we try to create the coordination with TurtleBot3 and Niryo Ned2.

Main Project Divided in Two Parts:

• Part I: Autonomous Driving

• Part II: Robots collaboration task
## Project Workflow 

## Requirements
- ros-noetic-image-transport 
- ros-noetic-cv-bridge 
- ros-noetic-vision-opencv 
- python3-opencv 
- libopencv-dev 
- ros-noetic-image-proc
- pyniryo

## Part I: Autonomous Driving
As required by ROBOTIS AutoRace Challenge,in this part we try to perform the autonomous driving of a ground differential robot by perception only.

![image](https://github.com/kebiabc/Robotic-project/assets/33951067/c8069536-25b1-46ee-996f-95242f253fca)

### Connection
```bash
ssh ubuntu@192.168.0.200
```

### TurtleBot3 Configuration #TB3
```bash
roslaunch turtlebot3_bringup turtlebot3_robot.launch #TB3
```
Open the camera on turtlebot3
```bash
roslaunch turtlebot3_autorace_camera raspberry_pi_camera_publish.launch
```
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/41972b96-896d-4a96-9204-43b201913350)

Launch the turtlebot3
```bash
roslaunch turtlebot3_bringup turtlebot3_robot.launch 
```     

### Intrinsic Camera Calibration
```bash
roslaunch turtlebot3_autorace_camera intrinsic_camera_calibration.launch mode:=calibration
```
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/1a9b8f6a-6f4c-41b1-aa4b-206dbd55ce45)

### Extrinsic Camera Calibration
```bash
roslaunch turtlebot3_autorace_camera extrinsic_camera_calibration.launch mode:=calibration
```
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/1493df54-6545-4f46-a2ee-a32ee1f39642)

### Lane Detection
```bash
roslaunch turtlebot3_autorace_detect detect_lane.launch mode:=calibration
```
```bash
rosrun rqt_reconfigure rqt_reconfigure
```
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/dc08bc5b-656d-4604-8b7a-4e714fbc6dd8)



## Part II: Robots collaboration task
The object is to go from start point to delivering point to pick a piece, and then come back to the starting point.

![image](https://github.com/kebiabc/Robotic-project/assets/33951067/97822208-a4b5-4bcc-bac3-7b730c67433b)

### Aruco tag detection

Using the camera on the TB3 we created an aruco tag detector which will detect the tag and publish on `/aruco_distance` topic the distance between the robot and the aruco tag.

```bash
rosrun turtlebot3_autorace_driving stoparuco.py
```

### Connect to Niryo Ned 2 
We connect to Niryo Ned 2 through SSH on the specific IP. By reading the documentation, there are many ways to establish a connection, because we also need to connect turtlebot, so in this case, we choose ethernet to connect.
Open a new terminal 

```bash
ssh niryo@192.168.0.150
```

### Operating interface
Niryo Studio is a graphical HMI. It allows a fast and direct control of Ned with an external computer.
Its purpose is to provide users with a complete and simple interface for Ned motion, programming environments and current status of Ned.
We set tasks and parameters through the graphical interface, and finally export it to a python file
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/8dea1538-c6e4-4c11-b7a0-437cc49d4192)


### Autonomous Robotic Coordination
Before 
```bash
roslaunch turtlebot3_autorace_driving turtlebot3_autorace_control_lane.launch
```
Launch the code for Niryo Ned 2
```bash

rosrun turtlebot3_autorace_driving connectned2.py

```
