# Echo server program
import socket
import rospy
import sys,re
import tf
import numpy as np

from trajectory_msgs.msg import MultiDOFJointTrajectory, MultiDOFJointTrajectoryPoint
from geometry_msgs.msg import Twist 
from geometry_msgs.msg import Transform
from geometry_msgs.msg import PointStamped

import math,time



HOST = socket.gethostname()               # Symbolic name meaning all available interfaces
PORT = 12346             # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr


def publish_waypoint(x,y,z,yaw):
	"""
	Publish a waypoint to 
	"""

	command_publisher = rospy.Publisher('/firefly/command/trajectory', MultiDOFJointTrajectory, queue_size = 10)

	# create trajectory msg
	traj = MultiDOFJointTrajectory()
	traj.header.stamp = rospy.Time.now()
	traj.header.frame_id = 'frame'
	traj.joint_names.append('base_link')


	# create start point for trajectory
	transforms = Transform()
	velocities = Twist()
	accel = Twist()
	point = MultiDOFJointTrajectoryPoint([transforms],[velocities],[accel],rospy.Time(1))
	traj.points.append(point)

	# create end point for trajectory
	# transforms = Transform()
	transforms.translation.x = x
	transforms.translation.y = y
	transforms.translation.z = z 

	quat = tf.transformations.quaternion_from_euler(0, 0, yaw*np.pi/180.0, axes = 'rzyx')

	transforms.rotation.x = quat[0]
	# transforms.rotation.x = 0
	transforms.rotation.y = quat[3]
	transforms.rotation.z = quat[2]
	transforms.rotation.w = quat[1]

	# print("quat[0]:",transforms.rotation.x)
	# print("quat[1]:",transforms.rotation.y)
	# print("quat[2]:",transforms.rotation.z)
	# print("quat[3]:",transforms.rotation.w)

	velocities = Twist()
	accel = Twist()
	point = MultiDOFJointTrajectoryPoint([transforms],[velocities],[accel],rospy.Time(2))
	traj.points.append(point)

	rospy.sleep(1)
	command_publisher.publish(traj)

def callback(point):
    # rospy.loginfo('I heard %f',point.point.x)
    # rospy.loginfo(" >> Published waypoint: x: {}, y: {}".format(point.point.x,point.point.y))
    # x_des=point.point.x+2
    # y_des=point.point.y+2
	x_des=point.point.x + float(subdata[0])*math.sin(270-float(subdata[1]))
	y_des=point.point.y + float(subdata[0])*math.cos(270-float(subdata[1]))
    # print x_des
	z_des=float(2)
	yaw_des=float(180+float(subdata[1]))
	publish_waypoint(point.point.x,point.point.y,z_des,yaw_des)
	publish_waypoint(x_des,y_des,z_des,yaw_des)
	# rospy.loginfo(" >> Published to UAV: x: {}, y: {}, z: {}, yaw: {}".format(x_des,y_des,z_des,yaw_des))


if __name__ == '__main__':
    rospy.init_node("riseq_rotors_waypoint_publisher", anonymous = True)
    # rospy.Subscriber('/firefly/ground_truth/position',PointStamped,callback)
    while 1:
		
		data = conn.recv(1024)
		# print "Received:", data
		if data:
			p1=re.compile(r'\[(.*?)\]',re.S)
			sdata=re.findall(p1,data)[-1].split(',')
			subdata = [float(sdata[0]), float(sdata[1])]
			# # # subdata=re.findall(p1,data)
			print "Addressed:", subdata
			# if sdata:
			# 	usefuldata = sdata[0].split(',')
			# 	# print usefuldata[0], usefuldata[1]
			# 	subdata = [float(usefuldata[0][1:]), float(usefuldata[1][:-1])]
				# print subdata
			rospy.Subscriber('/firefly/ground_truth/position',PointStamped,callback)
			time.sleep(2)
    conn.close()
    rospy.spin()