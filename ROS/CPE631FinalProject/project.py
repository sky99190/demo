#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from pedsim_msgs.msg import LineObstacles
from gazebo_msgs.msg import ModelStates
import time
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import utility
import copy
def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.obstacles)
    #print(type(data.obstacles))
    #print(len(data.obstacles))
    #print(data.obstacles[0])
    #print(type(data.obstacles[0]))
    x=0.0
    x=data.obstacles[2].start.x
    #print(x)
    y=0.0
    y=data.obstacles[2].start.y
    #print(y)
    z=0.0
    z=data.obstacles[2].start.z
    #print(z)
    
    sub_wall.unregister()

global p_v
def callback2(data):
    global p_v
    global p_t
    global yaw
    global px
    global py
    #print(data.name.index('my_robot'))
    #print(data.pose[7])
    #print("%.2f"%(data.twist[7].angular.z))
    #print("%.2f"%(data.twist[7].linear.x))
    #print(data.pose[7].orientation.x)
    px=data.pose[7].position.x
    py=data.pose[7].position.y
    orientation_q = data.pose[7].orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    #print(yaw/3.1415926*180)
    #if(time.time()-p_t>1.0):
#	p_t=time.time()
#	print(data.twist[7].linear.x-p_v)
#       p_v=data.twist[7].linear.x
    #print(data.my_robot.pose.position)
    #print(data.my_robot.twist.linear)


def set_ang_speed(yaw,target_angle,vel_msg):
    #print(yaw)
    

    diff=target_angle-yaw_to_angle(yaw)
    if diff<-180:
	diff=360+diff
    elif diff>180:
	diff=diff-360
    #print(diff)
    if diff>25 or diff<-25.0:
	ang_speed=0.6
    elif diff<10 or diff>-10.0:
	ang_speed=0.2
    else:
	ang_speed=0.3
    if diff<0 :
	vel_msg.angular.z=-ang_speed
    else:
	vel_msg.angular.z=ang_speed
    return(vel_msg)


def set_ang_speed_cali(yaw,target_angle,vel_msg):
    #print(yaw)
    

    diff=target_angle-yaw_to_angle(yaw)
    
    
    if diff<-180:
	diff=360+diff
    elif diff>180:
	diff=diff-360
    print(diff)
    if diff>25 or diff<-25.0:
	ang_speed=0.4
    elif diff<10 or diff>-10.0:
	ang_speed=0.1
    elif diff<4 or diff>-4:
	ang_speed=0.05
    else:
	ang_speed=0.25
    if diff<0 :
	vel_msg.angular.z=-ang_speed
    else:
	vel_msg.angular.z=ang_speed
    return(vel_msg)
  
  
def yaw_to_angle(yaw):
    if yaw<0:
	current_angle=360+yaw/3.1415926*180
    else:
	current_angle=yaw/3.1415926*180
    return(current_angle)


def cali(target,pub,rate,direction):
    vel_msg=Twist()
    global py
    global px
    global yaw
    
        
        
    
    if direction==0 :
        if target>py:
            ang=0.3
        elif target<py:
            ang=-0.3
        else:
            print('No need to calibrate')
            return(None)
            
    elif direction==1:
        if target>px:
            ang=-0.3
        elif target<px:
            ang=0.3
        else:
            print('No need to calibrate')
            return(None)
    elif direction==2:
        if target>py:
            ang=-0.3
        elif target<py:
            ang=0.3
        else:
            print('No need to calibrate')
            return(None)
    elif direction==3:
        if target>py:
            ang=-0.3
        elif target<py:
            ang=0.3
        else:
            print('No need to calibrate')
            return(None)
        
    if direction==0 or direction==2:
        print(target-py)
        dis=abs(target-py)
        while abs(target-py)>dis*0.95:
            vel_msg.angular.z=ang
            vel_msg.linear.x=0.2
            pub.publish(vel_msg)
            rate.sleep()
        
        
        while abs(target-py)>dis*0.35:
            vel_msg.angular.z=0
            vel_msg.linear.x=0.15
            pub.publish(vel_msg)
            rate.sleep()
            
            
        
    elif direction==1 or direction==3:
        dis=abs(target-px)
        print(target-px)
        while abs(target-px)>dis*0.95:
            vel_msg.angular.z=ang
            vel_msg.linear.x=0.2
            pub.publish(vel_msg)
            rate.sleep()
        
        
        while abs(target-px)>dis*0.35:
            vel_msg.angular.z=0
            vel_msg.linear.x=0.15
            pub.publish(vel_msg)
            rate.sleep()
        
    target_ang=direction_to_angle(direction)
    while abs(yaw_to_angle(yaw)-target_ang)>0.05:
        vel_msg=set_ang_speed_cali(yaw,target_ang,vel_msg)
        vel_msg.linear.x=0.1
        pub.publish(vel_msg)
        rate.sleep()
        #print(abs(0-yaw_to_angle(yaw)))
    print(px,py)
    #print(abs(0-yaw_to_angle(yaw)))
    vel_msg.linear.x=0
    vel_msg.angular.z=0.0
    pub.publish(vel_msg)
def direction_to_angle(direction):
    a=[0,90,180,270]
    return(a[direction])
def forward(target,pub,rate,direction):
    global px
    global py
    vel_msg=Twist()
    if direction==0 :
        while (target-px)>2:
            vel_msg.linear.x=0.6
            pub.publish(vel_msg)
            rate.sleep()
            
        while (target-px)>0.06:
            vel_msg.linear.x=0.3
            pub.publish(vel_msg)
            rate.sleep()
            
    elif direction==2:
        while (px-target)>2:
            vel_msg.linear.x=0.6
            pub.publish(vel_msg)
            rate.sleep()
        while (px-target)>0.06:
            vel_msg.linear.x=0.3
            pub.publish(vel_msg)
            rate.sleep()
    elif direction==1:
        while (target-py)>2:
            vel_msg.linear.x=0.6
            pub.publish(vel_msg)
            rate.sleep()
        while (target-py)>0.06:
            vel_msg.linear.x=0.3
            pub.publish(vel_msg)
            rate.sleep()
    elif direction==3:
        while (py-target)>2:
            vel_msg.linear.x=0.6
            pub.publish(vel_msg)
            rate.sleep()
        while (py-target)>0.06:
            vel_msg.linear.x=0.3
            pub.publish(vel_msg)
            rate.sleep()
    
    
    
    vel_msg.linear.x=0
    vel_msg.angular.z=0.0
    pub.publish(vel_msg)

def set_ang_speed2(yaw,target_angle,vel_msg):
    diff=target_angle-yaw_to_angle(yaw)
    if diff<-180:
	diff=360+diff
    elif diff>180:
	diff=diff-360
    #print(diff)
    if diff>25 or diff<-25.0:
	ang_speed=0.7
    elif diff<5 or diff>-5:
	ang_speed=0.3
    else:
	ang_speed=0.45
    if diff<0 :
	vel_msg.angular.z=-ang_speed
    else:
	vel_msg.angular.z=ang_speed
    return(vel_msg)
    
def sturn(target_angle,mid_angle,pub,rate,direction):
    global px
    global py
    global yaw
    vel_msg=Twist()
    
    #if abs(target_angle-yaw_to_angle(yaw))>5:
    #    print('Not in position for Sturn')
    #    print(target_angle,yaw_to_angle(yaw))
    #    print(abs(target_angle-yaw_to_angle(yaw)))
    #    return(None)
    #mid_angle=45
    
    
    while abs(mid_angle-yaw_to_angle(yaw))>0.2:
        print(abs(mid_angle-yaw_to_angle(yaw)))
        vel_msg=set_ang_speed2(yaw,mid_angle,vel_msg)
        vel_msg.linear.x=0.25
        pub.publish(vel_msg)
        rate.sleep()
    
    print(yaw_to_angle(yaw))
    
    #target_angle2=0
    while abs(target_angle-yaw_to_angle(yaw))>0.1:
        vel_msg=set_ang_speed2(yaw,target_angle,vel_msg)
        vel_msg.linear.x=0.20
        pub.publish(vel_msg)
        rate.sleep()
    #vel_msg.linear.x=0
    #vel_msg.angular.z=0.0
    #pub.publish(vel_msg)
    print(yaw_to_angle(yaw))

def turn(target_angle,pub,rate,direction):
    #global px
    #global py
    global yaw
    vel_msg=Twist()
    
    while abs(target_angle-yaw_to_angle(yaw))>0.06:
        vel_msg=set_ang_speed(yaw,target_angle,vel_msg)
        vel_msg.linear.x=0.1
        pub.publish(vel_msg)
        rate.sleep()
    vel_msg.linear.x=0
    vel_msg.angular.z=0.0
    pub.publish(vel_msg)
    print(yaw_to_angle(yaw))

def turn2(target_angle,pub,rate,direction):
    #global px
    #global py
    global yaw
    vel_msg=Twist()
    #print(target_angle)
    while abs(target_angle-yaw_to_angle(yaw))>0.06:
        vel_msg=set_ang_speed(yaw,target_angle,vel_msg)
        #print(vel_msg.angular.z)
        vel_msg.linear.x=0.0
        pub.publish(vel_msg)
        rate.sleep()
    vel_msg.linear.x=0
    vel_msg.angular.z=0.0
    pub.publish(vel_msg)
    print(yaw_to_angle(yaw))
    
def listener():
    global p_v
    global p_t
    global yaw
    global px
    global py
    
    navi=utility.maper()
    
    
    
    vel_msg = Twist()
    p_v=0.0
    p_t=time.time()
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    #rospy.init_node('listener', anonymous=True)
    pub = rospy.Publisher('Pioneer3AT/cmd_vel', Twist, queue_size=10)
    global sub_wall
    sub_wall=rospy.Subscriber("pedsim_simulator/simulated_walls", LineObstacles, callback)
    
    sub_state=rospy.Subscriber("gazebo/model_states", ModelStates, callback2)
    
    
    
    
    
    rate = rospy.Rate(50) 
    i=0
    time.sleep(2)
    '''while not rospy.is_shutdown():
        if i<200:
	    #print(i)
	    vel_msg.linear.x=0
	    vel_msg.angular.z=-8
	    i+=1
	elif i>=200 and i<400:
	    vel_msg.linear.x=-0.1
	    vel_msg.angular.z=-0
	    i+=1
        else:
	    vel_msg.linear.x=0
	    vel_msg.angular.z=0'''
    vel_msg.angular.z=0
    vel_msg.linear.x=0
    pub.publish(vel_msg)
    print(navi)
    for act in navi:
        if type(act)==list:
            print('foward')
            if act[0]==0 or act[0]==2:
                forward(act[1],pub,rate,act[0])
            elif act[0]==1 or act[0]==3:
                forward(act[2],pub,rate,act[0])
            
        else:
            if act.act=='cali':
                print('calibration')
                cali(act.target_d,pub,rate,act.direction)
            elif act.act=='turn':
                print('turing')
                turn(act.target_angle,pub,rate,act.direction)
            elif act.act=='sturn':
                print('sturn')
                sturn(act.target_angle,act.mid_angle,pub,rate,act.direction)
            
            
    print('done')
    '''
    
    #cali(py+0.35,pub,rate,0)
    #forward(5.5,pub,rate,0)
    #time.sleep(2)
    print(px,py)
    turn2(0,pub,rate,0)
    sturn(0,45,pub,rate,0)
    cali(-1.9,pub,rate,0)
    forward(14,pub,rate,0)
    turn(90,pub,rate,0)
    
    
    x0=px
    y0=py
    
    
    targety=-2.65
    
    dis=abs(targety-py)
    ang=0.3
    #target_angle2=0
    print(dis)
    targetx=5.5
    while abs(px-targetx)>0.06:
        vel_msg.linear.x=0.5
        pub.publish(vel_msg)
        rate.sleep()
        print(px)
    vel_msg.linear.x=0
    vel_msg.angular.z=0.0
    pub.publish(vel_msg)
    time.sleep(5)
    print(px-x0)
    
    x1=px
    y1=py
    print(y1-y0,x1-x0)
    vel_msg.linear.x=0
    vel_msg.angular.z=0.0
    pub.publish(vel_msg)
    
    if target_angle<0:
	target_angle=360+target_angle%360
    if target_angle>=360:
	target_angle=target_angle%360
    

    
    x1=px
    y1=py
    print(y1-y0,x1-x0)
    '''
    vel_msg.linear.x=0
    vel_msg.angular.z=0.0
    pub.publish(vel_msg)
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

if __name__ == '__main__':
    listener()
