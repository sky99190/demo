#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from pedsim_msgs.msg import LineObstacles
from gazebo_msgs.msg import ModelStates
import time
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import pyvisgraph as vg
import numpy as np
import copy

def dist_p(p1,p2):
    #print(p1,p2)
    return(abs(p1[0]-p2[0]+p1[1]-p2[1]))

def p_in_wall(p,wd):
    global wall_x,wall_y
    
    if wd=='x':
        r=wall_x.get(p[1])
        #print(p,r)
        if r!=None:
            for i in range(int(len(r)/2)):
                if p[0]>=r[i*2] and p[0]<=r[i*2+1]:
                    return(1)
        return(0)
    else:
        r=wall_y.get(p[0])    
        if r!=None:
            for i in range(int(len(r)/2)):
                if p[1]>=r[i*2] and p[1]<=r[i*2+1]:
                    return(1)
        return(0)
        
    
def padding_select(w0,w1):
    if w0==0 and w1==0:
        padding=0
    elif w0!=0 and w1==0:
        padding=1
    elif w0==0 and w1!=0:
        padding=2
    elif w0!=0 and w1!=0:
        padding=3
    else:
        padding=-1
    return padding

def cal_weight0(path_p):
    #print(path_p)
    w0=cal_weight1(path_p[0],path_p[1])
    w1=cal_weight1(path_p[1],path_p[2])
    #print(w0,w1)
    
    return(w0+w1,padding_select(w0,w1))
    
def cal_weight1(p1,p2):
    #print(p1,p2)
    dt=dist_p(p1,p2)
    if dt<=0.1:
        return(0)
    else:
        ps=np.linspace(p1,p2,num=dt/0.1+1)
        if ps[0][0]==ps[1][0]:
            wd='y'
        else:
            wd='x'
        ps=ps[1:-1]
        w=sum(map(lambda x: p_in_wall(x,wd), ps))
        return(w)
        #print(ps)

#print(cal_weight1([0,0],[0,0.2]))
    
def select_path(path):
    #print(path[0])
    #print(path[1])
    pw0,padding0=cal_weight0(path[0])
    pw1,padding1=cal_weight0(path[1])
    print(pw0,pw1)
    if pw0>pw1:
        return(path[0],padding0)
    else:
        return(path[1],padding1)
    
    
def f_direction(x,y):
    if x==0.0 and y>0.0:
        return(1)
    elif x==0.0 and y<0:
        return (3)
    elif y==0.0 and x>0:
        return(0)
    elif y==0.0 and x<0:
        return(2)
    
    
def p_d_3p(ps):
    y0=ps[1][1]-ps[0][1] 
    x0=ps[1][0]-ps[0][0] 
    y1=ps[2][1]-ps[1][1] 
    x1=ps[2][0]-ps[1][0] 
    return([f_direction(x0,y0),f_direction(x1,y1)])
    #print(y0,x0,y1,x1)

def p_d_2p(ps):
    y0=ps[1][1]-ps[0][1] 
    x0=ps[1][0]-ps[0][0] 
    return([f_direction(x0,y0)])
    
    
def padding_gen(padding,path_direct):
    padding_dd=dict()
    padding_dd[1,2]=[2,3]
    padding_dd[1,0]=[0,3]
    padding_dd[3,2]=[2,1]
    padding_dd[3,0]=[0,1]
    padding_dd[2,1]=[1,0]
    padding_dd[2,3]=[3,0]
    padding_dd[0,1]=[1,2]
    padding_dd[0,3]=[3,2]
    
    padding_lengh=dict()
    padding_lengh[3]=-0.1
    padding_lengh[1]=0.65
    padding_lengh[2]=-0.3
    padding_lengh[0]=0.3
    print(padding,path_direct)
    pd_data=[]
    for i in range(len(padding)):
        if padding[i]==0:
            pd_data.append(0)
            pd_data.append(0)
        elif padding[i]==1:
            pd_direction=padding_dd.get((path_direct[i][0],path_direct[i][1]))
            pd_data.append(padding_lengh[pd_direction[0]])
            pd_data.append(0)
        elif padding[i]==2:
            pd_direction=padding_dd.get((path_direct[i][0],path_direct[i][1]))
            pd_data.append(0)
            pd_data.append(padding_lengh[pd_direction[1]])
        elif padding[i]==3:
            pd_direction=padding_dd.get((path_direct[i][0],path_direct[i][1]))
            pd_data.append(padding_lengh[pd_direction[0]])
            pd_data.append(padding_lengh[pd_direction[1]])
        elif padding[i]==4:
            pd_data.append(0)
        elif padding[i]==5:
            pd_direction=padding_dd.get((path_direct[i-1][1],path_direct[i]))
            pd_data.append(padding_lengh[pd_direction[1]])
    print(pd_data)
    return(pd_data)
       
class action:
    act=''
    target_angle=0
    mid_angle=0
    target_d=0
    direction=0
    
def cal_mid_angle(direction,p0,p1):
    ag=47
    if direction==3 or direction==0:
        if p0>0 and p1<0:
            return(direction*90-ag)
        elif p0<0 and p1>0:
            return(direction*90+ag)
        else:
            raise ValueError('Error trans: (%d ,[%f ,%f])'%(direction,p0,p1))
    elif direction==1 or direction==2:
        if p0>0 and p1<0:
            return(direction*90+ag)
        elif p0<0 and p1>0:
            return(direction*90-ag)
        else:
            raise ValueError('Error trans: (%d ,[%f ,%f])'%(direction,p0,p1))
    else:
        raise ValueError('Error trans: ([%d] ,%f ,%f)'%(direction,p0,p1))
    
def add_trans(navi,pd_set,cali_set):
    if len(navi)<=1:
        print('no transaction needed')
        return(None)
    
    print(navi,pd_set)
    act_set=[]
    caliSet=set()
    for i in cali_set:
        caliSet.add(i)
    for i in range(len(navi)-1):
        trans=[navi[i][0],navi[i+1][0]]
        #print(trans)
        act=action()
        if trans==[1,3] or trans==[3,1] or trans==[2,0] or trans==[0,2]:
            #print(0)
            act.act='uturn'
            act.target_angle=trans[0]*90+(trans[1]-trans[0])*90
            act_set.append(act)
        elif abs(trans[0]-trans[1])==1:
            #print(1)
            act.act='turn'
            act.target_angle=trans[0]*90+(trans[1]-trans[0])*90
            act_set.append(act)
            if navi[i][0]==0:
                navi[i][1]-=1.5
            elif navi[i][0]==2:
                navi[i][1]+=1.5
            elif navi[i][0]==1:
                navi[i][2]-=0
            elif navi[i][0]==3:
                navi[i][2]+=1.5
        elif trans[0]==trans[1] and i+1 not in caliSet:
            #print(2)
            act.act='sturn'
            act.target_angle=trans[0]*90
            act.mid_angle=cal_mid_angle(trans[0],pd_set[i],pd_set[i+1])
            act_set.append(act)
            
        else:
            print(i)
            raise ValueError('Error trans: (%d ,%d)'%(trans[0],trans[1]))
    return(act_set,navi)
    
    
def gen_navi(pp,padding):
    
    
    if len(pp[0])<3:
        raise ValueError('Invalid start position')
    #d0=p_d_3p(pp[0])
    #d1=p_d_3p(pp[1])
    #print(d0)
    #print(d1)
    path_direct=[]
    path_direct_set=[]
    for i in range(len(pp)):
        if len(pp[i])==3:
            path_direct.append(p_d_3p(pp[i]))
        elif len(pp[i])==2:
            path_direct.append(p_d_2p(pp[i]))
        else:
            pass
        if i==0:
            path_direct_set=path_direct[0]
        else:
            path_direct_set=path_direct_set+path_direct[i]
    #print(path_direct_set)
        
    padding_set=padding_gen(padding,path_direct)
    pd_set=copy.deepcopy(padding_set)
    navi=[]
    cali_set=[]
    for i in range(len(pp)):
        for j in range(len(pp[i])-1):
            if dist_p(pp[i][j],pp[i][j+1])<=0.5:
                del pd_set[i*2+j]
                cali_set.append(len(navi))
            else:
                di=path_direct_set[i*2+j]
                if di==0 or di==2:
                    tx=pp[i][j+1][0]
                    ty=pp[i][j][1]+padding_set[i*2+j]
                elif di==1 or di==3:
                    tx=pp[i][j][0]+padding_set[i*2+j]
                    ty=pp[i][j+1][1]
                navi.append([di,tx,ty])
    print("cali_set: ")
    print(cali_set)
    trans=[]
    trans,navi=add_trans(navi,pd_set,cali_set)
    if len(navi)-len(trans)==1 or (len(navi==1) and trans==[]):
        print('adding trans')
    else:
        print(navi)
        print(trans)
        raise ValueError('Fail to add trans')
        
        
    for i in trans:
        print(i.act)
        print(i.target_angle)
        print(i.mid_angle)
        
    navigation_path=combine(navi,trans,cali_set)
    
    return(navigation_path)
    #print(navi)
    
def combine(navi, trans, cali_set):
    if len(navi)<=1:
        return(navi)
    final=[]
    cali_data=[]
    
    for i in cali_set:
        act=action()
        act.act='cali'
        act.direction=navi[i][0]
        if act.direction==0 or act.direction==2:
            act.target_d=navi[i][2]
        elif act.direction==1 or act.direction==3:
            act.target_d=navi[i][1]
        cali_data.append(act)
    cc=0
    tc=0        
    caliSet=set()
    for i in cali_set:
        caliSet.add(i)
    print(trans)
    for i in range(len(navi)):
        if cc<len(cali_set):
            if i==cali_set[cc]:
                final.append(cali_data[cc])
                cc+=1
                
                
        final.append(navi[i])
        
        if tc<len(trans) and (i+1 not in caliSet):
            final.append(trans[tc])
            tc+=1
            if i<len(navi)-2:
                act=action()
                act.act='cali'
                act.direction=navi[i+1][0]
                if act.direction==0 or act.direction==2:
                    act.target_d=navi[i+1][2]
                elif act.direction==1 or act.direction==3:
                    act.target_d=navi[i+1][1]
                final.append(act)
                
    print('-------------------')
    for i in final:
        if type(i)==list:
            print(i[0])
        else:
            print(i.act,i.direction,i.target_d)
            

    return(final)    
    
    
def callback(data):
    global obst
    global sub_wall
    rospy.loginfo(rospy.get_caller_id() + " Reading wall data")
    obst=copy.deepcopy(data.obstacles)
   
    sub_wall.unregister()
    #rospy.signal_shutdown('haha')
    
def maper():
    rospy.init_node('utility', anonymous=True)
    global obst
    global sub_wall
    #time.sleep(2)
    sub_wall=rospy.Subscriber("pedsim_simulator/simulated_walls", LineObstacles, callback)
    time.sleep(1)
    #rospy.spin()
    
    
    walls=[]    
    polys=[]
    points=set()
    global wall_x,wall_y
    wall_x=dict()
    wall_y=dict()
    for i in range(len(obst)-1):
        sx=obst[i].start.x
        sy=(obst[i].start.y)
        ex=obst[i].end.x
        ey=(obst[i].end.y)
        if (sx,sy) not in points:
            points.add((sx,sy))
            polys.append(vg.Point(sx,sy))
        if (ex,ey) not in points:
            points.add((ex,ey))
            polys.append(vg.Point(ex,ey))
        #polys.append(vg.Point(data.obstacles[i].start.x,data.obstacles[i].start.y))
        #polys.append(vg.Point(data.obstacles[i].end.x,data.obstacles[i].end.y))
        walls.append([[sx,sy],[ex,ey]])
        if sx==ex and sy!=ey:
            if sx in wall_y.keys():
                wall_y[sx].append([min(sy,ey),max(sy,ey)])
            else:
                wall_y[sx]=[min(sy,ey),max(sy,ey)]
        elif sy==ey and sx!=ex:
            if sy in wall_x.keys():
                wall_x[sy].append([min(sx,ex),max(sx,ex)])
            else:
                wall_x[sy]=[min(sx,ex),max(sx,ex)]
    wall_x[-2.5].append(0)
    wall_x[-2.5].append(5.5)
    walls.append([[0,-2.5],[5.5,-2.5]])
    #print(wall_x)
    #print(wall_y)
    #wall_v[-2.5]=[0,5.5]
    #print(polys)
    polys=polys[1:]
    polys.append(vg.Point(0,0))
    polys.append(vg.Point(0,-2.5))
    polys.append(vg.Point(5.5,-2.5))
    polys.append(vg.Point(0,-2.5))
    polys.append(vg.Point(0,-8.5))
    #polys.append(vg.Point(8.5,0))
    #print(polys)
    polys=[polys]
    #polys.append([vg.Point(0.1,2.5),vg.Point(5.5,2.5)])
    
    g = vg.VisGraph()
    
    g.build(polys)
    shortest = g.shortest_path(vg.Point(2,-8), vg.Point(15, -1))
    print(shortest)
    p=[]
    pr=[]
    pd=[]
    for i in range(len(shortest)):
        p.append([shortest[i].x,shortest[i].y]) 
        
    
    for i in range(len(p)-1):       
        if p[i][0]!=p[i+1][0] and p[i][1]!=p[i+1][1]:
            tp,padding=select_path([[p[i],[p[i][0],p[i+1][1]],p[i+1]],[p[i],[p[i+1][0],p[i][1]],p[i+1]]])  
        else: 
            tp=[[p[i][0],p[i][1]],[p[i][1],p[i+1][1]]] 
            if cal_weight1(tp[0],tp[1])!=0:
                padding=5
            else:
                padding=4
        pd.append(padding)    
        pr.append(tp)
        
    #print(navi)
    return(gen_navi(pr,pd))
    
    
    
    
    
if __name__ == '__main__':
    maper()
