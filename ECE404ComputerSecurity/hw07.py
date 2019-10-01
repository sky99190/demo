#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 04:15:54 2017

@author: Zha
"""

import sys
from BitVector import *
import copy
import hashlib

#variable used
h0 = BitVector(hexstring='6a09e667f3bcc908')
h1 = BitVector(hexstring='bb67ae8584caa73b')
h2 = BitVector(hexstring='3c6ef372fe94f82b')
h3 = BitVector(hexstring='a54ff53a5f1d36f1')
h4 = BitVector(hexstring='510e527fade682d1')
h5 = BitVector(hexstring='9b05688c2b3e6c1f')
h6 = BitVector(hexstring='1f83d9abfb41bd6b')
h7 = BitVector(hexstring='5be0cd19137e2179')
Ks = [BitVector(hexstring='428a2f98d728ae22'), BitVector(hexstring='7137449123ef65cd'), BitVector(hexstring='b5c0fbcfec4d3b2f'), BitVector(hexstring='e9b5dba58189dbbc'), BitVector(hexstring='3956c25bf348b538'), BitVector(hexstring='59f111f1b605d019'), BitVector(hexstring='923f82a4af194f9b'), BitVector(hexstring='ab1c5ed5da6d8118'), BitVector(hexstring='d807aa98a3030242'), BitVector(hexstring='12835b0145706fbe'), BitVector(hexstring='243185be4ee4b28c'), BitVector(hexstring='550c7dc3d5ffb4e2'), BitVector(hexstring='72be5d74f27b896f'), BitVector(hexstring='80deb1fe3b1696b1'), BitVector(hexstring='9bdc06a725c71235'), BitVector(hexstring='c19bf174cf692694'), BitVector(hexstring='e49b69c19ef14ad2'), BitVector(hexstring='efbe4786384f25e3'), BitVector(hexstring='0fc19dc68b8cd5b5'), BitVector(hexstring='240ca1cc77ac9c65'), BitVector(hexstring='2de92c6f592b0275'), BitVector(hexstring='4a7484aa6ea6e483'), BitVector(hexstring='5cb0a9dcbd41fbd4'), BitVector(hexstring='76f988da831153b5'), BitVector(hexstring='983e5152ee66dfab'), BitVector(hexstring='a831c66d2db43210'), BitVector(hexstring='b00327c898fb213f'), BitVector(hexstring='bf597fc7beef0ee4'), BitVector(hexstring='c6e00bf33da88fc2'), BitVector(hexstring='d5a79147930aa725'), BitVector(hexstring='06ca6351e003826f'), BitVector(hexstring='142929670a0e6e70'), BitVector(hexstring='27b70a8546d22ffc'), BitVector(hexstring='2e1b21385c26c926'), BitVector(hexstring='4d2c6dfc5ac42aed'), BitVector(hexstring='53380d139d95b3df'), BitVector(hexstring='650a73548baf63de'), BitVector(hexstring='766a0abb3c77b2a8'), BitVector(hexstring='81c2c92e47edaee6'), BitVector(hexstring='92722c851482353b'), BitVector(hexstring='a2bfe8a14cf10364'), BitVector(hexstring='a81a664bbc423001'), BitVector(hexstring='c24b8b70d0f89791'), BitVector(hexstring='c76c51a30654be30'), BitVector(hexstring='d192e819d6ef5218'), BitVector(hexstring='d69906245565a910'), BitVector(hexstring='f40e35855771202a'), BitVector(hexstring='106aa07032bbd1b8'), BitVector(hexstring='19a4c116b8d2d0c8'), BitVector(hexstring='1e376c085141ab53'), BitVector(hexstring='2748774cdf8eeb99'), BitVector(hexstring='34b0bcb5e19b48a8'), BitVector(hexstring='391c0cb3c5c95a63'), BitVector(hexstring='4ed8aa4ae3418acb'), BitVector(hexstring='5b9cca4f7763e373'), BitVector(hexstring='682e6ff3d6b2b8a3'), BitVector(hexstring='748f82ee5defb2fc'), BitVector(hexstring='78a5636f43172f60'), BitVector(hexstring='84c87814a1f0ab72'), BitVector(hexstring='8cc702081a6439ec'), BitVector(hexstring='90befffa23631e28'), BitVector(hexstring='a4506cebde82bde9'), BitVector(hexstring='bef9a3f7b2c67915'), BitVector(hexstring='c67178f2e372532b'), BitVector(hexstring='ca273eceea26619c'), BitVector(hexstring='d186b8c721c0c207'), BitVector(hexstring='eada7dd6cde0eb1e'), BitVector(hexstring='f57d4f7fee6ed178'), BitVector(hexstring='06f067aa72176fba'), BitVector(hexstring='0a637dc5a2c898a6'), BitVector(hexstring='113f9804bef90dae'), BitVector(hexstring='1b710b35131c471b'), BitVector(hexstring='28db77f523047d84'), BitVector(hexstring='32caab7b40c72493'), BitVector(hexstring='3c9ebe0a15c9bebc'), BitVector(hexstring='431d67c49c100d4c'), BitVector(hexstring='4cc5d4becb3e42b6'), BitVector(hexstring='597f299cfc657e2a'), BitVector(hexstring='5fcb6fab3ad6faec'), BitVector(hexstring='6c44198c4a475817')]
s0=[h0,h1,h2,h3,h4,h5,h6,h7]
t64=2**64


#read in file
if len( sys.argv ) != 2:                                                 #(M1)
    sys.exit( "Call syntax:  hw07.py  message.txt" )

message=sys.argv[1]
#message='message.txt'

fp=open(message,'r',encoding='utf-8')
temp=fp.read()
fp.close()

#padding
dv=BitVector(textstring=temp)
data=dv+BitVector(bitstring='1')
data1=data+BitVector(intVal=0,size=(896-data.length())%1024)+BitVector(intVal=dv.length(),size=128)
ssr=data1.length()//1024
word=[None]*80
s=copy.deepcopy(s0)

#loop
for i in range(ssr):
    
    ss=copy.deepcopy(s)
    current=data1[i*1024:(i+1)*1024]
    
    word[0:16]=[current[x:x+64] for x in range(0,1024,64)]
    
    for j in range(16,80):
        a1=word[j-15]
        a2=word[j-2]
        
        b0=(copy.deepcopy(a1)>>1)^(copy.deepcopy(a1)>>8)^(copy.deepcopy(a1).shift_right(7))
        b1=(copy.deepcopy(a2)>>19)^(copy.deepcopy(a2)>>61)^(copy.deepcopy(a2).shift_right(6))
        word[j]=BitVector(intVal = (int(word[j-16]) + int(b0) + int(word[j-7]) + int(b1)) % t64,size = 64)
        
    
    for k in range(80):
        c0=(copy.deepcopy(s[0])>>28)^(copy.deepcopy(s[0])>>34)^(copy.deepcopy(s[0])>>39)
        c4=(copy.deepcopy(s[4])>>14)^(copy.deepcopy(s[4])>>18)^(copy.deepcopy(s[4])>>41)
        d1=(s[4]&s[5])^((~s[4])&s[6])
        d2=(s[0]&s[1])^(s[0]&s[2])^(s[1]&s[2])
        e1=BitVector(intVal=(int(s[7])+int(d1)+int(c4)+int(word[k])+int(Ks[k]))%t64, size=64)
        e2=BitVector(intVal=(int(c0)+int(d2))%t64, size=64)
        f1=BitVector(intVal=(int(e1)+int(e2))%t64,size=64)
        f2=BitVector(intVal=(int(e1)+int(s[3]))%t64,size=64)
        s=[f1,s[0],s[1],s[2],f2,s[4],s[5],s[6]]
    s[0]=BitVector(intVal=(int(ss[0])+int(s[0]))%t64,size=64)
    s[1]=BitVector(intVal=(int(ss[1])+int(s[1]))%t64,size=64)
    s[2]=BitVector(intVal=(int(ss[2])+int(s[2]))%t64,size=64)
    s[3]=BitVector(intVal=(int(ss[3])+int(s[3]))%t64,size=64)
    s[4]=BitVector(intVal=(int(ss[4])+int(s[4]))%t64,size=64)
    s[5]=BitVector(intVal=(int(ss[5])+int(s[5]))%t64,size=64)
    s[6]=BitVector(intVal=(int(ss[6])+int(s[6]))%t64,size=64)
    s[7]=BitVector(intVal=(int(ss[7])+int(s[7]))%t64,size=64)
    
out=s[0]+s[1]+s[2]+s[3]+s[4]+s[5]+s[6]+s[7]
out1=out.get_hex_string_from_bitvector()
fp3=open('output.txt','w')
fp3.write(out1)
fp3.close()

'''
print(out1)
fp4=open('message.txt','r')
cc=fp4.read()
fp4.close()
ccc=cc.encode('utf-8')
tt=hashlib.sha512()
tt.update(ccc)
print(tt.hexdigest())
'''