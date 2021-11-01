from PyQt5 import QtWidgets, QtCore, QtGui

def hueGradient(x,y):
    g = QtGui.QLinearGradient(x,y)

    max_hue = 358
    for i in range(0,max_hue):
        g.setColorAt(float(i)/float(max_hue), QtGui.QColor.fromHsv(i,255,255))

    return g

class Widget(QtWidgets.QWidget):
    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        font = QtGui.QFont("Arial", 72)
        painter.setFont(font)
        rect = self.rect()
        # gradient = QtGui.QLinearGradient(rect.topLeft(), rect.topRight())
        # gradient.setColorAt(0, QtGui.QColor().fromHsv(0,255,255))
        # gradient.setColorAt(1, QtGui.QColor().fromHsv(120,255,255))
        gradient = hueGradient(rect.topLeft(), rect.topRight())
        pen = QtGui.QPen()
        pen.setBrush(QtGui.QBrush(gradient,QtGui.Qt.SolidPattern))
        painter.setPen(pen)
        painter.drawText(QtCore.QRectF(rect), "Hello world", QtGui.QTextOption(QtCore.Qt.AlignCenter))
        painter.drawRect(10,10,200,200)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec()