from http.server import ThreadingHTTPServer
from operator import add
from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIntValidator
import bluetooth
import sys
import threading
from bluetooth import address
from bluetooth.native_socket import BluetoothSocket
from serial import serial_for_url
from bluetoothHelper import *
from pyqt5Utils import *
def get_nearby_devices():
    nearby_devices = bluetooth.discover_devices(duration=3, lookup_names=True)
    # print("Found {} devices.".format(len(nearby_devices)))
    # print(type(nearby_devices))
    # for addr, name in nearby_devices:
    #     print("  {} - {}".format(addr, name))

    # for d in nearby_devices:
    #     print(type(d))
    #     print(d)
    return nearby_devices

# get_nearby_devices()


class DeviceScanner(QWidget):
    def __init__(self, vertical=True):
        super(DeviceScanner, self).__init__()

        self.nearby_devices = list()
        self.device = tuple()

        # self.sc = BluetoothSocketHelper()

        # self.test_send_btn = QPushButton("Test", self)
        # self.test_send_btn.clicked.connect(self.testSend)

        self.scan_btn = QPushButton("Scan", self)
        self.scan_btn.clicked.connect(self.info_scanning)
        self.scan_btn.clicked.connect(self.scanDevices)

        self.searching_info_lbl = QLabel("No devices")

        self.devices_co = QComboBox(self)
        self.devices_co.activated[int].connect(self.deviceSelected)
        self.devices_co.setFixedWidth(200)

        # self.rate_co = QComboBox(self)
        # self.rate_co.addItems(map(str,serial.Serial.BAUDRATES))

        # self.rate_le = QLineEdit(self)
        # self.rate_co.setLineEdit(self.rate_le)
        # self.rate_le.setText("115200")

        # onlyInt = QIntValidator()
        # self.rate_le.setValidator(onlyInt)

        if vertical == True:
            self.lo = QVBoxLayout(self)
        else:
            self.lo = QHBoxLayout(self)

        self.lo.addWidget(self.scan_btn)

        # self.lo.addSpacing(5)
        self.lo.addStretch()
        self.lo.addWidget(self.searching_info_lbl)
        self.lo.addStretch()
        self.lo.addWidget(self.devices_co)

        # self.lo.addWidget(self.test_send_btn)
        self.setFixedWidth(400)

        # self.lo.addWidget(self.rate_co)

        # self.scanPorts()

    def info_scanning(self):
     
        self.scan_btn.setEnabled(False)
        self.searching_info_lbl.setText("Scanning")

    def scanDevicesThread(self):

        # self.searching_info_lbl.setText("Searching")
        try:

            self.devices_co.clear()

            print("Searching...")

            self.nearby_devices = bluetooth.discover_devices(
                duration=3, lookup_names=True)

            for addr, name in self.nearby_devices:
                self.devices_co.addItem("{} | {}".format(name, addr))
                # print("  {} - {}".format(addr, name))

            if len(self.nearby_devices) > 0:
                self.devices_co.setCurrentIndex(0)
                self.deviceSelected(0)

            # for port in self.ports:
            #     self.ports_co.addItem(port.description)

            self.searching_info_lbl.setText(
                "{} devices".format(len(self.nearby_devices)))
           

        except:
            print("Scanning error")
            self.searching_info_lbl.setText("Error")

        self.scan_btn.setEnabled(True)

    def scanDevices(self):
        th = threading.Thread(target=self.scanDevicesThread)
        th.start()

    def deviceSelected(self, value):
        if value > -1 and len(self.nearby_devices) > 0:
            self.device = self.nearby_devices[value]
           

    # def testSend(self):
        
    #     addr, name = self.device
    #     port = 1

        # sock = bluetooth.BluetoothSocket()
        # ok = False

        # try:
        #     sock.connect((addr,port))
        #     ok = True
        # except:
        #     print("Connection error")

        # if ok:
        #     sock.send("hello!!".encode())
        #     sock.close()

        # if not self.sc.is_connected:
        #     self.sc.address = addr
        #     self.sc.port = port
        #     self.sc.connect()


        # if self.sc.is_connected:
        #     self.sc.sendStr("holiii")

# def data(self):
#     return self.port.device, int(self.rate_le.text())


class BluetoothSerialMonitor(QWidget):

    def __init__(self, vertical = True, _bluetooth_socket = 0):
        super(BluetoothSerialMonitor,self).__init__()
        self.setWindowTitle("BluetoothSerialMonitor")
        if vertical:
            self.portScanner = DeviceScanner(False)
        else:
            self.portScanner = DeviceScanner(True)

        self.monitor = MonitorWidget()

        self.monitor.setEnabled(False)
        self.isConnected = False



        self.connect_button = QPushButton("Start", self)
        self.connect_button.clicked.connect(self.connectButtonPressed)

        # self.color_button = QPushButton("Set Color", self)
        # self.color_button.clicked.connect(self.color)

        if _bluetooth_socket == 0:
            self.socket = BluetoothSocketHelper()
        else:
            self.socket = _bluetooth_socket

        self.socket.on_msg_sent.add(self.monitor.logSent)
        self.socket.info_broadcaster.add(self.monitor.logSystem)
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

        self.port_input = QLineEdit()
        self.port_input.setFixedWidth(35)
        validator = QIntValidator()
        validator.setBottom(1)
        self.port_input.setValidator(validator)
        self.port_input.setAlignment(Qt.AlignCenter)
        self.port_input.setText("1")

        
        self.portAndConnectlo.addWidget(self.portScanner)
        self.portAndConnectlo.addWidget(self.port_input)
        self.portAndConnectlo.addWidget(self.connect_button)
        self.portAndConnectlo.addStretch()

        
        self.msgOptions = MonitorMsgOptions(self.socket.connection_succes_msg,self.socket.start_marker,self.socket.end_marker,False)
        self.msgOptions.welcome.line_edit.textChanged.connect(self.messageOptionChanged)
        self.msgOptions.start.line_edit.textChanged.connect(self.messageOptionChanged)
        self.msgOptions.end.line_edit.textChanged.connect(self.messageOptionChanged)
        self.msgOptions.line_adjustments_cb.setSelectedLineAdjustment(self.socket.line_adjustment)
        self.msgOptions.line_adjustments_cb.currentIndexChanged.connect(self.messageOptionChanged)
        self.msgOptions.lo.addStretch()
      



        
        # self.lo = QHBoxLayout(self)
        self.lo.addLayout(self.portAndConnectlo)
        self.lo.addWidget(self.msgOptions)
        # h_lo.addWidget(self.portScanner)
        # self.lo.addWidget(self.msgOptions)
        self.lo.addWidget(self.monitor)

        self.monitor.on_send_message.add(self.sendMessagePrint)
        self.monitor.on_send_message.add(self.socket.sendStr)
        self.socket.on_msg_received.add(self.monitor.log)

    # def color(self):
    #     color = QColorDialog.getColor()

    #     if color.isValid():
    #        self.serial.sendStr(f"R{color.red()},{color.green()}.{color.blue()}")
        

    def connectThread(self):
        self.connect_button.setEnabled(False)
        if self.isConnected:
            try:
                
                self.socket.disconnect()
            except: 
                print("Disconnect error")
            self.isConnected = False
        
        else:

            
            try:
                self.socket.socket = BluetoothSocket()
                address,name = self.portScanner.device
               
                self.socket.address = address
                
                self.socket.port = int(self.port_input.text())
                print(f"port is {self.socket.port}")

                if self.socket.address and self.socket.port:
                    if self.socket.connect():
                        self.isConnected = True
                
                   

                   

            except:
                print("connectThread Error")

        self.connect_button.setEnabled(True)
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

    
    def connectButtonPressed(self):
        thread  = threading.Thread(target=self.connectThread)
        thread.start()

    


    def test(self):
        pass

    def sendMessagePrint(self, msg):
        print("Sending " + msg)


    def messageOptionChanged(self, text):
        sender = self.sender()
        if sender == self.msgOptions.welcome.line_edit:
            self.socket.connection_succes_msg = text
        elif sender == self.msgOptions.start.line_edit:
            self.socket.start_marker = text
        elif sender == self.msgOptions.end.line_edit:
            self.socket.end_marker = text
        elif sender == self.msgOptions.line_adjustments_cb:
            # print( f"current index selected is {self.msgOptions.line_adjustments_cb.currentIndex()}")
            self.socket.line_adjustment = self.msgOptions.line_adjustments_cb.lineAdjustment()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = BluetoothSerialMonitor(vertical=True)
    w.show()
    sys.exit(app.exec_())
