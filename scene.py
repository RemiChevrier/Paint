#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QCheckBox, QInputDialog
from PyQt5.QtCore import QT_VERSION_STR

class Scene (QtWidgets.QGraphicsScene) :
    def __init__(self,parent=None) :
        self.parent = parent
        QtWidgets.QGraphicsScene.__init__(self)
        self.tool='line'
        self.begin,self.end,self.offset=QtCore.QPoint(0,0),QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.item=None
        self.create = False
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
        self.pen.setWidth(3)
        self.brush=QtGui.QBrush(QtCore.Qt.green)
        self.font = QtGui.QFont()
        self.polygon=[]
        self.Items=[]
        self.polygones = []
        #self.doubleClicked = False
        
    #    self.brush.setColor(QtCore.Qt.green)
        #rect=QtWidgets.QGraphicsRectItem(0,0,100,100)
        #rect.setPen(self.pen)
        #rect.setBrush(self.brush)
        #self.addItem(rect)
        #self.destroyItemGroup(self.item)
    
        
    def set_tool(self,tool) :
        print("set_tool(self,tool)",tool)
        self.tool=tool

    def set_pen_color(self,color) :
        self.pen.setColor(color)
    
    def set_pen_line(self,line):
        self.pen.setStyle(line)
    
    def set_pen_width(self,width) :
        self.pen.setWidth(width)
        
    def set_brush_color(self,color) :
       print("set_brush_color(self,color)",color)
       self.brush.setColor(color)

    def set_brush_style(self,style):
        self.brush.setStyle(style)

    def set_font(self,font) :
       print("set_brush_color(self,color)",font)
       self.font=font
 
    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            print("Scene.mousePressEvent()")
            self.begin = self.end = event.scenePos()
            self.item=self.itemAt(self.begin,QtGui.QTransform())

            if self.tool == 'selection':
                self.begin = self.end = event.scenePos()
                self.offsets = []
                if self.Items != []:
                    for item in self.Items:
                        self.offsets.append(self.begin-item.pos())

            elif self.item :
                self.offset = self.begin-self.item.pos()

            else:
                self.create = True

            if self.tool == 'polygone':
                    c=event.scenePos()
                    print("coordonnees vue : ",c)
                    print("coordonnees scene : ",c)
                    self.polygon.append(c)
                    print(self.polygon)
                        
            elif self.tool == 'text':
                plainText, ok = QInputDialog.getText(self.parent, 'Write Text', 'Enter your text')
                if ok:
                    c=event.scenePos()
                    self.addTextToScene(plainText, c, self.font)
            
            

                
    def mouseMoveEvent(self, event):
        # print("Scene.mouseMoveEvent()")
        if self.item :
            self.item.setPos(event.scenePos() - self.offset)
        #self.end = event.scenePos()

        elif self.tool == "selection":
            if self.Items != []:
                i = 0
                for item in self.Items:
                    item.setPos(event.scenePos() - self.offsets[i])
                    i += 1        

    def mouseDoubleClickEvent(self, event):
        if self.tool == "polygone":
            print("mouseDoubleClickEvent()")
            print(self.polygon)
            self.ctrl = True
            self.drawPolygone(self.polygon, self.pen, self.brush)  # dessin ac paramètres actuels  
            del self.polygon[:]
            #self.doubleClicked = True
            
 
    def mouseReleaseEvent(self, event):
        print("Scene.mouseReleaseEvent()",self.tool)
        
        self.end = event.scenePos()
        """items = []
        for self.item in items:
                print("item",self.item)"""
        if self.item :
            
            print(" item ")
            print(self.item.__class__.__name__)
            print(event.pos())

            self.item.setPos(event.scenePos() - self.offset)
            self.item.ungrabMouse()
            self.item=None

        elif self.tool == "selection":
            if self.Items != []:
                i = 0
                for item in self.Items:
                    item.setPos(event.scenePos() - self.offsets[i])
                    i += 1
                self.Items = []
                self.offsets = []

            else:
                for item in self.items() :
                    if item.pos().x() > self.begin.x():
                        if item.pos().x() < self.end.x():
                            if item.pos().y() > self.begin.y():
                                if item.pos().y() < self.end.y():
                                    self.Items.append(item)
                            elif item.pos().y() < self.begin.y():
                                if item.pos().y() > self.end.y():
                                    self.Items.append(item)

                    elif item.pos().x() < self.begin.x():
                        if item.pos().x() > self.end.x():
                            if item.pos().y() > self.begin.y():
                                if item.pos().y() < self.end.y():
                                    self.Items.append(item)
                            elif item.pos().y() < self.begin.y():
                                if item.pos().y() > self.end.y():
                                    self.Items.append(item)
                print(self.Items)

        elif self.create:
            self.create = False
            if self.tool=='line' :
                self.addLine(self.begin.x(), self.begin.y(),self.end.x(), self.end.y(),self.pen)
            elif self.tool=='rect' :
                self.drawRectangle(QtWidgets.QGraphicsRectItem(self.begin.x(),
                                                                    self.begin.y(),
                                                                    self.end.x()-self.begin.x(),
                                                                    self.end.y()-self.begin.y()).rect(),
                                                                    self.pen, 
                                                                    self.brush)
            elif self.tool=='ellipse' :
                self.drawEllipse(QtWidgets.QGraphicsEllipseItem(self.begin.x(), self.begin.y(),self.end.x()-self.begin.x(), 
                self.end.y()-self.begin.y()).rect(), self.pen, self.brush)
                

            else :
                print("no item selected and nothing to draw !")
        
    def drawRectangle(self, rect, pen, brush):
        rectangle=QtWidgets.QGraphicsRectItem(rect)
        rectangle.setPen(pen)
        rectangle.setBrush(brush)
        self.addItem(rectangle)

    def drawEllipse(self, rect, pen, brush):
        ellipse=QtWidgets.QGraphicsEllipseItem(rect)
        ellipse.setPen(pen)
        ellipse.setBrush(brush)
        self.addItem(ellipse)

    def drawPolygone(self, polygon, pen, brush):
        self.polygones.insert(0, list(polygon))
        polygone=QtGui.QPolygonF(polygon)
        qgpoly=QtWidgets.QGraphicsPolygonItem(polygone)
        qgpoly.setPen(pen)
        qgpoly.setBrush(brush)
        self.addItem(qgpoly)


    def addTextToScene(self, plainText, pos, font):
        text = QtWidgets.QGraphicsTextItem()
        text.setPlainText(plainText)
        text.setPos(pos)
        text.setFont(font)
        self.addItem(text)
        
