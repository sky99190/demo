# -*- coding: utf-8 -*-
"""
Created on Sat May  4 06:51:37 2019

@author: gz
"""

import rospy

from gazebo_msgs.msg import ModelState
from gazebo_msgs.msg import ModelStates
import time
from geometry_msgs.msg import Twist
def callback2(data):
    orientation_q = data.pose[7].orientation
    #orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    #(roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    print(data.pose[7].orientation)


global sub_state
global d
d=ModelState()
d.model_name='my_robot'
rospy.init_node('set_state', anonymous=True)
pub_state = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
pub_cmd = rospy.Publisher('Pioneer3AT/cmd_vel', Twist, queue_size=10)
#sub_state=rospy.Subscriber("/gazebo/model_states", ModelStates, callback2)
time.sleep(2)
#5.69440778170271, -2.6624093207338806
vel_msg=Twist()
vel_msg.linear.x=0
vel_msg.angular.z=0
d.pose.position.x=5.69440778170271
d.pose.position.y=-2.6624093207338806
#d.pose.position.x=1
#d.pose.position.y=-3
d.pose.orientation.x=0
d.pose.orientation.y=0
d.pose.orientation.z=0
d.pose.orientation.w=1
d.twist.linear.x=0
d.twist.angular.z=0
pub_cmd.publish(vel_msg)
pub_state.publish(d)
time.sleep(0.5)
#name = raw_input("What's your name? ")
d.pose.position.x=2
d.pose.position.y=-8
d.pose.orientation.x=0
d.pose.orientation.y=0
d.pose.orientation.z=0
d.pose.orientation.w=1
d.twist.linear.x=0
d.twist.angular.z=0
pub_cmd.publish(vel_msg)
pub_state.publish(d)