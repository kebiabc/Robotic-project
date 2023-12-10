#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import Image, CompressedImage
import cv2
from cv2 import aruco

class Stoparuco:
    def __init__(self):
        rospy.init_node('stoparuco', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/camera/image/compressed', CompressedImage, self.image_callback)
        self.aruco_pub = rospy.Publisher('/aruco_markers', Image, queue_size=10)
        self.aruco_distance_pub = rospy.Publisher('/aruco_distance', Float64, queue_size=10)

        self.camera_matrix = np.array([[157.85325, 0, 160.94724],
                                       [0, 157.63912, 107.25425],
                                       [0, 0, 1]])

        self.dist_coeffs = np.array([-0.311590, 0.082363, -0.000079, -0.001038, 0.000000])
        

    def image_callback(self, msg):
        # Process image data if needed
        try:
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, 'bgr8')
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
            parameters = aruco.DetectorParameters_create()
        
            corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
            if ids is not None:
                for i in range(len(ids)):
                    # print(f"Detected ArUco marker {ids[i]}")
                    # Estimate the pose of the marker
                    rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners[i], 0.1, self.camera_matrix, self.dist_coeffs)

                    aruco.drawDetectedMarkers(cv_image, corners, ids)
                    # Calculate the distance from the camera to the marker
                    distance = np.linalg.norm(tvecs[0]) if tvecs is not None else None
                    rospy.loginfo(f"Distance to marker: {distance} meters")        
                    self.aruco_distance_pub.publish(Float64(distance))
                
                # Convert the image back to ROS format and publish it
                aruco_image_msg = self.bridge.cv2_to_imgmsg(cv_image, 'bgr8')
                self.aruco_pub.publish(aruco_image_msg)

        except Exception as e:
            rospy.logerr(f"Error processing image: {str(e)}")
        


if __name__ == '__main__':
    try:
        stoparuco = Stoparuco()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass

