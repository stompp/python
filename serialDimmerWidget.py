import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QColorDialog,\
                            QSlider, QStyleOptionSlider, QStyle

from serialWidgets import SerialMonitor
from serialhelper import SerialHelper
import sys
from myutils import *
from RGBDimmer import *

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
    def mousePressEvent(self, event):
        super(ClickSlider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

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

class TemperatureSlider(ClickSlider):
    def __init__(self, *args, **kwargs):
        super(TemperatureSlider, self).__init__(*args, **kwargs)        

        self.setRange(RGBDimmerController.MIN_TEMPERATURE,RGBDimmerController.MAX_TEMPERATURE)
        self.setMouseTracking(True)
        self.setSingleStep(100)   

class HueSlider(ClickSlider):
    def __init__(self, *args, **kwargs):
        super(HueSlider, self).__init__(*args, **kwargs)        

        self.setRange(RGBDimmerController.MIN_HUE,RGBDimmerController.MAX_HUE)
        self.setMouseTracking(True)
        self.setSingleStep(5)   

class BrightnessSlider(ClickSlider):
    def __init__(self, *args, **kwargs):
        super(BrightnessSlider, self).__init__(*args, **kwargs)        

        self.setRange(RGBDimmerController.MIN_BRIGHTNESS,RGBDimmerController.MAX_BRIGHTNESS)
        self.setMouseTracking(True)
        self.setSingleStep(5)  

class RGBDimmerWidget(QWidget):
    def __init__(self, rgbDimmer = 0):
        super(RGBDimmerWidget,self).__init__()

      
        # self.serial_monitor.serial = RGBDimmerSerial()

        if rgbDimmer == 0:
            self.dimmer = RGBDimmerController()
        else :
            self.dimmer = rgbDimmer

        self.on_btn = QPushButton("On",self)
        self.on_btn.clicked.connect(self.on_button)

        # self.color_btn = QPushButton("Set Color",self)
        # self.color_btn.clicked.connect(self.set_color)


        self.color_dialog = ColorPickerWidget()
        self.color_dialog.setCurrentColor(QColor(255,0,0))
        self.color_dialog.currentColorChanged.connect(self.colorSelected)
        # self.color_dialog.colorSelected.connect(lambda: print("Color Changed")) 
       

        self.temperature_slider = TemperatureSlider(Qt.Horizontal, self)
        self.temperature_slider.valueChanged[int].connect(self.set_temperature)

        self.hue_slider = HueSlider(Qt.Horizontal, self)
        self.hue_slider.valueChanged[int].connect(self.set_hue)

        self.brighness_slider = BrightnessSlider(Qt.Horizontal, self)
        self.brighness_slider.valueChanged[int].connect(self.set_brightness)


        left_column_lo = QVBoxLayout(self)

        left_column_lo.addWidget(self.on_btn)
        # left_column_lo.addWidget(self.color_btn)
        left_column_lo.addWidget(self.temperature_slider)
        left_column_lo.addWidget(self.hue_slider)
        left_column_lo.addWidget(self.brighness_slider)

        left_column_lo.addWidget(self.color_dialog)

    def on_button(self):
        self.dimmer.sendCommand(3)
    
    def set_temperature(self, value):
        b = self.color_dialog.currentColor().value()
        k = Kelvin2RGB(value,math.ceil(mapValue(b,0.0,255.0,Kelvin2RGB.MIN_BRIGHTNESS,Kelvin2RGB.MAX_BRIGHTNESS)))
        self.color_dialog.blockSignals(True)
        self.color_dialog.setCurrentColor(QColor(k.red,k.green,k.blue))
        self.color_dialog.blockSignals(False)
        self.dimmer.setTemperature(value)
  
    def set_hue(self, value):
        b = self.color_dialog.currentColor().value()
        c = QColor.fromHsv(value,255,b)
        self.color_dialog.blockSignals(True)
        self.color_dialog.setCurrentColor(c)
        self.color_dialog.blockSignals(False)
        self.dimmer.setHue(value)

    def set_brightness(self, value):
        c = self.color_dialog.currentColor()
        c.setHsv(c.hue(),c.saturation(),value)
        self.color_dialog.blockSignals(True)
        self.color_dialog.setCurrentColor(c)
        self.color_dialog.blockSignals(False)
        self.dimmer.setBrightness(value)

    # def set_color(self):
    #     # color_dialog = QColorDialog()
    #     self.color_dialog.show()
    #     # self.color_dialog.currentColorChanged.connect(self.colorSelected)
    #     # color = self.color_dialog.getColor()
    #     # color = QColorDialog.getColor()

    #     # if color.isValid():
    #     #     self.dimmer.setRGB(color.red(),color.green(),color.blue())

    def colorSelected(self,color):
        try:
            if color.isValid():
               
                self.dimmer.setRGB(color.red(),color.green(),color.blue())
                self.brighness_slider.blockSignals(True)
                self.hue_slider.blockSignals(True)
                self.brighness_slider.setValue(color.value())
                self.hue_slider.setValue(color.hue())
                self.brighness_slider.blockSignals(False)
                self.hue_slider.blockSignals(False)
        except:
            print("Error selecting color")





class DimmerSerialWidget(QWidget):

    def __init__(self, rgbDimmer = 0, serial = 0):
        super(DimmerSerialWidget,self).__init__()

        self.dimmerWidget = RGBDimmerWidget(rgbDimmer)
        self.dimmer = self.dimmerWidget.dimmer

        self.serial_monitor = SerialMonitor(True,serial)
        self.serial = self.serial_monitor.serial


        self.dimmerWidget.dimmer.senders.add(self.serial.sendStr)

        h_lo = QHBoxLayout(self)

        h_lo.addWidget(self.dimmerWidget)
        h_lo.addWidget(self.serial_monitor)

    def __del__(self):
        self.dimmer.senders.remove(self.serial.sendStr)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DimmerSerialWidget()
    w.show()    
    sys.exit(app.exec_())





