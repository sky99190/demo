# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PIL import Image as im
import numpy as np
from scipy import interpolate as sp_inter 
import scipy.misc
from enum import Enum
import time

class Effect(Enum):
    rotate90=[0,1,2,3]
    rotate180=[3,2,1,0]
    rotate270=[1,3,0,2]
    flipHorizontally=[2,3,0,1]
    flipVertically=[1,0,3,2]
    transpose=[0,2,1,3]
            
            
class Homography:
    Effect=["rotate90","rotate180","rotate270","flipHorizontally","flipVertically","transpose"]
    def __init__(self, **kwargs):
        noi=len(kwargs.keys())
        self.forwardMatrix=[]
        self.inverseMatrix=[]
        if noi==1:
            self.ck_matrix(kwargs.get("homographyMatrix"))
            self.forwardMatrix=np.matrix(kwargs.get("homographyMatrix"))
            self.inverseMatrix=self.forwardMatrix**-1
        elif noi==3 or noi==2:
            self.calc_h(kwargs.get("sourcePoints"),kwargs.get("targetPoints"),kwargs.get("effect"))
            temp=self.computeHomography(kwargs.get("sourcePoints"),kwargs.get("targetPoints"),kwargs.get("effect"))
        else:
            pass
        
    def ck_matrix(self,h_matrix):
        if type(h_matrix)!=np.ndarray:
            raise ValueError("h_matrix is wrong type.")
        if h_matrix.size!=9 or h_matrix[0].size!=3:
            raise ValueError("woops")
        else:
            pass
        
        for x in h_matrix:
            for y in x:
                if type(y)==float or type(y)==np.float64:
                    pass
                else:
                    raise ValueError("\"{0}\" in {1} is not a float.".format(y,h_matrix))
        
    def calc_h(self,sp,tp,ef=None):
        if type(sp)!=np.ndarray or type(tp)!=np.ndarray:
            raise ValueError("tp sp is wrong type")
        if sp.size!=8 or sp[0].size!=2:
            raise ValueError("woops2")
        
        if ef!=None:
            #if type(ef)!=Effect:
            #   raise TypeError("effet is not type Enum")

            if ef.name not in self.Effect:
                raise TypeError("no such effect!")
                
        for x in sp:
            for y in x:
                if type(y)==float or type(y)==np.float64:
                    pass
                else:
                    raise TypeError("{0} not a float number!".format(y))
        for x in tp:
            for y in x:
                if type(y)==float or type(y)==np.float64:
                    pass
                else:
                    raise TypeError("{0} not a float number!".format(y))
                    
                    
    def computeHomography(self, sourcePoints, targetPoints, effect=None):
        tp0=targetPoints[0]
        tp1=targetPoints[1]
        tp2=targetPoints[2]
        tp3=targetPoints[3]
        od=[]

        if type(effect)==str:
            raise TypeError("effect is wrong type")
        if effect==None:
            od=[0,1,2,3]
        elif effect.name=="rotate90":
            od=[2,0,3,1]
        elif effect.name=="rotate180":
            od=[3,2,1,0]
        elif effect.name=="rotate270":
            od=[1,3,0,2]
        elif effect.name=="flipHorizontally":
            od=[2,3,0,1]
        elif effect.name=="flipVertically":
            od=[1,0,3,2]
        elif effect.name=="transpose":
            od=[0,2,1,3]
        else:
            raise ValueError("wtf!!")
        #print(effect)
        sp0=sourcePoints[od[0]]
        sp1=sourcePoints[od[1]]
        sp2=sourcePoints[od[2]]
        sp3=sourcePoints[od[3]]
        matrix_A=[]
        matrix_b=[]
        matrix_A=[[sp0[0],sp0[1],1.0,0.0,0.0,0.0,-tp0[0]*sp0[0],-tp0[0]*sp0[1]],\
                  [0.0,0.0,0.0,sp0[0],sp0[1],1.0,-tp0[1]*sp0[0],-tp0[1]*sp0[1]],\
                  [sp1[0],sp1[1],1.0,0.0,0.0,0.0,-tp1[0]*sp1[0],-tp1[0]*sp1[1]],\
                  [0.0,0.0,0.0,sp1[0],sp1[1],1.0,-tp1[1]*sp1[0],-tp1[1]*sp1[1]],\
                  [sp2[0],sp2[1],1.0,0.0,0.0,0.0,-tp2[0]*sp2[0],-tp2[0]*sp2[1]],\
                  [0.0,0.0,0.0,sp2[0],sp2[1],1.0,-tp2[1]*sp2[0],-tp2[1]*sp2[1]],\
                  [sp3[0],sp3[1],1.0,0.0,0.0,0.0,-tp3[0]*sp3[0],-tp3[0]*sp3[1]],\
                  [0.0,0.0,0.0,sp3[0],sp3[1],1.0,-tp3[1]*sp3[0],-tp3[1]*sp3[1]]]
        matrix_b=[tp0[0],tp0[1],tp1[0],tp1[1],tp2[0],tp2[1],tp3[0],tp3[1]]
        h=np.linalg.solve(matrix_A,matrix_b)
        #print(h)
        matrix_H=[]
        matrix_H=[[h[0],h[1],h[2]],[h[3],h[4],h[5]],[h[6],h[7],1]]
        #print(matrix_H)
        self.forwardMatrix=np.array(matrix_H)
        self.inverseMatrix=np.array(np.matrix(matrix_H)**-1)
        return self.forwardMatrix
        
class Transformation:
    def __init__(self, sourceImage, homography=None):
        self.time=time.time()
        if type(sourceImage)!=np.ndarray:
            raise TypeError("sourceImage not a ndarray")
        self.data=sourceImage
        self.index=0
        width=len(sourceImage[0])
        self.width=width
        height=len(sourceImage)
        self.height=int(height)
        
        
        self.sp=np.zeros((4,2))
        
        #self.sp=[[0.0,0.0],[width,0.0],[0.0,height],[width,height]]
        self.sp[1][0]=width-1
        self.sp[2][1]=height-1
        self.sp[3][0]=width-1
        self.sp[3][1]=height-1
        #print(self.sp)

        if homography is None:
            self.homo=None
        else:
            pass
            #if type(homography)!=Homography:
            #    raise TypeError("homography not type class.")
            #self.homo=homography
            
    
    def setupTransformation(self, targetPoints, effect=None):
        self.tp=targetPoints
        #print(effect)
        if self.homo==None:
            self.homo=Homography( sourcePoints=self.sp,targetPoints=self.tp,effect=effect)
        else:
            pass

        for i in range(0,4):
            pass
        xmin=targetPoints[0][0]
        xmax=targetPoints[0][0]
        ymin=targetPoints[0][1]
        ymax=targetPoints[0][1]

        for x in range(1,4):
            for i in range(0,2):
                if i==0:
                    xmin=min(targetPoints[x][i],xmin)
                    xmax=max(targetPoints[x][i],xmax)
                else:
                    ymin=min(targetPoints[x][i],ymin)
                    ymax=max(targetPoints[x][i],ymax)
        xmin=int(xmin)
        xmax=int(xmax)
        ymin=int(ymin)
        ymax=int(ymax)
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
        self.bd=[[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]]


    def trick(self,x0):
        sum(map(lambda y:self.tricks(x0,y),range(self.ymin,self.ymax+1)))
        return 1

    def tricks(self,x,y):
        mat=self.homo.inverseMatrix
        #temp2=np.matrix(self.homo.inverseMatrix)*np.matrix([[x],[y],[1]])
        c0=(mat[2][0]*x+mat[2][1]*y+mat[2][2])
        x0=np.round((mat[0][0]*x+mat[0][1]*y+mat[0][2])/c0,3)
        y0=np.round((mat[1][0]*x+mat[1][1]*y+mat[1][2])/c0,3)

        #y0=np.round((temp2[1][0]/temp2[2][0]),3)
        #x0=np.round((temp2[0][0]/temp2[2][0]),3)
        #print(x,y) y0>=0.0 and y0<=float(self.height-1) and x0>=0.0 and x0<=float(self.width-1)
        if 0.0<=y0<=float(self.height-1) and 0.0<=x0<=float(self.width-1):
            self.containerImage[y][x]=np.uint8(np.round(self.intapolator(y0,x0)))
        return 1


    def transformImageOnto(self, containerImage):
        self.containerImage=containerImage
        x_array=np.arange(0,int(self.height))
        y_array=np.arange(0,int(self.width))

        #print(type(self.data))
        #print(self.data.size,self.data[0].size)
        #print(x_array.size)
        #
        # print(y_array.size)
        self.intapolator=sp_inter.RectBivariateSpline(x_array,y_array,self.data,kx=1,ky=1)
        self.data2=containerImage
        self.tph=len(containerImage)
        self.tpw=len(containerImage[0])

        if hasattr(self,'tp'):
            pass
        else:
            raise TypeError("no tp")
        #self.time=self.time-time.time()
        #print(self.time)
        sum(map(lambda x:self.trick(x),range(self.xmin,self.xmax+1)))

        '''
        for y in range(self.ymin,self.ymax+1):
            for x in range(self.xmin,self.xmax+1):
                temp=np.matrix([[x],[y],[1]])
                temp2=np.matrix(self.homo.inverseMatrix)*temp
                #print(temp2[2][0])
                y0=np.round((temp2[1][0]/temp2[2][0]),3)
                x0=np.round((temp2[0][0]/temp2[2][0]),3)
                if y0>=0.0 and y0<=float(self.height-1) and x0>=0.0 and x0<=float(self.width-1):
                    containerImage[y][x]=np.uint8(np.round(self.intapolator(y0,x0)))
        '''
        #img=im.fromarray(self.containerImage)
        #img.save("out.jpg")
        #scipy.misc.toimage("out.jpg",containerImage)
        return self.containerImage



        
        
class ColorTransformation(Transformation):

    def __init__(self, sourceImage, homography=None):
        if type(sourceImage)!=np.ndarray:
            raise TypeError("color_T: sourceImage is not a ndarray")
        if sourceImage[0][0].size!=3:

            raise ValueError("Not a color image.")
        if homography!=None:
            if type(homography)!=Homography:
                raise TypeError("type of the given homography is wrong.")

        super(ColorTransformation,self).__init__(sourceImage,homography)

        self.r=sourceImage[:,:,0]
        self.g=sourceImage[:,:,1]
        self.b=sourceImage[:,:,2]

    def trick(self,x0):
        sum(map(lambda y:self.tricks(x0,y),range(self.ymin,self.ymax+1)))
        return 1

    def tricks(self,x,y):
        mat=self.homo.inverseMatrix

        c0=(mat[2][0]*x+mat[2][1]*y+mat[2][2])
        x0=np.round((mat[0][0]*x+mat[0][1]*y+mat[0][2])/c0,3)
        y0=np.round((mat[1][0]*x+mat[1][1]*y+mat[1][2])/c0,3)


        if 0.0<=y0<=float(self.height-1) and 0.0<=x0<=float(self.width-1):
            self.out_r[y][x]=np.uint8(np.round(self.intapolator_r(y0,x0)))
            self.out_g[y][x]=np.uint8(np.round(self.intapolator_g(y0,x0)))
            self.out_b[y][x]=np.uint8(np.round(self.intapolator_b(y0,x0)))
        return 1


    def transformImageOnto(self, containerImage):
        x_array=np.arange(0,int(self.height))
        y_array=np.arange(0,int(self.width))

        self.intapolator_r=sp_inter.RectBivariateSpline(x_array,y_array,self.r,kx=1,ky=1)
        self.intapolator_g=sp_inter.RectBivariateSpline(x_array,y_array,self.g,kx=1,ky=1)
        self.intapolator_b=sp_inter.RectBivariateSpline(x_array,y_array,self.b,kx=1,ky=1)

        self.out_r=containerImage[:,:,0]
        self.out_g=containerImage[:,:,1]
        self.out_b=containerImage[:,:,2]
        self.tph=len(containerImage)
        self.tpw=len(containerImage[0])

        if hasattr(self,'tp'):
            pass
        else:
            raise TypeError("no tp")

        sum(map(lambda x:self.trick(x),range(self.xmin,self.xmax+1)))


        return np.dstack((self.out_r,self.out_g,self.out_b))

        
        
        

class AdvancedTransformation:
    def __init__(self, sourceImage, v, h1, h2):

        if type(sourceImage)!=np.ndarray or type(v)!=int or type(h1)!=int or type(h2)!=int:
            raise TypeError("input is in wrong type")

        if sourceImage[0][0].size!=3:
            raise ValueError("not a color image")

        if  v<0 or h1<0 or h2<0:
            raise ValueError("input parameter smaller than zero")

        self.data=sourceImage

        self.v=int(v)
        self.h1=int(h1)
        self.h2=int(h2)

        width=len(sourceImage[0])
        self.width=width
        height=len(sourceImage)
        self.height=int(height)

        if sourceImage[0][0].size==3:
            self.mode=3
        elif sourceImage[0][0].size==1:
            self.mode=1
        else:
            raise ValueError("Image form unknown")
        #print(sourceImage.size,sourceImage[0].size)
        self.sp1=np.zeros((4,2))
        self.sp2=np.zeros((4,2))
        self.tp1=np.zeros((4,2))
        self.tp2=np.zeros((4,2))
        self.target=np.full((int(height+v),int(width),3),255,dtype=np.uint8)
        img=im.fromarray(self.target,"RGB")
        img.save("out00.png")
        #print(self.target[5][5])
        #print(v,h1,h2)

        if width%2==0:
            self.sp1[1][0]=width/2-1
            self.sp1[2][1]=height-1
            self.sp1[3][0]=width/2-1
            self.sp1[3][1]=height-1

            self.sp2[0][0]=0
            self.sp2[1][0]=width/2-1
            self.sp2[2][1]=height-1
            self.sp2[2][0]=0
            self.sp2[3][0]=width/2-1
            self.sp2[3][1]=height-1


        else:
            raise ValueError("colume is not a even number.")

        self.data1=np.hsplit(sourceImage,2)[0]
        self.data1=np.array(self.data1)
        self.data2=np.hsplit(sourceImage,2)[1]
        self.data2=np.array(self.data2)

        self.r_1=self.data1[:,:,0]
        self.g_1=self.data1[:,:,1]
        self.b_1=self.data1[:,:,2]
        self.r_2=self.data2[:,:,0]
        self.g_2=self.data2[:,:,1]
        self.b_2=self.data2[:,:,2]


        
    
    def applyEffectV(self):

        self.tp1[0][0]=self.sp1[0][0]
        self.tp1[0][1]=self.sp1[0][1]
        self.tp1[1][0]=self.sp1[1][0]-self.h2
        self.tp1[1][1]=self.sp1[1][1]+self.v
        self.tp1[2][0]=self.sp1[2][0]+self.h1
        self.tp1[2][1]=self.sp1[2][1]
        self.tp1[3][0]=self.sp1[3][0]
        self.tp1[3][1]=self.sp1[3][1]+self.v

        self.tp2[0][0]=self.sp2[0][0]+self.h2
        self.tp2[0][1]=self.sp2[0][1]+self.v
        self.tp2[1][0]=self.sp2[1][0]
        self.tp2[1][1]=self.sp2[1][1]
        self.tp2[2][0]=self.sp2[2][0]
        self.tp2[2][1]=self.sp2[2][1]+self.v
        self.tp2[3][0]=self.sp2[3][0]-self.h1
        self.tp2[3][1]=self.sp2[3][1]
        self.homo1=Homography( sourcePoints=self.sp1,targetPoints=self.tp1)
        self.homo2=Homography( sourcePoints=self.sp2,targetPoints=self.tp2)
        #print(self.width, self.height)
        #print(self.sp1)
        #print(self.tp1)
        #print(self.sp2)
        #print(self.tp2)
        a=self.color()
        img=im.fromarray(a,"RGB")
        img.save("out0.png")
        return self.target




    
    def applyEffectA(self):
        self.tp1[0][0]=self.sp1[0][0]+self.h1
        self.tp1[0][1]=self.sp1[0][1]+self.v
        self.tp1[1][0]=self.sp1[1][0]
        self.tp1[1][1]=self.sp1[1][1]
        self.tp1[2][0]=self.sp1[2][0]
        self.tp1[2][1]=self.sp1[2][1]+self.v
        self.tp1[3][0]=self.sp1[3][0]-self.h2
        self.tp1[3][1]=self.sp1[3][1]

        self.tp2[0][0]=self.sp2[0][0]
        self.tp2[0][1]=self.sp2[0][1]
        self.tp2[1][0]=self.sp2[1][0]-self.h1
        self.tp2[1][1]=self.sp2[1][1]+self.v
        self.tp2[2][0]=self.sp2[2][0]+self.h2
        self.tp2[2][1]=self.sp2[2][1]
        self.tp2[3][0]=self.sp2[3][0]
        self.tp2[3][1]=self.sp2[3][1]+self.v
        self.homo1=Homography( sourcePoints=self.sp1,targetPoints=self.tp1)
        self.homo2=Homography( sourcePoints=self.sp2,targetPoints=self.tp2)
        #print(self.width, self.height)
        #print(self.sp1)
        #print(self.tp1)
        #print(self.sp2)
        #print(self.tp2)

        a=self.color()
        img=im.fromarray(a,"RGB")
        img.save("out1.png")
        return self.target


    def color(self):

        x_array_1=np.arange(0,int(self.height))
        y_array_1=np.arange(0,int(self.width/2))
        x_array_2=np.arange(0,int(self.height))
        y_array_2=np.arange(0,int(self.width/2))


        self.intapolator_r_1=sp_inter.RectBivariateSpline(x_array_1,y_array_1,self.r_1,kx=1,ky=1)
        self.intapolator_g_1=sp_inter.RectBivariateSpline(x_array_1,y_array_1,self.g_1,kx=1,ky=1)
        self.intapolator_b_1=sp_inter.RectBivariateSpline(x_array_1,y_array_1,self.b_1,kx=1,ky=1)
        self.intapolator_r_2=sp_inter.RectBivariateSpline(x_array_2,y_array_2,self.r_2,kx=1,ky=1)
        self.intapolator_g_2=sp_inter.RectBivariateSpline(x_array_2,y_array_2,self.g_2,kx=1,ky=1)
        self.intapolator_b_2=sp_inter.RectBivariateSpline(x_array_2,y_array_2,self.b_2,kx=1,ky=1)



        for y in range(0,int(self.height+self.v)):
            for x in range(0,int(self.width/2)):

                mat=self.homo1.inverseMatrix
                c0=(mat[2][0]*x+mat[2][1]*y+mat[2][2])
                x0=np.round((mat[0][0]*x+mat[0][1]*y+mat[0][2])/c0,3)
                y0=np.round((mat[1][0]*x+mat[1][1]*y+mat[1][2])/c0,3)

                if 0.0<=y0<=float(self.height-1) and 0.0<=x0<=float(self.width/2-1):
                    r=np.uint8(np.round(self.intapolator_r_1(y0,x0)))
                    g=np.uint8(np.round(self.intapolator_g_1(y0,x0)))
                    b=np.uint8(np.round(self.intapolator_b_1(y0,x0)))
                    self.target[y][x]=([np.uint8(r[0][0]),np.uint8(g[0][0]),np.uint8(b[0][0])])




        img=im.fromarray(self.target,"RGB")
        img.save("half.png")
        for y in range(0,int(self.height+self.v)):
            for x in range(0,int(self.width/2)):

                mat=self.homo2.inverseMatrix
                c0=(mat[2][0]*x+mat[2][1]*y+mat[2][2])
                x0=np.round((mat[0][0]*x+mat[0][1]*y+mat[0][2])/c0,3)
                y0=np.round((mat[1][0]*x+mat[1][1]*y+mat[1][2])/c0,3)

                if 0.0<=y0<=float(self.height-1) and 0.0<=x0<=float(self.width/2-1):
                    r=np.uint8(np.round(self.intapolator_r_2(y0,x0)))
                    g=np.uint8(np.round(self.intapolator_g_2(y0,x0)))
                    b=np.uint8(np.round(self.intapolator_b_2(y0,x0)))
                    self.target[y][x+self.width/2]=([r[0],g[0],b[0]])


        return self.target


        

    
        



        
def main():
    im1=im.open('Ring.png')
    im2=im.open('White.png')
    data1=np.array(im1)
    data2=np.array(im2)

    #a=AdvancedTransformation(data1,0,00,00)
    #b=a.applyEffectV()
    #print(type(b))
    #img=im.fromarray(b,"RGB")
    #img.save("adv.png")
    #fptr=open("test.txt","w")
    #fptr2=open("test2.txt","w")


    
    
    
    
if __name__=="__main__":
    main()
