#! /usr/bin/env python

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from Send_Center import send_center


import sys
import tf
from trajectory_msgs.msg import MultiDOFJointTrajectory, MultiDOFJointTrajectoryPoint
from geometry_msgs.msg import Twist 
from geometry_msgs.msg import Transform
import socket

s=socket.socket() 
host=socket.gethostname()
port=12345
    # global clientsocket
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect((host,port))



# sys.path.append("/home/smalllogo/tracking_ws/src/uav_follow_robot/scripts/1209/PyIT2FLS-master/PyIT2FLS-master/examples")
# from new_v2 import IT2FL_v2_fun


# Show Image
def Show_Image(AnImage):
    cv2.imshow("View", AnImage)
    cv2.waitKey(3) 

# Image Process
def Calcuate_Center(CV_Image):

    # rospy.Subscriber('/firefly/command/trajectory', MultiDOFJointTrajectory, queue_size = 10)

    hsv = cv2.cvtColor(CV_Image, cv2.COLOR_BGR2HSV)
    lower= np.array([ 0, 0, 0])
    upper = np.array([180, 255, 46])
    mask = cv2.inRange(hsv, lower, upper)
    # Show_Image(mask)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] 
    if len(cnts) > 0: 
        c = max(cnts, key = cv2.contourArea) 
        ((x, y), radius) = cv2.minEnclosingCircle(c) 
        center=(int(x),int(y))
        cv2.circle(CV_Image, (int(x),int(y)), int(radius), (0,0,255), 2)
        Show_Image(CV_Image)
        # print CV_Image.shape
        print center
        #  Send Center
        send_center(int(center[0]), int(center[1]))





# Access Image
def callback(data):
    try:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')
        Calcuate_Center(cv_image)

        

    except CvBridgeError as e:
        print(e)

    
    

def main():

    print "666666666666"

    rospy.init_node('uav_image', anonymous=True)
    # rospy.init_node("riseq_rotors_waypoint_publisher", anonymous = True)
    # rospy.Subscriber('/firefly/vi_sensor/left/image_raw', Image, callback)
    image_sub = rospy.Subscriber('/firefly/vi_sensor/left/image_raw', Image, callback)
    # position_sub = rospy.Subscriber('/firefly/ground_truth/position',PointStamped,callback2)
    # image_sub = rospy.Subscriber('/firefly/vi_sensor/camera_depth/camera/image_raw', Image, callback)
    # image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, callback)
if __name__ == '__main__':
    main()
    rospy.spin()