
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
import threading
import os
import time

class mainWindow(QtWidgets.QMainWindow):

    MAX_FLOWRATE = 4.0 #ml min

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
        flowRate_str = pump.setFlowrateText.text()
        try:
            flowRate = float(flowRate_str)
        except ValueError:
            print("Invalid flow rate input")
            return

        if flowRate > self.MAX_FLOWRATE:
            self.emergency_stop(
                f"Requested {flowRate} mL/min > safety limit of {self.MAX_FLOWRATE} mL/min!"
            )
            return

        pump.setFlowrate()
        print(f"Pump {pump.pumpName} running at {flowRate} mL/min")

    
    # zak emergency stop for too high flow rate
    def emergency_Stop(self, message='Emergency stop triggered'):
        print(f"X {message}")
        try:
            for pump in self.pumps:
                pump.stop()
        except Exception as e:
            print(f"Error While stopping pumps: {e}")


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
    
   
    #zak's addition
    def run_flowrate_sequence_from_csv(self, csv_file):
        """
        Run a sequence of flow rates on both pumps from a CSV file.
        CSV must contain columns 'flow_rate_a' and 'flow_rate_b'.
        delay: seconds to wait at each step
        """
        

        df = pd.read_csv(csv_file)

       
        

        if not {"flow_rate_a", "flow_rate_b","y_res_time"}.issubset(df.columns):
            raise ValueError("CSV must contain 'flow_rate_a','flow_rate_b', and 'y_res_time' columns")

        for i, row in df.iterrows():

            flow_a = float(row["flow_rate_a"])
            flow_b = float(row["flow_rate_b"])

            if flow_a > self.MAX_FLOWRATE or flow_b > self.MAX_FLOWRATE:
                self.emergency_stop(
                f"CSV step {i}: Flow too high (A={flow_a}, B={flow_b}, limit={self.MAX_FLOWRATE})"
                )
                return
            
            
            delay = (3*row["y_res_time"])*0.5

            # Pump A
            self.pump1.setFlowrateText.setText(str(row["flow_rate_a"]))
            self.pump1.setFlowrate()

            # Pump B
            self.pump2.setFlowrateText.setText(str(row["flow_rate_b"]))
            self.pump2.setFlowrate()

            print(f"[Step {i}] Pump A = {row['flow_rate_a']} | Pump B = {row['flow_rate_b']}")

            time.sleep(delay)



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

    def test_sequence(): 
        print("Starting test of Zak's CSV flowrate sequence...")
        csv_path = os.path.join(os.path.dirname(__file__), "doe_points_with_flows.csv")
        MainWindow.run_flowrate_sequence_from_csv(csv_path)
        print("Finished test sequence.")

    threading.Thread(target=test_sequence, daemon=True).start() # test sequence acitvate
    sys.exit(app.exec_())


