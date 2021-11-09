from datetime import time
import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QWheelEvent
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QColorDialog,\
                            QSlider, QStyleOptionSlider, QStyle
import bluetooth

from serialWidgets import SerialMonitor

import sys
from myutils import *
from RGBDimmer import *
from pyqt5Utils import *
import time


DIMMER_WIDGET_STYLE = """
    QSlider::handle:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                    border: 1px solid #5c5c5c;
                    width: 10px;
                    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
                    border-radius: 3px;
                    }
     QSlider::handle:vertical {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                    border: 1px solid #5c5c5c;
                    height: 10px;
                    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
                    border-radius: 3px;
                    }
    QSlider::groove:horizontal {
                    border: 1px solid #999999;
                    /* height: 8px; */                         
                    margin: 2px 0;
                    }
    QSlider::groove:vertical {
                    border: 1px solid #999999;
                    /* height: 8px; */ 
                    margin: 2px 0;
                        }
                        """

class TemperatureSlider(ClickSlider):
    WHEEL_INC = 100
    STYLE = """         
               TemperatureSlider::groove:horizontal {
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0.000 #ff3800
                                    stop: 0.045 #ff6d00
                                    stop: 0.091 #ff8a12
                                    stop: 0.136 #ffa148
                                    stop: 0.182 #ffb46b
                                    stop: 0.227 #ffc489
                                    stop: 0.273 #ffd1a3
                                    stop: 0.318 #ffdbba
                                    stop: 0.364 #ffe4ce
                                    stop: 0.409 #ffece0
                                    stop: 0.455 #fff3ef
                                    stop: 0.500 #fff9fd
                                    stop: 0.545 #f5f3ff
                                    stop: 0.591 #ebeeff
                                    stop: 0.636 #e3e9ff
                                    stop: 0.682 #dce5ff
                                    stop: 0.727 #d6e1ff
                                    stop: 0.773 #d0deff
                                    stop: 0.818 #cfdaff
                                    stop: 0.864 #ccd8ff
                                    stop: 0.909 #c8d5ff
                                    stop: 0.955 #c5d3ff
                                    stop: 1.000 #c3d1ff);
                }
                TemperatureSlider::groove:vertical {
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0.000 #ff3800
                                    stop: 0.045 #ff6d00
                                    stop: 0.091 #ff8a12
                                    stop: 0.136 #ffa148
                                    stop: 0.182 #ffb46b
                                    stop: 0.227 #ffc489
                                    stop: 0.273 #ffd1a3
                                    stop: 0.318 #ffdbba
                                    stop: 0.364 #ffe4ce
                                    stop: 0.409 #ffece0
                                    stop: 0.455 #fff3ef
                                    stop: 0.500 #fff9fd
                                    stop: 0.545 #f5f3ff
                                    stop: 0.591 #ebeeff
                                    stop: 0.636 #e3e9ff
                                    stop: 0.682 #dce5ff
                                    stop: 0.727 #d6e1ff
                                    stop: 0.773 #d0deff
                                    stop: 0.818 #cfdaff
                                    stop: 0.864 #ccd8ff
                                    stop: 0.909 #c8d5ff
                                    stop: 0.955 #c5d3ff
                                    stop: 1.000 #c3d1ff);
                }
            """
    def __init__(self, *args, **kwargs):
        super(TemperatureSlider, self).__init__(*args, **kwargs)        

        self.setRange(RGBDimmerController.MIN_TEMPERATURE,RGBDimmerController.MAX_TEMPERATURE)
         
        self.setStyleSheet(self.STYLE)
        
    def wheelEvent(self, event):
        # print(f"delta is {event.angleDelta()}")
        if event.angleDelta().y()> 0:
            # print("positive")
            self.setValue(self.value()+self.WHEEL_INC)
        else:
            # print("negative")
            self.setValue(self.value()-self.WHEEL_INC)
        # print(f"delta is {event.angleDelta()}")

class HueSlider(ClickSlider):
    STYLE = """         
               HueSlider::groove:horizontal {
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 red, 
                                    stop: 0.17 #ff0,
                                    stop: 0.33 lime,
                                    stop: 0.5 cyan,
                                    stop: 0.66 blue
                                    stop: 0.83 #f0f
                                    stop: 1 red);
                }
                HueSlider::groove:vertical {       
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 red, 
                                    stop: 0.17 #ff0,
                                    stop: 0.33 lime,
                                    stop: 0.5 cyan,
                                    stop: 0.66 blue
                                    stop: 0.83 #f0f
                                    stop: 1 red);
                }
            """
    def __init__(self, *args, **kwargs):
        super(HueSlider, self).__init__(*args, **kwargs)        

        self.setRange(RGBDimmerController.MIN_HUE,RGBDimmerController.MAX_HUE)
        self.setStyleSheet(self.STYLE)
       

class BrightnessSlider(ClickSlider):
    STYLE_TEMPLATE = """BrightnessSlider::groove:horizontal {{
                            background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                stop: 0 black,                                
                                stop: 1 "{0}");
                        }}
                        BrightnessSlider::groove:vertical {{
                            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 black,                                
                                stop: 1 "{0}");
                        }}
                        """
    
    def __init__(self, *args, **kwargs):
       
        super(BrightnessSlider, self).__init__(*args, **kwargs)        

        self.setRange(RGBDimmerController.MIN_BRIGHTNESS,RGBDimmerController.MAX_BRIGHTNESS)
        self.set_color("white")
     

    def set_color(self,hexrgb):
     
        self.setStyleSheet(self.STYLE_TEMPLATE.format(hexrgb))


class SaturationSlider(ClickSlider):
    STYLE_TEMPLATE = """SaturationSlider::groove:horizontal {{
                            background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                stop: 0 white,                                
                                stop: 1 "{0}");
                        }}
                        SaturationSlider::groove:vertical {{
                            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 white,                                
                                stop: 1 "{0}");
                        }}
                        """
    
    def __init__(self, *args, **kwargs):
        super(SaturationSlider, self).__init__(*args, **kwargs)        

        self.setRange(RGBDimmerController.MIN_SATURATION,RGBDimmerController.MAX_SATURATION)
        self.set_color("white")
     

    def set_color(self,hexrgb):
     
        self.setStyleSheet(self.STYLE_TEMPLATE.format(hexrgb))



class RGBDimmerWidget(QWidget):

    def __init__(self, rgbDimmer = 0):
        super(RGBDimmerWidget,self).__init__()

        if rgbDimmer == 0:
            self.dimmer = RGBDimmerController()
        else :
            self.dimmer = rgbDimmer

        self.random_test_thread = LoopThreadHelper(self.random_program)

        self.random_test_btn = QPushButton("Random Test",self)
        self.random_test_btn.clicked.connect(self.start_stop_random_program)
        
        self.on_btn = QPushButton("On",self)
        self.on_btn.clicked.connect(self.on_button)

     
        self.temperature_slider = TemperatureSlider(Qt.Horizontal, self)
        self.temperature_slider.valueChanged[int].connect(self.set_temperature)
        self.temperature_slider.valueChanged[int].connect(self.dimmer.setTemperature)

        self.hue_slider = HueSlider(Qt.Horizontal, self)
        self.hue_slider.valueChanged[int].connect(self.set_hue)
        self.hue_slider.valueChanged[int].connect(self.dimmer.setHue)

        self.brighness_slider = BrightnessSlider(Qt.Horizontal, self)
        self.brighness_slider.valueChanged[int].connect(self.set_brightness)
        self.brighness_slider.valueChanged[int].connect(self.dimmer.setBrightness)

        self.sliders_lo = QVBoxLayout()
        self.sliders_lo.addWidget(self.temperature_slider)
        self.sliders_lo.addWidget(self.hue_slider)
        self.sliders_lo.addWidget(self.brighness_slider)

     

        # left_column_lo.addWidget(self.temperature_slider)
        # left_column_lo.addWidget(self.hue_slider)
        # left_column_lo.addWidget(self.brighness_slider)

        self.color_picker = ColorPickerWidget()      
        self.color_picker.currentColorChanged.connect(self.set_color)

        left_column_lo = QVBoxLayout(self)
        left_column_lo.addWidget(self.random_test_btn)
        left_column_lo.addWidget(self.on_btn)
        left_column_lo.addLayout(self.sliders_lo)
        left_column_lo.addWidget(self.color_picker)

        c = QColor(0,255,0)
        self.color_picker.setCurrentColor(c)
        # self.set_color(c)

        self.setFixedWidth(int(self.color_picker.width()/2))

    def on_button(self):
        self.dimmer.sendCommand(3)
    
    def set_temperature(self, value):
        b = self.color_picker.currentColor().value()
        k = Kelvin2RGB(value,math.ceil(mapValue(b,0.0,255.0,Kelvin2RGB.MIN_BRIGHTNESS,Kelvin2RGB.MAX_BRIGHTNESS)))
        self.color_picker.blockSignals(True)
        self.color_picker.setCurrentColor(QColor(k.red,k.green,k.blue))
        self.color_picker.blockSignals(False)
        # self.dimmer.setTemperature(value)
        self.brighness_slider.set_color(rgb_to_hex((k.red,k.green,k.blue),True))
  
    def set_hue(self, value):
        b = self.color_picker.currentColor().value()
        c = QColor.fromHsv(value,255,b)
        self.brighness_slider.set_color(rgb_to_hex((c.red(),c.green(),c.blue()),True))
        self.color_picker.blockSignals(True)
        self.color_picker.setCurrentColor(c)
        self.color_picker.blockSignals(False)

        # self.dimmer.setHue(value)

    def set_brightness(self, value):
      
        if value > 0:
            c = self.color_picker.currentColor()
            c.setHsv(c.hue(),c.saturation(),value)
            self.color_picker.blockSignals(True)
            self.color_picker.setCurrentColor(c)
            self.color_picker.blockSignals(False)
        # self.dimmer.setBrightness(value)


    def set_color(self,color):
        try:
            if color.isValid():
               
                self.dimmer.setRGB(color.red(),color.green(),color.blue())
                
                self.brighness_slider.blockSignals(True)
                self.hue_slider.blockSignals(True)

                self.brighness_slider.setValue(color.value())
               
                if color.hue() > -1 :
                    self.hue_slider.setValue(color.hue())
                    self.brighness_slider.set_color(rgb_to_hex((color.red(),color.green(),color.blue()),True))

                self.brighness_slider.blockSignals(False)
                self.hue_slider.blockSignals(False)
        except:
            print("Error selecting color")

    def start_stop_random_program(self):
        if self.random_test_thread.active == True:
            self.random_test_thread.stop()
            print("random test stopped")
        else:
            self.random_test_thread.start()
            print("random test started")

    def random_program(self):
       
        self.dimmer.setRandomTone()
        time.sleep(2)





import bluetoothWidgets
class DimmerSerialWidget(QWidget):

    def __init__(self, rgbDimmer = 0, serial = 0):
        super(DimmerSerialWidget,self).__init__()

        h_lo = QHBoxLayout(self)
       

        self.dimmerWidget = RGBDimmerWidget(rgbDimmer)
        self.dimmer = self.dimmerWidget.dimmer

      

        
        h_lo.addWidget(self.dimmerWidget)

        self.serial_monitor = SerialMonitor(True,serial)
        # self.serial = self.serial_monitor.serial
        self.dimmerWidget.dimmer.senders.add(self.serial_monitor.serial.sendStr)
        h_lo.addWidget(self.serial_monitor)
        
        self.bluetooth_monitor = bluetoothWidgets.BluetoothSerialMonitor()
        self.dimmerWidget.dimmer.senders.add(self.bluetooth_monitor.socket.sendStr)
        h_lo.addWidget(self.bluetooth_monitor)

        self.setStyleSheet(DIMMER_WIDGET_STYLE)

        

    def __del__(self):
        self.dimmer.senders.remove(self.serial.sendStr)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DimmerSerialWidget()
    w.show()    
    sys.exit(app.exec_())





