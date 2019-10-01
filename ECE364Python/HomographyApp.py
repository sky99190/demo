import sys
import re
from PySide.QtCore import *
from PySide.QtGui import *
from HomographyGUI import *
from PIL import ImageQt as imq
from PIL import Image as im
from PIL import ImageEnhance as imh
import numpy as np
from Homography import *
from enum import Enum



class Effect(Enum):
    rotate90=[0,1,2,3]
    rotate180=[3,2,1,0]
    rotate270=[1,3,0,2]
    flipHorizontally=[2,3,0,1]
    flipVertically=[1,0,3,2]
    transpose=[0,2,1,3]


class Transform(QMainWindow, Ui_Dialog):
    Efkt=["rotate90","rotate180","rotate270","flipHorizontally","flipVertically","transpose"]
    def __init__(self, parent=None):

        super(Transform, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled((False))
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_7.setEnabled(True)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_4.setEnabled(False)
        self.lines=[self.lineEdit,self.lineEdit_2,self.lineEdit_3,self.lineEdit_4]
        self.lines_s=[self.lineEdit_6,self.lineEdit_7]
        self.comboBox.setEnabled(False)
        self.graphicsView.setEnabled(False)
        self.graphicsView_2.setEnabled(False)
        self.fgetp=0
        self.fgetp_s=0
        self.reset_en=0
        self.count=0
        self.count2=0
        self.ps=None
        self.pt=None
        self.store=self.graphicsView_2.mousePressEvent
        self.store2=self.graphicsView_2.keyPressEvent
        self.store_s=self.graphicsView.mousePressEvent
        self.store2_s=self.graphicsView.keyPressEvent
        self.tp=np.zeros((4,2))
        self.sp=np.zeros((2,2))
        self.c_b()


    def c_b(self):
        self.pushButton.clicked.connect(lambda: self.loadData(0))
        self.pushButton_2.clicked.connect(lambda: self.loadData(1))
        self.pushButton_3.clicked.connect(self.transfer)
        self.pushButton_4.clicked.connect(self.reset_image)
        self.pushButton_5.clicked.connect(self.save)
        self.pushButton_6.clicked.connect(self.s333)
        self.pushButton_7.clicked.connect(self.reset)
        self.pushButton_8.clicked.connect(self.s444)

    def reset_image(self):
        img=im.fromarray(self.backup)
        self.out=self.backup
        qimg=imq.ImageQt(img)
        pixmap=QPixmap.fromImage(qimg)
        scn=QGraphicsScene()
        self.graphicsView_2.setScene((scn))
        pixmap2=scn.addPixmap(pixmap)
        self.graphicsView_2.fitInView(pixmap2, Qt.KeepAspectRatio)
        self.graphicsView_2.show()

    def transfer(self):
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled((False))
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        a=self.comboBox.findText(self.comboBox.currentText())
        if a==0:
            ef=None
        else:
            ef=Effect[self.Efkt[a-1]]

        if self.source[0][0].size==self.target[0][0].size==1:
            b=Transformation(self.source)
            b.setupTransformation(self.tp,ef)
            c=b.transformImageOnto(self.target)

            img=im.fromarray(c)
            self.out=c
            qimg=imq.ImageQt(img)
            pixmap=QPixmap.fromImage(qimg)
            scn=QGraphicsScene()
            self.graphicsView_2.setScene((scn))

            pixmap2=scn.addPixmap(pixmap)
            self.graphicsView_2.fitInView(pixmap2, Qt.KeepAspectRatio)
            self.graphicsView_2.show()

        elif self.source[0][0].size==self.target[0][0].size==3:
            b=ColorTransformation(self.source)
            b.setupTransformation(self.tp,ef)
            c=b.transformImageOnto(self.target)
            img=im.fromarray(c)
            self.out=c
            qimg=imq.ImageQt(img)
            pixmap=QPixmap.fromImage(qimg)
            scn=QGraphicsScene()
            self.graphicsView_2.setScene((scn))

            pixmap2=scn.addPixmap(pixmap)
            self.graphicsView_2.fitInView(pixmap2, Qt.KeepAspectRatio)
            self.graphicsView_2.show()
        elif self.source[0][0].size==3 and self.target[0][0].size==1:
            temp=im.fromarray(self.target)
            temp2=im.Image.convert(temp,"RGB")
            temp3=np.array(temp2)
            self.target=temp3

            b=ColorTransformation(self.source)
            b.setupTransformation(self.tp,ef)
            c=b.transformImageOnto(self.target)
            img=im.fromarray(c)
            self.out=c
            qimg=imq.ImageQt(img)
            pixmap=QPixmap.fromImage(qimg)
            scn=QGraphicsScene()
            self.graphicsView_2.setScene((scn))

            pixmap2=scn.addPixmap(pixmap)
            self.graphicsView_2.fitInView(pixmap2, Qt.KeepAspectRatio)
            self.graphicsView_2.show()



        elif self.source[0][0].size==1 and self.target[0][0].size==3:
            temp=im.fromarray(self.source)
            temp2=im.Image.convert(temp,"RGB")
            temp3=np.array(temp2)
            self.source=temp3

            b=ColorTransformation(self.source)
            b.setupTransformation(self.tp,ef)
            c=b.transformImageOnto(self.target)
            img=im.fromarray(c)
            self.out=c
            qimg=imq.ImageQt(img)
            pixmap=QPixmap.fromImage(qimg)
            scn=QGraphicsScene()
            self.graphicsView_2.setScene((scn))

            pixmap2=scn.addPixmap(pixmap)
            self.graphicsView_2.fitInView(pixmap2, Qt.KeepAspectRatio)
            self.graphicsView_2.show()


        else:
            pass

        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.pushButton_7.setEnabled(True)
        self.pushButton_8.setEnabled(True)



    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, caption='save to file ...', filter="PNG files (*.png)")
        if not filePath:
            return
        img=im.fromarray(self.out)
        qimg=imq.ImageQt(img)
        pixmap=QPixmap.fromImage(qimg)
        pixmap.save(filePath+".png","png")



    def loadData(self,s):
        """
        Obtain a file name from a file dialog, and pass it on to the loading method. This is to facilitate automated
        testing. Invoke this method when clicking on the 'load' button.

        *** DO NOT MODIFY THIS METHOD! ***
        """
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open PNG file ...', filter="PNG files (*.png)")
        if not filePath:
            return

        if s==0:
            if filePath!=self.ps:
                self.count=0
                self.count2=0
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit_4.setText("")
                self.lineEdit_5.setText("")
                self.lineEdit_6.setText("")
                self.lineEdit_7.setText("")
                self.ps=filePath
                self.dataready()
                if self.pt!=None:
                    self.reset_image()


            img=im.open(filePath)
            self.s_w, self.s_h=img.size
            qimg=imq.ImageQt(img)
            self.source=np.array(img)
            img.close()
            pixmap=QPixmap.fromImage(qimg)
            scn=QGraphicsScene()
            self.graphicsView.setScene((scn))
            self.graphicsView.setEnabled(True)
            pixmap2=scn.addPixmap(pixmap)
            self.graphicsView.fitInView(pixmap2, Qt.KeepAspectRatio)
            self.graphicsView.show()



        if s==1:
            if filePath!=self.pt:
                self.count=0
                self.count2=0
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit_4.setText("")
                self.lineEdit_5.setText("")
                self.lineEdit_6.setText("")
                self.lineEdit_7.setText("")
                self.pt=filePath
                self.dataready()
            img=im.open(filePath)
            self.t_w, self.t_h=img.size
            self.target=np.array(img)
            self.backup=np.array(img)
            self.out=self.target
            qimg=imq.ImageQt(img)
            img.close()
            pixmap=QPixmap.fromImage(qimg)
            scn=QGraphicsScene()

            self.graphicsView_2.setScene((scn))
            scn.clear()
            self.graphicsView_2.setEnabled(True)
            pixmap2=scn.addPixmap(pixmap)
            self.graphicsView_2.fitInView(pixmap2, Qt.KeepAspectRatio)
            self.graphicsView_2.show()



        if self.graphicsView.isEnabled() and self.graphicsView_2.isEnabled():
            if not self.pushButton_6.isEnabled():
                self.s222()
            else:
                pass



    def s222(self):
        self.pushButton_6.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_3.setEnabled(True)
        self.lineEdit_4.setEnabled(True)
        self.lineEdit_5.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.lineEdit_6.setEnabled(True)
        self.lineEdit_7.setEnabled(True)

    def s333(self):

        if self.pushButton.isEnabled():
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_7.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_6.setStyleSheet('QPushButton {background-color: #A3C1DA;color\
                                            : black;}')
            self.getp()

        else:
            if self.count<4:
                #self.fgetp=0
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit_4.setText("")
                self.lineEdit_5.setText("")
                self.graphicsView_2.setCursor(Qt.ArrowCursor)
                self.graphicsView_2.mousePressEvent=self.store
                self.graphicsView_2.keyPressEvent=self.store2
                self.pushButton_6.setStyleSheet("")
                self.pushButton.setEnabled(True)
                self.pushButton_2.setEnabled(True)
                self.pushButton_7.setEnabled(True)
            elif self.count==4:
                self.fgetp=0
                self.lineEdit_5.setText("")
                self.graphicsView_2.setCursor(Qt.ArrowCursor)
                self.graphicsView_2.mousePressEvent=self.store
                self.graphicsView_2.keyPressEvent=self.store2
                self.pushButton_6.setStyleSheet("")
                self.pushButton.setEnabled(True)
                self.pushButton_2.setEnabled(True)
                self.pushButton_7.setEnabled(True)
                self.dataready()

    def s444(self):
        if self.pushButton.isEnabled():
            self.lineEdit_6.setText("")
            self.lineEdit_7.setText("")
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)

            self.pushButton_7.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.pushButton_8.setStyleSheet('QPushButton {background-color: #A3C1DA;color\
                                            : black;}')
            self.getp_s()

        else:
            if self.count_s<2:
                self.lineEdit_6.setText("")
                self.lineEdit_7.setText("")
                self.graphicsView.setCursor(Qt.ArrowCursor)
                self.graphicsView.mousePressEvent=self.store_s
                self.graphicsView.keyPressEvent=self.store2_s
                self.pushButton_8.setStyleSheet("")
                self.pushButton.setEnabled(True)
                self.pushButton_2.setEnabled(True)
                self.pushButton_3.setEnabled(True)
                self.pushButton_7.setEnabled(True)
            elif self.count_s==2:
                self.fgetp_s=0
                self.lineEdit_5.setText("")
                self.graphicsView.setCursor(Qt.ArrowCursor)
                self.graphicsView.mousePressEvent=self.store
                self.graphicsView.keyPressEvent=self.store2
                self.pushButton_8.setStyleSheet("")
                self.pushButton.setEnabled(True)
                self.pushButton_2.setEnabled(True)
                self.pushButton_7.setEnabled(True)
                self.dataready()



    def dataready(self):
        if self.count==4:
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.comboBox.setEnabled(True)
        else:
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.comboBox.setEnabled(False)


    def getp_s(self):
        self.count_s=0
        self.count2_s=0
        self.fgetp_s=1
        self.graphicsView.setCursor(Qt.CrossCursor)
        self.graphicsView.keyPressEvent=self.keydetect_s
        self.graphicsView.mousePressEvent=self.mouse_s

    def keydetect_s(self,event):
        if event.key()==Qt.Key_Backspace:
            if self.count2_s==1 :
                if 0<self.count_s<2:
                    self.count_s-=1
                    self.lines_s[self.count_s].setText("")

                elif self.count_s==0:
                    self.lines_s[self.count_s].setText("")
                    self.count2_s=0

                elif self.count_s==2:
                    self.lineEdit_5.setText("")
                    self.count_s-=1
                    self.lines_s[self.count_s].setText("")
            else:
                self.store2_s(event)
        else:
            self.store2_s(event)


    def mouse_s(self, event):

        if self.fgetp_s==1:
            if event.button()==Qt.LeftButton:
                if self.count_s<2:
                    a=self.graphicsView.mapToScene(event.pos())
                    x=round(a.x(),0)
                    y=round(a.y(),0)
                    self.lineEdit_5.setText("")
                    if 0<=x<self.s_w and 0<=y<self.s_h:

                         self.sp[self.count_s]=[x,y]
                         x=str(x)
                         y=str(y)
                         self.lines_s[self.count_s].setText(x+", "+y)
                         self.count_s+=1
                         self.count2_s=1
                    else:
                        x=str(x)
                        y=str(y)
                        self.lineEdit_5.setText(x+", "+y+"  Out of Bound!")


                else:
                    self.lineEdit_5.setText("Already Have 2 Source Points.")


    def getp(self):
        self.count=0
        self.count2=0
        self.fgetp=1
        self.graphicsView_2.setCursor(Qt.CrossCursor)
        self.graphicsView_2.keyPressEvent=self.keydetect
        self.graphicsView_2.mousePressEvent=self.mouse




    def keydetect(self,event):
        if event.key()==Qt.Key_Backspace:
            if self.count2==1 :
                if 0<self.count<4:
                    self.count-=1
                    self.lines[self.count].setText("")

                elif self.count==0:
                    self.lines[self.count].setText("")
                    self.count2=0

                elif self.count==4:
                    self.lineEdit_5.setText("")
                    self.count-=1
                    self.lines[self.count].setText("")


            else:
                self.store2(event)

        else:

            self.store2(event)


    def mouse(self, event):

        if self.fgetp==1:
            if event.button()==Qt.LeftButton:
                if self.count<4:
                    a=self.graphicsView_2.mapToScene(event.pos())
                    x=round(a.x(),0)
                    y=round(a.y(),0)
                    self.lineEdit_5.setText("")
                    if 0<=x<self.t_w and 0<=y<self.t_h:

                         self.tp[self.count]=[x,y]
                         x=str(x)
                         y=str(y)
                         self.lines[self.count].setText(x+", "+y)
                         self.count+=1
                         self.count2=1
                    else:
                        x=str(x)
                        y=str(y)
                        self.lineEdit_5.setText(x+", "+y+"  Out of Bound!")


                else:
                    self.lineEdit_5.setText("Already Have 4 Target Points.")






    def reset(self):

        scn=QGraphicsScene()
        self.graphicsView.setScene((scn))
        self.graphicsView_2.setScene((scn))
        scn.clear()
        self.graphicsView.setEnabled(False)
        self.graphicsView_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_6.setEnabled(False)
        self.lineEdit_7.setEnabled(False)
        self.count=0
        self.count2=0
        self.fgetp=0
        self.count_s=0
        self.count2_s=0
        self.fgetp_s=0
        self.reset_en=0
        self.pt=None
        self.ps=None








def main():
    currentApp = QApplication(sys.argv)
    currentForm = Transform()
    currentForm.show()
    currentApp.exec_()






if __name__=="__main__":
    main()