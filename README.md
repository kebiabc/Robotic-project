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
## Flow-chart of Project 

![image](https://github.com/kebiabc/Robotic-project/assets/33951067/4c2c992b-5199-48aa-ae3a-857cf4e277ab)

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
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/cee3acd5-9fa1-417a-bef7-ec3c40d4b36d)

Launch the turtlebot3
```bash
roslaunch turtlebot3_bringup turtlebot3_robot.launch 
```     

### Intrinsic Camera Calibration
```bash
roslaunch turtlebot3_autorace_camera intrinsic_camera_calibration.launch mode:=calibration
```
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/1a9b8f6a-6f4c-41b1-aa4b-206dbd55ce45)

The adjusted parameters should be placed in turtlebot3_autorace_camera/calibration/intrinsic_calibration/camerav2_320x240_30fps.yaml.

### Extrinsic Camera Calibration
```bash
roslaunch turtlebot3_autorace_camera extrinsic_camera_calibration.launch mode:=calibration
```
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/1493df54-6545-4f46-a2ee-a32ee1f39642)

The adjusted parameters should be placed in turtlebot3_autorace_camera/calibration/extrinsic_calibration/projection.yaml.

### Lane Detection
```bash
roslaunch turtlebot3_autorace_detect detect_lane.launch mode:=calibration
```

Click Detect Lane then adjust parameters to do line color filtering.
```bash
rosrun rqt_reconfigure rqt_reconfigure
```
![image](https://github.com/kebiabc/Robotic-project/assets/33951067/724c13f7-1fc9-4613-9b66-312a38a4881c)

The adjusted parameters should be placed in turtlebot3_autorace_detect/param/lane/lane.yaml.

### Filtered Image resulted from adjusting parameters at rqt_reconfigure

![image](https://github.com/kebiabc/Robotic-project/assets/33951067/dc08bc5b-656d-4604-8b7a-4e714fbc6dd8)



## Part II: Robots collaboration task
The object is to go from start point to delivering point to pick a piece, and then come back to the starting point.

![image](https://github.com/kebiabc/Robotic-project/assets/33951067/97822208-a4b5-4bcc-bac3-7b730c67433b)

### Aruco tag detection

Using the camera on the TB3 we created an aruco tag detector which will detect the tag and publish on `/aruco_distance` topic the distance between the robot and the aruco tag.

![image](https://github.com/kebiabc/Robotic-project/assets/33951067/f8ac90d7-81a7-494e-a1ab-2b0acba10d8f)


```bash
rosrun turtlebot3_autorace_driving stoparuco.py
```
First, preprocess the images obtained by the camera.
Then use the aruco.detectMarkers from opencv library to Identify Aruco tag and get the id.
```bash
cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, 'bgr8')
gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()       
corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
```
#### In order to obtain the specific distance, we must first estimate the pose of the camera
cameraMatrix and distCoeffs are the camera calibration parameters that were created during the camera calibration process.We have already obtained it in the previous steps.

The output parameters rvecs and tvecs are the rotation and translation vectors respectively, for each of the markers in markerCorners.
```bash
rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.1, self.camera_matrix, self.dist_coeffs)
aruco.drawDetectedMarkers(cv_image, corners, ids)
# Calculate the distance from the camera to the marker
distance = np.linalg.norm(tvecs[0]) if tvecs is not None else None
rospy.loginfo(f"Distance to marker: {distance} meters")
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
Before launching
```bash
roslaunch turtlebot3_autorace_driving turtlebot3_autorace_control_lane.launch
```
Launch the code for Niryo Ned 2
```bash

rosrun turtlebot3_autorace_driving connectned2.py

```
### Connections:
```bash
        +------------------+               +------------------+
        |   ControlLane    |               |   Connectned2    |
        |                  |               |                  |
        | /control/lane    |               | /niryo_con       |
        | /control/max_vel |               |                  |
        | /aruco_distance  |               +------------------+
        | /niryo_con       | ------\       |                  |
        | /control/cmd_vel |        \      |                  |
        +------------------+         \     +------------------+
                                       \
                                        \
                                         \
                                      +------------------+
                                      |   Stoparuco      |
                                      |                  |
                                      | /camera/image/   |
                                      | compressed       |
                                      | /aruco_distance  |
                                      | /aruco_markers   |
                                      +------------------+
```

The ControlLane class subscribes to /aruco_distance topic, which is  published by the Stoparuco class.

The Connectned2 class subscribes to and publishes messages on the /niryo_con topic, which used by the ControlLane class to coordinate the robot's behavior based on the Niryo controller status.

The Stoparuco class is responsible for processing camera images and detecting Aruco markers, providing distance information. This information is used by the ControlLane class to make decisions based on the detected Aruco markers.

## Demo
![GIF 2023-12-10 17-27-12](https://github.com/kebiabc/Robotic-project/assets/33951067/839a0c90-f378-4dc9-86ec-ca72292314fe)


![GIF 2023-12-10 17-19-55](https://github.com/kebiabc/Robotic-project/assets/33951067/e92541d5-2c1d-40b7-91ea-a095e2d93e6e)


