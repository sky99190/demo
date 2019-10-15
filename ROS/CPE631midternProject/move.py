import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from visualization_msgs.msg import Marker
from math import radians, pi

rospy.init_node('nav_test', anonymous=False)
        
move_base0 = actionlib.SimpleActionClient("/tb3_0/move_base", MoveBaseAction)
move_base1 = actionlib.SimpleActionClient("/tb3_1/move_base", MoveBaseAction)
move_base2 = actionlib.SimpleActionClient("/tb3_2/move_base", MoveBaseAction)
rospy.sleep(2)

goal = MoveBaseGoal()
goal.target_pose.header.frame_id = '/map'
goal.target_pose.header.stamp = rospy.Time.now()
goal.target_pose.pose = Pose(Point(-1.815, -1.076, -0.00), Quaternion(*quaternion_from_euler(0, 0, pi/2, axes='sxyz')))

goal1 = MoveBaseGoal()
goal1.target_pose.header.frame_id = '/map'
goal1.target_pose.header.stamp = rospy.Time.now()
goal1.target_pose.pose = Pose(Point(-1.815, 0.4304, 0.00), Quaternion(*quaternion_from_euler(0, 0, pi*3/2, axes='sxyz')))

goal2 = MoveBaseGoal()
goal2.target_pose.header.frame_id = '/map'
goal2.target_pose.header.stamp = rospy.Time.now()
goal2.target_pose.pose = Pose(Point(-7, 3, 0.00), Quaternion(*quaternion_from_euler(0, 0, pi/2, axes='sxyz')))

goal3 = MoveBaseGoal()
goal3.target_pose.header.frame_id = '/map'
goal3.target_pose.header.stamp = rospy.Time.now()
goal3.target_pose.pose = Pose(Point(3.1, 3.0, -0.00), Quaternion(*quaternion_from_euler(0, 0, pi/2, axes='sxyz')))

goal_mid = MoveBaseGoal()
goal_mid.target_pose.header.frame_id = '/map'
goal_mid.target_pose.header.stamp = rospy.Time.now()
goal_mid.target_pose.pose = Pose(Point(-2.386, -0.516, -0.00), Quaternion(*quaternion_from_euler(0, 0, pi/2, axes='sxyz')))

goal4 = MoveBaseGoal()
goal4.target_pose.header.frame_id = '/map'
goal4.target_pose.header.stamp = rospy.Time.now()
goal4.target_pose.pose = Pose(Point(3.1, -5.680, -0.00), Quaternion(*quaternion_from_euler(0, 0, pi/2, axes='sxyz')))

move_base0.send_goal(goal1)
move_base1.send_goal(goal)
move_base2.send_goal(goal_mid)

while move_base0.get_state()!=3 and move_base1.get_state() != 3 and move_base2.get_state()!=3:
    print('r0: '+str(move_base0.get_state())+' r1: '+str(move_base1.get_state())+' r2: '+str(move_base2.get_state()))
    rospy.sleep(1)
rospy.sleep(3)
move_base2.send_goal(goal2)
move_base0.send_goal(goal3)
rospy.sleep(3)
move_base1.send_goal(goal4)
