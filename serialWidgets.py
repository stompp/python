from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QWidget, QPushButton,QComboBox,QVBoxLayout,QHBoxLayout
from PyQt5.QtWidgets import QTextEdit,QGridLayout,QColorDialog, QScrollBar,QCheckBox
from PyQt5.QtGui import QIntValidator, QTextCursor

import sys
import serial
import serial.tools.list_ports

from serialhelper import SerialHelper
from pyqt5Utils import *
class PortScannerWidget(QWidget):
    def __init__(self, vertical = True):
        super(PortScannerWidget,self).__init__()
        
       
        self.port = 0

        self.scan_btn = QPushButton("Scan", self)
        self.scan_btn.clicked.connect(self.scanPorts)


        self.ports_co = QComboBox(self)
        self.ports_co.activated[str].connect(self.portSelected)
      

        self.rate_co = QComboBox(self)
        self.rate_co.addItems(map(str,serial.Serial.BAUDRATES))

        self.rate_le = QLineEdit(self)
        self.rate_co.setLineEdit(self.rate_le)
        self.rate_le.setText("115200")
      
        onlyInt = QIntValidator()
        self.rate_le.setValidator(onlyInt)

        
        if vertical == True:
             self.lo = QVBoxLayout(self)
        else:
            self.lo = QHBoxLayout(self)       
            

               
        self.lo.addWidget(self.scan_btn)
        self.lo.addWidget(self.ports_co)
        self.lo.addWidget(self.rate_co)
     
       
        self.scanPorts()

    def scanPorts(self):
        

        try:
            self.ports_co.clear()
            self.ports = serial.tools.list_ports.comports()

            for port in self.ports:
                self.ports_co.addItem(port.description)

            if len(self.ports) > 0 : 
                self.portSelected(self.ports[0].description) 
        except:
            print("Scanning error")

    def portSelected(self,value):
        try:
           
            for port in self.ports:
                if port.description == value:
                    self.port = port
                    print(f"Device is {self.port.device}")
        except:
            print("Port selected error")

    def baudRate(self): 
        return int(self.rate_le.text())

    def device(self):
        return self.port.device

    def data(self):
        return self.port.device, int(self.rate_le.text())
 

class SerialMonitor(QWidget):

    def __init__(self, vertical = True, _serial = 0):
        super(SerialMonitor,self).__init__()
        self.setWindowTitle("Monitor")
        if vertical:
            self.portScanner = PortScannerWidget(False)
        else:
            self.portScanner = PortScannerWidget(True)

        self.monitor = MonitorWidget()

        self.monitor.setEnabled(False)
        self.isConnected = False

        self.connect_button = QPushButton("Start", self)
        self.connect_button.clicked.connect(self.connectButtonPressed)

        # self.color_button = QPushButton("Set Color", self)
        # self.color_button.clicked.connect(self.color)

        if _serial == 0:
            self.serial = SerialHelper()
        else:
            self.serial = _serial

        self.serial.on_msg_sent.add(self.monitor.logSent)
        self.serial.info_broadcaster.add(self.monitor.logSystem)
        # test_btn = QPushButton("Test",self)
        # test_btn.clicked.connect(self.test)

        # serial_v_lo = QVBoxLayout()

        # serial_v_lo.addWidget(self.portScanner)


        # self.portScanner.lo.addWidget(self.connect_button)
        # self.portScanner.lo.addStretch()
        # serial_v_lo.addWidget(self.connect_button)
        # serial_v_lo.addWidget(self.color_button)

        if vertical :
            self.lo = QVBoxLayout(self)
            self.portAndConnectlo = QHBoxLayout()
           
        else :
            self.lo = QHBoxLayout(self)
            self.portAndConnectlo = QVBoxLayout()

        self.portAndConnectlo.addWidget(self.portScanner)
        self.portAndConnectlo.addWidget(self.connect_button)
        self.portAndConnectlo.addStretch()

        
        self.msgOptions = MonitorMsgOptions(self.serial.connection_succes_msg,self.serial.start_marker,self.serial.end_marker,False)
        self.msgOptions.welcome.line_edit.textChanged.connect(self.messageOptionChanged)
        self.msgOptions.start.line_edit.textChanged.connect(self.messageOptionChanged)
        self.msgOptions.end.line_edit.textChanged.connect(self.messageOptionChanged)
        self.msgOptions.line_adjustments_cb.setSelectedLineAdjustment(self.serial.line_adjustment)
        self.msgOptions.line_adjustments_cb.currentIndexChanged.connect(self.messageOptionChanged)
        self.msgOptions.lo.addStretch()
      



        
        # self.lo = QHBoxLayout(self)
        self.lo.addLayout(self.portAndConnectlo)
        self.lo.addWidget(self.msgOptions)
        # h_lo.addWidget(self.portScanner)
        # self.lo.addWidget(self.msgOptions)
        self.lo.addWidget(self.monitor)

        self.monitor.on_send_message.add(self.sendMessagePrint)
        self.monitor.on_send_message.add(self.serial.sendStr)
        self.serial.on_msg_received.add(self.monitor.log)

    # def color(self):
    #     color = QColorDialog.getColor()

    #     if color.isValid():
    #        self.serial.sendStr(f"R{color.red()},{color.green()}.{color.blue()}")
        

    
    def connectButtonPressed(self):

        if self.isConnected:
            try:
                self.serial.disconnect()
            except: 
                print("Disconnect error")
            self.isConnected = False
        
        else:

            try:
                device,rate = self.portScanner.data()
                # print(f"Device is {device} and rate is {rate}")
                self.serial.port = device
                self.serial.baudrate = rate
                if self.serial.connect():
                    self.isConnected = True
                
                    # print("Connected")

                    # self.serial.on_msg_received_actions.append(self.monitor.log)

            except:
                print("Test Error")

        if self.isConnected:
            self.isConnected = True
            self.monitor.setEnabled(True)
            self.portScanner.setEnabled(False)
            self.connect_button.setText("Stop")
        else:
            self.isConnected = False
            self.monitor.setEnabled(False)
            self.portScanner.setEnabled(True)
            self.connect_button.setText("Start")


    def test(self):
        try:
            device,rate = self.portScanner.data()
            print(f"Device is {device} and rate is {rate}")
        except:
            print("Test Error")


    def sendMessagePrint(self, msg):
        print("Sending " + msg)


    def messageOptionChanged(self, text):
        sender = self.sender()
        if sender == self.msgOptions.welcome.line_edit:
            self.serial.connection_succes_msg = text
        elif sender == self.msgOptions.start.line_edit:
            self.serial.start_marker = text
        elif sender == self.msgOptions.end.line_edit:
            self.serial.end_marker = text
        elif sender == self.msgOptions.line_adjustments_cb:
            # print( f"current index selected is {self.msgOptions.line_adjustments_cb.currentIndex()}")
            self.serial.line_adjustment = self.msgOptions.line_adjustments_cb.lineAdjustment()







if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SerialMonitor()
    w.show()    
    sys.exit(app.exec_())




    
