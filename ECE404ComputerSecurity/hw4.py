#! /usr/bin/python
# Guanghua Zha ECE404 HW 4
import sys
from BitVector import *
import copy
import numpy as np
import time
import re

#parameter and table 
sbox_e=[99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]

sbox_d=[82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]

mm=[[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
mm=np.array(mm)
mm_r=[[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
mm_r=np.array(mm_r)

AES_modulus = BitVector(bitstring='100011011')


#start
start=time.time()
fp=open("plaintext.txt","r")
data=fp.read()
fp.close()

if len(data)%16!=0:
    data += '0' * (16-len(data)%16 )
    
try:
    fp1=open("key.txt","r")    
    key=fp1.read()
    fp1.close()
except:
    key='yayboilermakers!'
    
keysize=128
if len(key)%16!=0:
    key += '0' * (16-len(key)%16 )

sbox=np.array(sbox_e)
sbox=sbox.reshape(16,16)

sbox_r=np.array(sbox_d)
sbox_r=sbox_r.reshape(16,16)

key_c=[]


#key_generate
for i in range(16):
    temp=ord(key[i])
    key_c.append(temp)
key_c=np.array(key_c)
key_d=key_c.reshape(4,4)
key_d=key_d.transpose() 

key_zero=copy.deepcopy(key_d)
r_key=[1,0,0,0]

def key_gen(key_c,r_key):
    temp3=[key_c[:,3][1],key_c[:,3][2],key_c[:,3][3],key_c[:,3][0]]
    temp3=[sbox[temp3[0]//16][temp3[0]%16],sbox[temp3[1]//16][temp3[1]%16],sbox[temp3[2]//16][temp3[2]%16],sbox[temp3[3]//16][temp3[3]%16]]    
    key_first=[]
    temp=key_c[:,0]^temp3^r_key
    key_first.append(temp)
    temp=key_c[:,1]^key_first[0]
    key_first.append(temp)
    temp=key_c[:,2]^key_first[1]
    key_first.append(temp)
    temp=key_c[:,3]^key_first[2]
    key_first.append(temp)
    key_first_1=np.array(key_first)
    key_first_2=key_first_1.transpose()     
    return(key_first_2)

key_index=[]
for i in range(10):
    key_e=copy.deepcopy(key_gen(key_d,r_key))
    key_index.append(key_e)
    key_d=key_e
    r_key[0]=r_key[0]<<1
    if r_key[0]==256:
        r_key[0]=27


#sub bytes function
def replace(some_int,sel=0):
    if sel==0:
        return sbox[some_int//16][some_int%16]
    elif sel==1:
        return sbox_r[some_int//16][some_int%16]
    else:
        print("error_replace")

        
#shift_row 
def shift_row(some_matrix,sel=0):
    
    if sel==0:
        result=[]
        result.append(some_matrix[0])
        result.append(np.roll(some_matrix[1],-1))
        result.append(np.roll(some_matrix[2],2))
        result.append(np.roll(some_matrix[3],1))
        return np.array(result)
    elif sel==1:
        result=[]
        result.append(some_matrix[0])
        result.append(np.roll(some_matrix[1],1))
        result.append(np.roll(some_matrix[2],2))
        result.append(np.roll(some_matrix[3],-1))
        return np.array(result)
    else:
        print("error_shift_row")
        

#mix colume
def mixc(matrix,sel=0):
    result=[]
    if sel==0:
        for j in range(4):
            for i in range(4):
                a=list(map(mod_multi,mm[j],matrix[:,i]))
                b=a[0]^a[1]^a[2]^a[3]
                result.append(b)
        return result
    elif sel==1:
        for j in range(4):
            for i in range(4):
                a=list(map(mod_multi,mm_r[j],matrix[:,i]))
                b=a[0]^a[1]^a[2]^a[3]
                result.append(b)
        return result
    else:
        print("error_mixc")
        
    
#modulus multiplycation
def mod_multi(int2,int1):
    if int1==1:
        return int2
    counter=BitVector(intVal=int1,size=8)
    current=int2
    result=0
    i=7
    while int(counter)!=0:
        if counter[i]==1:
            result=result^current
            current=current<<1
            counter[i]=0
        else:
            current=current<<1
            
        if current>=256:
                current=(current%256)^27
        i-=1
    return result

#trans function for matrix
def transp(matrix):
    temp=list(map(np.transpose,matrix))
    temp=np.array(temp)
    return temp    


#start  encrypted  
data2=np.array(list(map(ord,data)))
data2_1=data2.reshape(-1,4,4)  
data2_1=transp(data2_1)
data2_2=data2_1^(key_zero) 

#first nine rounds
for i in range(9):
    data2_2=np.array(data2_2)
    data2_3=data2_2.reshape(1,-1)
    data2_4=data2_3[0]

    
    data3=list(map(replace,data2_4))
    data3=np.array(data3)
    data3_1=data3.reshape(-1,4,4)
    
    data4=list(map(shift_row,data3_1))
    data4_1=np.array(data4)

    c=list(map(mixc,data4_1))
    c_1=np.array(c)
    c_2=c_1.reshape(-1,4,4)
    c_3=c_2^(key_index[i]) 

    
    data2_2=copy.deepcopy(c_3)

#last round
data2_2=np.array(data2_2)
data2_3=data2_2.reshape(1,-1)
data2_4=data2_3[0]

data3=list(map(replace,data2_4))
data3_1=np.array(data3)
data3_2=data3_1.reshape(-1,4,4)

data4=list(map(shift_row,data3_2))

c=np.array(data4)
c_1=c.reshape(-1,4,4)
c_2=c_1^(key_index[9])

c_3=transp(c_2)
c_3=np.array(c_3)
c_3=c_3.reshape(1,-1)
c_3=c_3[0]
#print(c_3)
fp2=open('encrypted.txt','w')
for ele in c_3:
    if ele==0:
        fp2.write('00')
    elif ele<16:
        fp2.write('0'+format(ele,'x'))
    else:
        fp2.write(format(ele,'x'))

fp2.close()

end=time.time()

print('AES encrypted total time={:.6f}'.format(end-start),'s')

#start decrypted
fp3=open('encrypted.txt','r')
data=fp3.read()
fp3.close()
data2=re.findall("..",data)
lenz=len(data2)
if (len(data2))%16!=0:
    print('some error when open file for decrypt')

data3=list(map(int,data2,[16]*len(data2)))
data3=np.array(data3)
#print(data3)
data4=data3.reshape(-1,4,4)
data5=transp(data4)
data6=data5^key_index[9]

#first nine rounds
for i in range(9):
    data7=list(map(shift_row,data6,[1]*len(data6)))
    data7=np.array(data7)
    data8=data7.reshape(1,-1)
    data8_1=data8[0]
    data9=list(map(replace,data8_1,[1]*len(data8_1)))
    data9=np.array(data9)
    data9=data9.reshape(-1,4,4)
    data10=data9^key_index[8-i]
    data11=list(map(mixc,data10,[1]*len(data10)))
    data11=np.array(data11)
    data6=data11.reshape(-1,4,4)
 
#last round
data7=list(map(shift_row,data6,[1]*len(data6)))
data7=np.array(data7)
data8=data7.reshape(1,-1)
data8_1=data8[0]
data9=list(map(replace,data8_1,[1]*len(data8_1)))
data9=np.array(data9)
data9=data9.reshape(-1,4,4)
data10=data9^key_zero
data10=transp(data10)
data10=data10.reshape(1,-1)
data11=data10[0]

result=str()
for ele in data11:
    result+=chr(ele)
#print(result)
fp5=open('decrypted.txt','w')
fp5.write(result)
fp5.close()
end2=time.time()
print('AES decrypted total time={:.6f}'.format(end2-end),'s')