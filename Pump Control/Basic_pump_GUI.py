
from ast import Return
from pickle import FALSE
import typing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
import sys
import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSlot
import pumpWidget as pw
import datetime



class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        global windowRun
        windowRun = False
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        # self.tab_main = QtWidgets.QTabWidget(self)
        # self.tab_main.layout = QtWidgets.QGridLayout()
        # self.tab_main.setStyleSheet("QTabBar::tab { height: 30px; width: 150px }")
        self.layout = QtWidgets.QGridLayout(self.centralWidget)

        self.pumpsBox = QtWidgets.QGroupBox("Pumps")
        self.pumpsBox.setMaximumHeight(400)
        self.pumpsBox.setMaximumWidth(1000)
        self.pumpsBox.setHidden(False)
        self.pumpsLayout = QtWidgets.QGridLayout(self.pumpsBox)
        self.layout.addWidget(self.pumpsBox)

        self.pump1 = pw.PumpControl(self, pumpName="Pump A")
        self.pump1.pumpModelCombo.setCurrentText("MilliGAT LF")
        self.pump1.formatWidget(pump="MilliGAT LF")
        self.pumpsLayout.addWidget(self.pump1, 0, 0, QtCore.Qt.AlignLeft)
        
        self.pump2 = pw.PumpControl(self, pumpName="Pump B")
        self.pump2.pumpModelCombo.setCurrentText("MilliGAT LF")
        self.pump2.formatWidget(pump="MilliGAT LF")
        self.pumpsLayout.addWidget(self.pump2, 0, 1, QtCore.Qt.AlignLeft)
        self.pumps = [self.pump1, self.pump2]

        self.pumpALLButton = QtWidgets.QPushButton("RUN ALL")
        self.pumpALLButton.setFixedSize(50, 25)
        self.pumpALLButton.setStyleSheet("background-color: #549c55;" "color: white;" "border-radius:5px")
        self.pumpALLButton.clicked.connect(self.pump_ALL)
        self.pumpsLayout.addWidget(self.pumpALLButton,0, 2, QtCore.Qt.AlignLeft)
        


    def pump_ALL(self):
        for pump in self.pumps:
            value = 1
            self.setFlowrates(pump)
        print("pump ALL", str(datetime.datetime.now()))


    def setFlowrates(self, pump):
        flowRate = pump.setFlowrateText.text()
        print("fR=",flowRate)
        # pumpModel = pump.pumpModelCombo.currentText()
        # print(pumpModel)
        pump.setFlowrate()
        # try:
        #     if pumpModel == 'MilliGAT HF':
        #         pump.set_flow_rate(float(flowRate), pump_type='HF')
        #     elif pumpModel == "MilliGAT LF":
        #         pump.set_flow_rate(float(flowRate), pump_type="LF")
        #     elif pumpModel == 'Chemyx Fusion 6000X':
        #         pump.setRate(rate=flowRate, x=0)
        # except:
        #     print('No pump connected')

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Pump Controller")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Pump Controller", "Pump Controller"))
    



if __name__ == "__main__":
    import sys
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = mainWindow()
    ui = mainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setMinimumSize(1200, 600)
    MainWindow.show()
    sys.exit(app.exec_())


