from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QWidget, QPushButton,QComboBox,QVBoxLayout,QHBoxLayout
from PyQt5.QtWidgets import QTextEdit,QGridLayout,QColorDialog, QScrollBar,QCheckBox
from PyQt5.QtGui import QIntValidator, QTextCursor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import sys
import serial
import serial.tools.list_ports
import logging
import threading

from datetime import datetime
from myutils import MessageBroadcaster, MethodsList
from serialhelper import SerialHelper

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

class LineAdjustmentComboBox(QComboBox):
    def __init__(self) :
        super(LineAdjustmentComboBox,self).__init__()
        self.line_adjustments = ["-", "NL","CR","CR & NL"]
     
        self.addItems(self.line_adjustments)

    def lineAdjustment(self):
        out = ""
        if self.currentText() == "NL":
            out = "\n"
        elif self.currentText() == "CR":
            out = "\r"
        elif self.currentText() == "CR & NL":
            out = "\r\n"
        
        return out

    def setSelectedLineAdjustment(self, txt):
        if txt in self.line_adjustments:
            self.setCurrentText(txt)
        elif txt == "\n":
            self.setCurrentText("NL")
        elif txt == "\r":
            self.setCurrentText("CR")
        elif txt == "\r\n":
            self.setCurrentText("CR & NL")
        else:
            self.setCurrentText("-")


class QLogTextEdit(logging.Handler,QTextEdit):
    def __init__(self, parent=None, auto_scroll = True, timestamp = True):
        QTextEdit.__init__(self,parent)
        logging.Handler.__init__(self)

        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setReadOnly(True)

        self.emit_lock = threading.Lock()


        self.timestamp_format = '[%I:%M:%S]'
        self.withAutoScroll(auto_scroll)
        self.withTimeStamp(timestamp)
        


    def emit(self, record):
       
        with self.emit_lock:
            QtCore.QMetaObject.invokeMethod(self, 
                "append",  
                QtCore.Qt.QueuedConnection,
                QtCore.Q_ARG(str, self.format(record)))

            
            QtCore.QMetaObject.invokeMethod(self, 
                "doAutoScroll",
                QtCore.Qt.QueuedConnection)

    def withAutoScroll(self,autoscroll = True):
        self.auto_scroll = autoscroll
        if self.auto_scroll:
            self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().maximum())
        elif self.verticalScrollBar().maximum() >= 1:
             self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().maximum() - 1)
    def withTimeStamp(self, prependTimeStamp = True):
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        # self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
        # if prependTimeStamp:
        #     logging.basicConfig(format='%(asctime)s %(message)s', datefmt=self.timestamp_format)
        # else:
        #     logging.basicConfig(format='%(message)s')

        if prependTimeStamp:
            self.setFormatter(logging.Formatter('%(asctime)s  %(message)s', datefmt=self.timestamp_format))
        else:
            self.setFormatter(logging.Formatter('%(message)s'))


    def format(self, record):
        # if record.levelno == logging.INFO:
        #     bgcolor = WHITE
        #     fgcolor = BLACK
        # elif record.levelno == logging.WARNING:
        #     bgcolor = YELLOW
        #     fgcolor = BLACK
        # elif record.levelno == logging.ERROR:
        #     bgcolor = ORANGE
        #     fgcolor = BLACK
        # elif record.levelno == logging.CRITICAL:
        #     bgcolor = RED
        #     fgcolor = BLACK
        # else:
        #     bgcolor = BLACK
        #     fgcolor = WHITE

        # self.setTextBackgroundColor(bgcolor)
        # self.setTextColor(fgcolor)
        # self.setFont(DEFAULT_FONT)
        record = logging.Handler.format(self, record)
        return record

    @QtCore.pyqtSlot()
    def doAutoScroll(self):
        if self.auto_scroll:
            self.moveCursor(QTextCursor.End)
        # self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().maximum())


class MonitorWidget2(QWidget):

    def __init__(self):
        super(MonitorWidget2,self).__init__()

        # self.prepend_timestamp = True
        self.sent_msg_prepend = ">>> "
        self.sys_msg_prepend = "### "

        self.on_send_message = MessageBroadcaster()
        # self.send_msg_methods = list()

        self.sent_msgs = list()
        self.sent_msgs_index = -1


        self.resize(200,400)

        self.monitor_te = QLogTextEdit(self)
   
      
        self.send_le = QLineEdit(self)
      
        self.send_btn = QPushButton("Send", self)
        self.send_btn.clicked.connect(self.sendInput)

        send_lo = QHBoxLayout()
        send_lo.addWidget(self.send_le)
        send_lo.addWidget(self.send_btn)


        self.autoscroll_cb = QCheckBox("Autoscroll",self)
        self.timestamp_cb = QCheckBox("Timestamp",self)

        self.autoscroll_cb.setChecked(True)
        self.timestamp_cb.setChecked(True)

        self.autoscroll_cb.stateChanged.connect(self.autoScrollStateChanged)
        self.timestamp_cb.stateChanged.connect(self.timeStampStateChanged)
      

        options_h_lo = QHBoxLayout()
        options_h_lo.addWidget(self.autoscroll_cb)
        options_h_lo.addWidget(self.timestamp_cb)
        options_h_lo.addStretch()
          
        v_lo = QVBoxLayout(self)
        v_lo.addWidget(self.monitor_te)
        v_lo.addLayout(send_lo)
        v_lo.addLayout(options_h_lo)

        logging.getLogger().addHandler(self.monitor_te)
        # self.status_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().setLevel(logging.DEBUG)
        self.autoScrollStateChanged()
        self.timeStampStateChanged()

        


    def autoScrollStateChanged(self):
        self.monitor_te.withAutoScroll(self.autoscroll_cb.isChecked())
    def timeStampStateChanged(self):
        self.monitor_te.withTimeStamp(self.timestamp_cb.isChecked())

    # def ts(self):
    #     if self.timestamp_cb.isChecked():
    #         now = datetime.now()
    #         return now.strftime("[%H:%M:%S] ")
    #     return ""


    def log(self, msg):
        # getattr(self.logger, "debug")("Hola " + msg)
        logging.debug(msg)
      
        

    def logSent(self,msg):       
        self.log(self.sent_msg_prepend + msg)

    def logSystem(self, msg):
        if(len(msg)):
            self.log(self.sys_msg_prepend + msg)
        else:
            self.logSystem("Empty")

    def sendInput(self):

        t = self.send_le.text()
        if len(t) > 0:
            # o = t + self.lineAdjustment()
            self.on_send_message.broadcast(t)
            # for m in self.send_msg_methods:
            #     m(t)

          
            if len(self.sent_msgs) == 0:
                self.sent_msgs.append(t)
            elif len(self.sent_msgs) > 0:
                if self.sent_msgs[len(self.sent_msgs) -1] != t:
                    self.sent_msgs.append(t)
            
            # self.logSent(t)
            self.sent_msgs_index = -1
            self.send_le.setText("")

    def keyPressEvent(self, event) :
        if (self.send_btn.hasFocus() or self.send_le.hasFocus()) and (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) :
           
            self.sendInput()

        if(self.send_btn.hasFocus() or self.send_le.hasFocus()):

         
            if event.key() == Qt.Key_Up:
                
                if self.sent_msgs_index == -1:
                    if len(self.sent_msgs) > 0:
                        self.sent_msgs_index = len(self.sent_msgs) -1
                        self.send_le.setText(self.sent_msgs[self.sent_msgs_index])
                elif self.sent_msgs_index > 0:
                    if len(self.sent_msgs) > 0:
                        if(self.sent_msgs_index > 0):
                            self.sent_msgs_index -= 1
                            self.send_le.setText(self.sent_msgs[self.sent_msgs_index])
            elif event.key() == Qt.Key_Down:

                if self.sent_msgs_index == -1:
                    self.send_le.setText("")
                elif self.sent_msgs_index < len(self.sent_msgs) -1:
                    self.sent_msgs_index +=1
                    self.send_le.setText(self.sent_msgs[self.sent_msgs_index])
                else :
                    self.sent_msgs_index = -1
                    self.send_le.setText("")



                    





        # return super().keyPressEvent(event)



    
class LabeledTextEdit(QWidget):
    def __init__(self,labelText,lineEditText,vertical = False):
        super(LabeledTextEdit, self).__init__()

        if vertical :
            self.lo = QVBoxLayout(self)
        else:
            self.lo = QHBoxLayout(self)

        self.label = QLabel(self)
        self.label.setText(labelText)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(lineEditText)

        self.lo.addWidget(self.label)
        self.lo.addWidget(self.line_edit)  

class SerialMonitorMsgOptions(QWidget):
    def __init__(self, welcomeMessageText,messageStartText,messageEndText,vertical):
        super(SerialMonitorMsgOptions, self).__init__()
        self.welcome = LabeledTextEdit("Expected ",welcomeMessageText,False)
        self.welcome.setMaximumWidth(120)
        self.start = LabeledTextEdit("Start",messageStartText,False)
        self.start.setMaximumWidth(80)
        self.end = LabeledTextEdit("End",messageEndText,False)
        self.end.setMaximumWidth(80)

        self.line_adjustments_cb  = LineAdjustmentComboBox()

        # self.line_adjustments = ["-", "NL","CR","CR & NL"]
        # self.line_adjustments_cb = QComboBox(self)
        # self.line_adjustments_cb.addItems(self.line_adjustments)

        if vertical:
            self.lo = QVBoxLayout(self)
        else:
            self.lo = QHBoxLayout(self)
        
        self.lo.addWidget(self.welcome)
        self.lo.addWidget(self.start)
        self.lo.addWidget(self.end)
        self.lo.addWidget(self.line_adjustments_cb)

    # def lineAdjustment(self):
    #     out = ""
    #     if self.line_adjustments_cb.currentText() == "NL":
    #         out = "\n"
    #     elif self.line_adjustments_cb.currentText() == "CR":
    #         out = "\r"
    #     elif self.line_adjustments_cb.currentText() == "CR & NL":
    #         out = "\r\n"
        
    #     return out

    # def setSelectedLineAdjustment(self, txt):
    #     if txt == "\n":
    #         self.line_adjustments_cb.setCurrentText("NL")
    #     elif txt == "\r":
    #         self.line_adjustments_cb.setCurrentText("CR")
    #     elif txt == "\r\n":
    #         self.line_adjustments_cb.setCurrentText("CR & NL")
    #     else:
    #         self.line_adjustments_cb.setCurrentText("-")

class SerialMonitor(QWidget):

    def __init__(self, vertical = True, _serial = 0):
        super(SerialMonitor,self).__init__()
        self.setWindowTitle("Monitor")
        if vertical:
            self.portScanner = PortScannerWidget(False)
        else:
            self.portScanner = PortScannerWidget(True)

        self.monitor = MonitorWidget2()

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

        
        self.msgOptions = SerialMonitorMsgOptions(self.serial.connection_succes_msg,self.serial.start_marker,self.serial.end_marker,False)
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

    # def lineAdjustmentChanged(self):
    #     self.serial.line_adjustment = self.msgOptions.line_adjustments_cb.lineAdjustment()

    





if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SerialMonitor()
    w.show()    
    sys.exit(app.exec_())




    
