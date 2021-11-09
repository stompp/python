from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor, QWheelEvent, QTextCursor
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QColorDialog,\
                        QSlider, QStyleOptionSlider, QStyle,QComboBox,QTextEdit, QLineEdit, QCheckBox
import logging
from myutils import *


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



class MonitorMsgOptions(QWidget):
    def __init__(self, welcomeMessageText,messageStartText,messageEndText,vertical):
        super(MonitorMsgOptions, self).__init__()
        self.welcome = LabeledTextEdit("Expected ",welcomeMessageText,False)
        self.welcome.setMaximumWidth(120)
        self.start = LabeledTextEdit("Start",messageStartText,False)
        self.start.setMaximumWidth(80)
        self.end = LabeledTextEdit("End",messageEndText,False)
        self.end.setMaximumWidth(80)

        self.line_adjustments_cb  = LineAdjustmentComboBox()

        if vertical:
            self.lo = QVBoxLayout(self)
        else:
            self.lo = QHBoxLayout(self)
        
        self.lo.addWidget(self.welcome)
        self.lo.addWidget(self.start)
        self.lo.addWidget(self.end)
        self.lo.addWidget(self.line_adjustments_cb)

 

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



class MonitorWidget(QWidget):

    def __init__(self):
        super(MonitorWidget,self).__init__()

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

        self.send_lo = QHBoxLayout()
        self.send_lo.addWidget(self.send_le)
        self.send_lo.addWidget(self.send_btn)


        self.autoscroll_cb = QCheckBox("Autoscroll",self)
        self.timestamp_cb = QCheckBox("Timestamp",self)

        self.autoscroll_cb.setChecked(True)
        self.timestamp_cb.setChecked(True)

        self.autoscroll_cb.stateChanged.connect(self.autoScrollStateChanged)
        self.timestamp_cb.stateChanged.connect(self.timeStampStateChanged)
      

        self.options_h_lo = QHBoxLayout()
        self.options_h_lo.addWidget(self.autoscroll_cb)
        self.options_h_lo.addWidget(self.timestamp_cb)
        self.options_h_lo.addStretch()
          
        v_lo = QVBoxLayout(self)
        v_lo.addWidget(self.monitor_te)
        v_lo.addLayout(self.send_lo)
        v_lo.addLayout(self.options_h_lo)

        logging.getLogger().addHandler(self.monitor_te)
        
        # self.status_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().setLevel(logging.DEBUG)
        self.autoScrollStateChanged()
        self.timeStampStateChanged()

        
    def setEnabled(self, enabled):
       
        self.monitor_te.setEnabled(enabled)
        self.send_le.setEnabled(enabled)
        self.send_btn.setEnabled(enabled)
       
        # self.send_lo.children().(enabled)


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


class ColorPickerWidget(QColorDialog):
    def __init__(self, parent=None):
        super(ColorPickerWidget,self).__init__(parent)
        self.setOptions(self.options() | QColorDialog.DontUseNativeDialog)

        for children in self.findChildren(QWidget):
            classname = children.metaObject().className()
            if classname not in ("QColorPicker", "QColorLuminancePicker"):
                children.hide()



class ClickSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super(ClickSlider, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)    
    def mousePressEvent(self, event):
       
        if event.button() == Qt.LeftButton:
           

            opt = QStyleOptionSlider()
            self.initStyleOption(opt)
            sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
            # do nothing if clicked on handle
            if sr.contains(event.pos()):
                super(ClickSlider, self).mousePressEvent(event)
            # move handle and set value if clicked not on on handle
            else:

                val = self.pixelPosToRangeValue(event.pos())
                self.setValue(val)
        else:
            super(ClickSlider, self).mousePressEvent(event)
    

    def pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
     
        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                               sliderMax - sliderMin, opt.upsideDown)

