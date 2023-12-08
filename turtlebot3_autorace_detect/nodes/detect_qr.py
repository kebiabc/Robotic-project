import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge
from std_msgs.msg import UInt8, Float64
from sensor_msgs.msg import Image, CompressedImage
from dynamic_reconfigure.server import Server
from turtlebot3_autorace_detect.cfg import DetectLaneParamsConfig
from pyzbar.pyzbar import decode

#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ArUcoDetector:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.image_callback)

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # Perform ArUco marker detection and distance calculation here

        # If marker detected and distance < 0.2m, stop TurtleBot3
        if marker_detected and distance < 0.2:
            # Stop TurtleBot3 (publish to cmd_vel topic)
            # Example: self.cmd_vel_pub.publish(Twist())

if __name__ == '__main__':
    rospy.init_node('aruco_detector')
    aruco_detector = ArUcoDetector()
    rospy.spin()
