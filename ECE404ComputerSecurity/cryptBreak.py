#!/usr/bin/env python
"""
Created on Wed Jan 18 01:16:19 2017

@author: Guanghua Zha
ECE404 HW1 problem 2
"""

from BitVector import *
import string
import re

'''
only work with the file given for the homework that contain the keyword someplace

decrypt text will show in terminal or in the output_decrypt.txt
key only show in terminal. the format of the key is in decimal which are actually the ascii serial number


simplely just run the program, do not require DecryptForFun.py to run
input file name is encrypted.txt

'''
#def test():
a=BitVector(bitlist=[0]*16)
#b=BitVector(bitlist=[1]*8)
#c=BitVector(bitlist=[0]*16)
#print(int(c[0:8]))
local_max=2**16
#a^=BitVector(textstring="1")
fp=open("encrypted.txt","r")



b=BitVector(hexstring=fp.read())

fp2=open("output_decrypt.txt","w")


### construct of a word book that contains all the possible 
### letters and symbols in the original text

book2= string.ascii_letters            
book2+=' '
book2+=','
book2+='.'
book2+='\''
counter=0


i=0
overload=0
result=[]
imax=0

###copy from DecryptForFun.py to generate by_iv


PassPhrase = "Hopes and dreams of a million years" #(C)       
BLOCKSIZE = 16
numbytes = BLOCKSIZE // 8 #(E)
# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE) #(F)
for i in range(0,len(PassPhrase) // numbytes): #(G)
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes] #(H)
    bv_iv ^= BitVector( textstring = textstr )


### decrypt process, run until find the original text
while counter<local_max and overload==0:             
    temp=b[0:16]
    
    temp^=bv_iv
    temp^=a
    
    
    
### decrypt first two bytes(16 bits) and translate to character    
    by1=(int(temp[0:4]))                 
    by2=(int(temp[4:8]))
    by3=int(temp[8:12])
    by4=int(temp[12:16])
    
    str1=by1*16+by2
    str2=by3*16+by4
    
### if the first two characters are not in the word book, go to next key

    if chr(str1) in book2 and chr(str2) in book2:        
        #print(str3)
        draw=chr(str1)+chr(str2)
        last=b[0:16]
        j=0
        i=1

### decrypt  the entire sentence

        while i<(len(b)//16) and j==0:                      
            temp2=b[i*16:i*16+16]
            temp2^=last
            last=b[i*16:i*16+16]
            temp2=temp2^a

            by1=(int(temp2[0:4]))
            by2=(int(temp2[4:8]))
            by3=int(temp2[8:12])
            by4=int(temp2[12:16])
            
            str1=by1*16+by2
            str2=by3*16+by4

### if any of the character is not in the word book, 
### stop decrypt of the sentence
                
            if chr(str1) in book2 and chr(str2) in book2:    
                draw=draw+chr(str1)+chr(str2)
            else:
                j=1

            if i>imax:
                imax=i
                
### if entire sentence is decrypted and someplace in this sentence, 
### stop the program                 
            if i==(len(b)//16-1):                          
                if re.match(".*someplace.*",draw):
                    fp2.write(draw)
                    result.append(draw)
                    print("key(ascii in decimal)= "+str(int(a[0:8]))+","+str(int(a[8:16])))
                    overload=1
                
                    
                
            
            i=i+1
   
    counter=counter+1

### next key    
    try:
        a=BitVector(intVal=int(a)+1,size=16)           
        
    except:
        pass
    
    
### print result
    
if result!=[]:                                  
    print("The decrypt text is:")
    print(result[0])
else:
    print("key not found")
    
fp.close()
fp2.close()


