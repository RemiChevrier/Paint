# coding: utf-8
# https://ensip.gitlab.io/pages-info/ressources/transverse/tuto_pyqt.html#qgraphicsview-et-qgraphicsscene

import sys
from PyQt5 import QtCore,QtGui,QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self, titre,x=0,y=0,width=600,height=800):
        QtWidgets.QWidget.__init__(self) 
        self.setWindowTitle(titre)
        self.setGeometry(x,y,width,height)
        self.create_scene()
        self.view.installEventFilter(self)
        self.polygon=[]
        self.start,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0),
    def create_scene(self) :
            self.scene=QtWidgets.QGraphicsScene()
            self.view =QtWidgets.QGraphicsView(self.scene,self)
            self.view.setSceneRect(QtCore.QRectF(-200,-200,400,400))
            rect=QtWidgets.QGraphicsRectItem(100.0,0.0,100.0,200)
            rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
            self.scene.addItem(rect)
        
    def eventFilter(self, obj, event):
        if obj == self.view:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.button_press_event(event)
                return True
        return False
 
    def button_press_event(self, event):
        print("coordonnees fenetre : ",event.pos())
        c=event.pos()-self.view.pos()
        print("coordonnees vue : ",c)
        # Conversion en coordonnées scenes :
        c=self.view.mapToScene(c)
        print("coordonnees scene : ",c)
        # Ajout à la scne
        self.scene.addRect(c.x()-10,c.y()-10,20,20)
        self.polygon.append(c)
        self.setMouseTracking(True)
    def mousePressEvent(self, event):
        print("mousePressEvent()")
    def mouseMoveEvent(self, event):
        print("mouseMoveEvent()")
##        itemToDraw=QGraphicsLineItem(0,self)
##        itemToDraw.setPen(QPen(Qt.black, 3, Qt.SolidLine))
##        itemToDraw.setPos(origPoint)
        self.pStart = event.pos()
    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent()")
    def mouseDoubleClickEvent(self, event):
        print("mouseDoubleClickEvent()")
        print(self.polygon)
        qpoly=QtGui.QPolygonF(self.polygon)
        qgpoly=QtWidgets.QGraphicsPolygonItem(qpoly)
        self.scene.addItem(qgpoly)
        del self.polygon[:]
        
        
    def display(self) :
        self.view.show()
        self.show()

  
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)   
##    mw=QtWidgets.QWidget()
##    create_scene(mw)
##    mw.show()
    mw=MainWindow("Fenêtre principale")
    mw.display()

    sys.exit(app.exec_())
