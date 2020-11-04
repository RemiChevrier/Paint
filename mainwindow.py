#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QShortcut, QApplication, QWidget, QPushButton, QMessageBox, QGraphicsLineItem, QFontDialog, QMenu
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.QtGui import QIcon, QPen, QPainter, QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
import pickle
from scene import Scene


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.resize(500, 300)
        self.setWindowTitle("Editeur v0.1")
        self.create_scene()
        self.create_actions()
        self.create_menus()
        self.connect_actions()
        
##        textEdit = QtGui.QTextEdit()
##        self.setCentralWidget(textEdit)
    def create_scene(self) :
        self.filename = ""
        self.view=QtWidgets.QGraphicsView()
        self.scene=Scene(self)
        #text= self.scene.addText("Hello World !")
    #    text.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        #text.setPos(100,200)
    #    text.setVisible(True)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)
        self.view.installEventFilter(self)

    def create_actions(self) :
        self.action_new = QtWidgets.QAction(QtGui.QIcon('icons/new.png'), 'New', self)
        self.action_new.setShortcut('Ctrl+N')
        self.action_new.setStatusTip('Open a new file')

        self.action_save = QtWidgets.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        self.action_save.setShortcut('Ctrl+S')
        self.action_save.setStatusTip('Save to file')

        self.action_save_as = QtWidgets.QAction(QtGui.QIcon('icons/save_as.png'), 'Save as', self)
        self.action_save_as.setShortcut('Ctrl+Shift+S')
        self.action_save_as.setStatusTip('Save as')

        self.action_open = QtWidgets.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        self.action_open.setShortcut('Ctrl+O')
        self.action_open.setStatusTip('Open file')

        self.action_exit = QtWidgets.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        self.action_exit.setShortcut('Ctrl+Q')
        self.action_exit.setStatusTip('Exit application')

        self.group_action_tools = QtWidgets.QActionGroup(self)
        self.action_selection = QtWidgets.QAction(self.tr("&Selection"), self)
        self.action_selection.setCheckable(True)
        self.action_selection.setChecked(False)

        self.action_line = QtWidgets.QAction(self.tr("&Line"), self)
        self.action_line.setCheckable(True)
        self.action_line.setChecked(False)

        self.action_rect = QtWidgets.QAction(self.tr("&Rectangle"), self)
        self.action_rect.setCheckable(True)
        self.action_rect.setChecked(False)

        self.action_ellipse = QtWidgets.QAction(self.tr("&Ellipse"), self)
        self.action_ellipse.setCheckable(True)
        self.action_ellipse.setChecked(False)

        self.action_polygone = QtWidgets.QAction(self.tr("&Polygone"), self)
        self.action_polygone.setCheckable(True)
        self.action_polygone.setChecked(False)

        self.action_text = QtWidgets.QAction(self.tr("&Text"), self)
        self.action_text.setCheckable(True)
        self.action_text.setChecked(False)

        self.group_action_tools.addAction(self.action_selection)
        self.group_action_tools.addAction(self.action_line)
        self.group_action_tools.addAction(self.action_rect)
        self.group_action_tools.addAction(self.action_ellipse)
        self.group_action_tools.addAction(self.action_polygone)
        self.group_action_tools.addAction(self.action_text)
        
        self.group_action_penStyle = QtWidgets.QActionGroup(self)

        self.action_SolidLine = QtWidgets.QAction(self.tr("SolidLine"), self)
        self.action_SolidLine.setCheckable(True)
        self.action_SolidLine.setChecked(True)

        self.action_DashDotLine = QtWidgets.QAction(self.tr("DashDotLine"), self)
        self.action_DashDotLine.setCheckable(True)
        self.action_DashDotLine.setChecked(False)

        self.action_DotLine = QtWidgets.QAction(self.tr("DotLine"), self)
        self.action_DotLine.setCheckable(True)
        self.action_DotLine.setChecked(False)

        self.action_DashLine = QtWidgets.QAction(self.tr("DashLine"), self)
        self.action_DashLine.setCheckable(True)
        self.action_DashLine.setChecked(False)

        self.action_DashDotDotLine = QtWidgets.QAction(self.tr("DashDotDotLine"), self)
        self.action_DashDotDotLine.setCheckable(True)
        self.action_DashDotDotLine.setChecked(False)

        self.group_action_penStyle.addAction(self.action_SolidLine)
        self.group_action_penStyle.addAction(self.action_DashDotLine)
        self.group_action_penStyle.addAction(self.action_DotLine)
        self.group_action_penStyle.addAction(self.action_DashLine)
        self.group_action_penStyle.addAction(self.action_DashDotDotLine)

        self.action_pen_color = QtWidgets.QAction(self.tr("Color"), self)
        self.action_pen_line = QtWidgets.QAction(self.tr("Line"), self)
        self.action_pen_width = QtWidgets.QAction(self.tr("Width"), self)                      

        self.action_brush_color = QtWidgets.QAction(self.tr("Color"), self)
        self.action_text_font = QtWidgets.QAction(self.tr("Font"), self)


        self.group_action_brushStyle = QtWidgets.QActionGroup(self)

        self.action_brush_solidPattern=QtWidgets.QAction(self.tr("SolidPattern"), self)
        self.action_brush_solidPattern.setCheckable(True)
        self.action_brush_solidPattern.setChecked(True)
        self.action_brush_verticalPattern=QtWidgets.QAction(self.tr("VerticalPattern"), self)
        self.action_brush_verticalPattern.setCheckable(True)
        self.action_brush_verticalPattern.setChecked(False)

        self.group_action_brushStyle.addAction(self.action_brush_solidPattern)
        self.group_action_brushStyle.addAction(self.action_brush_verticalPattern)

        self.action_about_us = QtWidgets.QAction(self.tr("About this Editor"), self)
        self.action_about_qt = QtWidgets.QAction(self.tr("About Qt"), self)
        self.action_about_app = QtWidgets.QAction(self.tr("About the Application"), self)

        self.fileShortcut = QShortcut(QKeySequence('Ctrl+F'), self)
        self.toolShortcut = QShortcut(QKeySequence('Ctrl+T'), self)
        self.styleShortcut = QShortcut(QKeySequence('Ctrl+W'), self)
        self.helpShortcut = QShortcut(QKeySequence('Ctrl+H'), self)

    def create_menus(self) :
 #       statusbar=self.statusBar()
        self.menubar = self.menuBar()
        self.menu_file = self.menubar.addMenu('&File')
        self.menu_file.addAction(self.action_new)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_save_as)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)      
       
        self.menu_tools = self.menubar.addMenu('&Tools')
        self.menu_tools.addAction(self.action_selection)
        self.menu_tools.addSeparator()
        self.menu_tools.addAction(self.action_line)
        self.menu_tools.addAction(self.action_rect)
        self.menu_tools.addAction(self.action_ellipse)
        self.menu_tools.addAction(self.action_polygone)
        self.menu_tools.addSeparator()
        self.menu_tools.addAction(self.action_text)    
      

        self.menu_style=self.menubar.addMenu('&Style')
        menu_style_pen=self.menu_style.addMenu('Pen')
        menu_style_pen.addAction(self.action_pen_color)        
        menu_style_pen.addAction(self.action_pen_width)

        menu_pen_line = menu_style_pen.addMenu('&Line')
        menu_pen_line.addAction(self.action_SolidLine)
        menu_pen_line.addAction(self.action_DashDotLine)
        menu_pen_line.addAction(self.action_DotLine)
        menu_pen_line.addAction(self.action_DashLine)
        menu_pen_line.addAction(self.action_DashDotDotLine)

        menu_style_brush=self.menu_style.addMenu('Brush')
        menu_style_brush.addAction(self.action_brush_color)

        menu_style_brush_fill=menu_style_brush.addMenu('Fill')
        menu_style_brush_fill.addAction(self.action_brush_solidPattern)
        menu_style_brush_fill.addAction(self.action_brush_verticalPattern)
        self.menu_style.addAction(self.action_text_font)

        self.menu_help=self.menuBar().addMenu(self.tr("&Help"))
        self.menu_help.addAction(self.action_about_us)
        self.menu_help.addAction(self.action_about_qt)
        self.menu_help.addAction(self.action_about_app)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(self.action_exit)
        toolbar = self.addToolBar('Open')
        toolbar.addAction(self.action_open)
        toolbar = self.addToolBar('Save')
        toolbar.addAction(self.action_save)
        toolbar = self.addToolBar('New')
        toolbar.addAction(self.action_new) 
                
        

        self.popupMenu = QMenu( "Standard PopupMenu", self )  
        self.popupMenu.addMenu(self.menu_tools)        
        self.popupMenu.addMenu(self.menu_style)
        self.popupMenu.addSeparator()
        self.popupMenu.addAction(self.action_new)


 

    def connect_actions(self) :
        self.action_new.triggered.connect(self.new_file)
        self.action_open.triggered.connect(self.file_open)
        self.action_save.triggered.connect(self.file_save)
        self.action_save_as.triggered.connect(self.file_save_as)
        self.action_exit.triggered.connect(self.file_exit)
    

        self.action_pen_color.triggered.connect(self.pen_color_selection)
        self.action_pen_width.triggered.connect(self.pen_width_selection)

        self.action_SolidLine.triggered.connect(lambda checked, line=Qt.SolidLine: self.set_action_line(checked, line))
        self.action_DashDotLine.triggered.connect(lambda checked, line=Qt.DashDotLine: self.set_action_line(checked, line))
        self.action_DotLine.triggered.connect(lambda checked, line=Qt.DotLine: self.set_action_line(checked, line))
        self.action_DashLine.triggered.connect(lambda checked, line=Qt.DashLine: self.set_action_line(checked, line))
        self.action_DashDotDotLine.triggered.connect(lambda checked, line=Qt.DashDotDotLine: self.set_action_line(checked, line))
        
        self.action_brush_color.triggered.connect(self.brush_color_selection)
        self.action_selection.triggered.connect(lambda checked, tool="selection": self.set_action_tool(checked,tool))
        self.action_line.triggered.connect(lambda checked, tool="line": self.set_action_tool(checked,tool))
        self.action_rect.triggered.connect(lambda checked, tool="rect": self.set_action_tool(checked,tool))
        self.action_ellipse.triggered.connect(lambda checked, tool="ellipse": self.set_action_tool(checked,tool))
        self.action_polygone.triggered.connect(lambda checked, tool="polygone": self.set_action_tool(checked,tool))
        self.action_text.triggered.connect(lambda checked, tool="text": self.set_action_tool(checked,tool))
        self.action_text_font.triggered.connect(lambda checked: self.text_font_selection())

        self.action_brush_solidPattern.triggered.connect(lambda checked, style=Qt.SolidPattern: self.set_action_brushStyle(checked, style))
        self.action_brush_verticalPattern.triggered.connect(lambda checked, style=Qt.VerPattern: self.set_action_brushStyle(checked, style))
    
        self.action_about_us.triggered.connect(self.help_about_us)
        self.action_about_qt.triggered.connect(self.help_about_qt)
        self.action_about_app.triggered.connect(self.help_about_app)

        self.fileShortcut.activated.connect(self.showFileMenu)
        self.toolShortcut.activated.connect(self.showToolMenu)
        self.styleShortcut.activated.connect(self.showStyleMenu)
        self.helpShortcut.activated.connect(self.showHelpMenu)

    def showFileMenu(self):
        self.menu_file.popup(self.view.mapToGlobal(self.view.pos())-QtCore.QPoint(-5, 100))
        #self.menu_file.mousePressEvent(QtCore.QEvent.QMouseEvent())

    def showToolMenu(self):
        self.menu_tools.popup(self.view.mapToGlobal(self.view.pos())-QtCore.QPoint(-45, 100))

    def showStyleMenu(self):
        self.menu_style.popup(self.view.mapToGlobal(self.view.pos())-QtCore.QPoint(-85, 100))

    def showHelpMenu(self):
        self.menu_help.popup(self.view.mapToGlobal(self.view.pos())-QtCore.QPoint(-125, 100))


    def set_action_tool(self,checked, tool) :
        print("lamda checked, tool : ",checked, tool)
        self.scene.set_tool(tool)
    
    def set_action_line(self, checked, line):
        print(checked)
        #checked =False
        self.scene.set_pen_line(line)
        
    def set_action_brushStyle(self, checked, style):
        print(checked)
        self.scene.set_brush_style(style)
    
    def file_exit(self):
        #self.action_exit.setGeometry(10,10,60,35)
        #self.connect(self.action_exit, QtCore.SIGNAL('clicked()'), self.changeTitre)

        buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you want to save?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if buttonReply == QMessageBox.Yes:
            self.file_save()
        if buttonReply == QMessageBox.No:
            exit()
        else:
            QMessageBox.information(self, 'Welcome Back','Welcome back to the App')
        self.show()
        
    def file_open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getcwd())
        print(filename[0])
        fileopen=QtCore.QFile(filename[0])
        if fileopen.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)==None or filename[0] == "" :
            print("fileopen.open(QtCore.QIODevice.WriteOnly)==None")
            return -1
        else :
            self.create_scene()
            self.filename = filename[0]
            self.setWindowTitle("Editeur v0.1 - " + self.filename)
            print(filename[0] + " opened !")
            filehandler = open(filename[0], 'rb')
            dict2Load = pickle.load(filehandler)

            for Type in dict2Load['Ordre']:
                if Type == 3:
                    info = dict2Load['Rectangle'][0]
 
                    rect = info[0]
                    pen_color = info[1]
                    width = info[2]
                    pen_style = info[3]
                    brush_color = info[4]
                    brush_style = info[5]

                    pen=QtGui.QPen()
                    pen.setColor(pen_color)
                    pen.setWidth(width)
                    pen.setStyle(pen_style)
                    brush=QtGui.QBrush(brush_color)
                    brush.setStyle(brush_style)

                    self.scene.drawRectangle(rect, pen, brush)
                    del dict2Load['Rectangle'][0]

                elif Type == 4:
                    info = dict2Load['Ellipse'][0]
                    
                    rect = info[0]
                    pen_color = info[1]
                    width = info[2]
                    pen_style = info[3]
                    brush_color = info[4]
                    brush_style = info[5]

                    pen=QtGui.QPen()
                    pen.setColor(pen_color)
                    pen.setWidth(width)
                    pen.setStyle(pen_style)
                    brush=QtGui.QBrush(brush_color)
                    brush.setStyle(brush_style)

                    self.scene.drawEllipse(rect, pen, brush)
                    del dict2Load['Ellipse'][0]

                elif Type == 5:
                    info = dict2Load['Polygone'][0]
                    polygon = info[0]
                    pen_color = info[1]
                    width = info[2]
                    pen_style = info[3]
                    brush_color = info[4]
                    brush_style = info[5]

                    pen=QtGui.QPen()
                    pen.setColor(pen_color)
                    pen.setWidth(width)
                    pen.setStyle(pen_style)
                    brush=QtGui.QBrush(brush_color)
                    brush.setStyle(brush_style)

                    self.scene.drawPolygone(polygon, pen, brush)

                    del dict2Load['Polygone'][0]
                
                elif Type == 6:
                    info = dict2Load['Line'][0]
                    pos1 = info[0]
                    pos2 = info[1]
                    pen_color = info[2]
                    width = info[3]
                    style = info[4]

                    pen=QtGui.QPen()
                    pen.setColor(pen_color)
                    pen.setWidth(width)
                    pen.setStyle(style)

                    self.scene.addLine(pos1.x(), pos1.y(), pos2.x(), pos2.y(), pen)
                    del dict2Load['Line'][0]

                elif Type == 8:
                    info = dict2Load['Text'][0]
                    plainText = info[0]
                    pos = info[1]
                    string = info[2]
                    size = info[3]
                    style = info[4]
                    bold = info[5]
                    italica = info[6]
                    hint = info[7]
                    name = info[8]

                    font = QtGui.QFont(string)
                    font.setPointSize(size)
                    font.setStyle(style)
                    font.setBold(bold)
                    font.setItalic(italica)
                    font.setStyleHint(hint)
                    font.setStyleName(name)
                    
                    self.scene.addTextToScene(plainText, pos, font)
                    del dict2Load['Text'][0]
                

    def file_save_as(self):
        filename = self.chooseFilename()
        print(filename)
        if filename == -1:
            return
        self.filename = filename
        self.file_save()

    def chooseFilename(self):
        filename= QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.getcwd())
        filesave=QtCore.QFile(filename[0])
        if filesave.open(QtCore.QIODevice.WriteOnly)==None or filename[0] == "" :
            print("filesave.open(QtCore.QIODevice.WriteOnly)==None")
            return -1
        else :
            return filename[0]
    
    def file_save(self):
        if self.filename == "":
            filename = self.chooseFilename()
            if filename == -1:
                return
            self.filename = filename
        self.setWindowTitle("Editeur v0.1 - " + self.filename)
        print(self.filename + " ready to save !")
        dict2Save = {'Rectangle' : [], 'Ellipse':[], 'Text':[], "Line" : [], "Polygone": [], "Ordre":[]}
        i = 0
        for item in self.scene.items():
            print(item.type(), QtWidgets.QGraphicsRectItem.type)
            if item.type() == 3: #rectangle
                dict2Save['Ordre'].insert(0, 3)
                print ("Rectangle", item.pos(), item.rect())
                dict2Save['Rectangle'].insert(0,(item.rect(), item.pen().color(), item.pen().width(), item.pen().style(), item.brush().color(), item.brush().style()))

            elif item.type() == 8: #text
                dict2Save['Ordre'].insert(0, 8)
                print ("text",  item.toHtml(), item.pos())
                dict2Save['Text'].insert(0,(item.toPlainText(), item.pos(), item.font().toString(), item.font().pointSize(), 
                item.font().style(), item.font().bold(), item.font().italic(), item.font().styleHint(), item.font().styleName()))

            elif item.type() == 4: #ellipse
                dict2Save['Ordre'].insert(0, 4)
                print ("ellipse",  item.rect())
                dict2Save['Ellipse'].insert(0,(item.rect(), item.pen().color(), item.pen().width(), item.pen().style(), item.brush().color(), item.brush().style()))

            elif item.type() == 6: #Line
                dict2Save['Ordre'].insert(0, 6)
                print ("line", item.line().p1(), item.line().p2(), item.pen().color(), item.pen().width())
                dict2Save['Line'].insert(0,(item.line().p1(), item.line().p2(), item.pen().color(), item.pen().width(), item.pen().style()))
            
            elif item.type() == 5: #Polygone
                dict2Save['Ordre'].insert(0, 5)
                print ("polygone", self.scene.polygones[i])
                dict2Save['Polygone'].insert(0,(self.scene.polygones[i], item.pen().color(), item.pen().width(), 
                item.pen().style(), item.brush().color(), item.brush().style()))
                i+=1
                
        with open(self.filename, 'wb') as output:
            pickle.dump(dict2Save, output)
    
    def new_file(self):
        buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you want to save?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if buttonReply == QMessageBox.Yes:
            self.file_save()
        elif buttonReply == QMessageBox.No:
            self.create_scene()
        else:
            QMessageBox.information(self, 'Welcome Back','Welcome back to the App')
        

    def pen_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self )
        if color.isValid() :
            print("Color Choosen : ",color.name())
            self.scene.set_pen_color(color) 
        else :
            print("color is not a valid one !")
            
    def text_font_selection(self):
        print("dialogfont")
        font, ok = QFontDialog.getFont()
        if ok:
            self.scene.set_font(font) 
    
    def pen_width_selection(self):
        width, ok = QtWidgets.QInputDialog.getInt(self, "Width", "Entrer Width", value = 3, min = 1, max = 20, step = 1)
        if ok:
            self.scene.set_pen_width(width)

    def brush_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self )
        if color.isValid() :
            print("Color ChopopupMenusen : ",color.name())
            self.scene.set_brush_color(color)
        else :
            print("color is not a valid one !")
        
    def help_about_us(self):
        QtWidgets.QMessageBox.information(self, self.tr("About Me"),
                                self.tr("Rémi Chevrier\n copyright ENIB 2020"))

    def help_about_qt(self):
        QtWidgets.QMessageBox.information(self, self.tr("About Qt"),
                                self.tr("Qt est une API orientée objet et développée en C++, conjointement par The Qt Company et Qt Project.Qt offre des composants d'interface graphique (widgets), d'accès aux données, de connexions réseaux, de gestion des fils d'exécution, d'analyse XML, etc. ;"))
    def help_about_app(self):
        text=open('README.txt').read()
        QtWidgets.QMessageBox.information(self, self.tr("About Me"),
                                self.tr(text))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.file_exit()        

    def eventFilter(self, obj, event):
        if (obj != self.view) :
            if event.type() == QtCore.QEvent.MouseButtonPress & QtCore.Qt.RightButton:
                return True
        return False

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.RightButton:
            self.popupMenu.popup(QtGui.QCursor.pos())
            print("Mw.mousePressEvent()")

if __name__ == "__main__" :  
    print(QT_VERSION_STR)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
