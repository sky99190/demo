#!/usr/bin/env python
"""
Created on Wed Jan 18 11:30:53 2017

@author: Guanghua Zha
ECE 404 HW1, problem 1
"""
'''
simple run, no need to specify any file
input.txt key.txt output.txt
file must only contain upper and lower case letter
key should not be empty
'''
import string

#open file
fp=open("input.txt","r")
data=fp.readlines()
fp.close()
fp1=open("key.txt","r")
key=fp1.readlines()
fp1.close()
fp2=open("output.txt","w")

#read key
key1=''
for line in key:
    key1=key1+line.strip()

if len(key1)==0:
    raise ValueError("key.txt is empty")
    
#index for cipher
book=dict()
book2=dict()
book3=dict()
counter=0

for x in string.ascii_lowercase:
    book[x]=counter
    book[x.upper()]=counter
    book2[counter]=x.upper()
    book3[counter]=x
    counter+=1

#read plan text one by one and generate the encrypt text
#upper or lower case are depend on the key
counter=0
for line in data:
    for x in line:
        if key1[counter].isupper():
            temp=(book[x]+book[key1[counter]])%26
            fp2.write(book2[temp])
            
        elif key1[counter].islower():
            temp=(book[x]+book[key1[counter]])%26
            fp2.write(book3[temp])
        else:
            fp2.write(x)
        counter=(counter+1)%len(key1)

fp2.close()