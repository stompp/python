

import random
import logging
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

WHITE, BLACK, YELLOW, ORANGE, RED = QtGui.QColor("white"), QtGui.QColor("black"), QtGui.QColor("yellow"), QtGui.QColor("orange"), QtGui.QColor("red")
DEFAULT_FONT = QtGui.QFont()

class QHandler(logging.Handler, QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        QtWidgets.QTextEdit.__init__(self, parent)
        logging.Handler.__init__(self)

        self.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.setReadOnly(True)

        self.emit_lock = threading.Lock()

    def emit(self, record):
        with self.emit_lock:
            QtCore.QMetaObject.invokeMethod(self, 
                "append",  
                QtCore.Qt.QueuedConnection,
                QtCore.Q_ARG(str, self.format(record)))

            QtCore.QMetaObject.invokeMethod(self, 
                "autoScroll",
                QtCore.Qt.QueuedConnection)

    def format(self, record):
        if record.levelno == logging.INFO:
            bgcolor = WHITE
            fgcolor = BLACK
        elif record.levelno == logging.WARNING:
            bgcolor = YELLOW
            fgcolor = BLACK
        elif record.levelno == logging.ERROR:
            bgcolor = ORANGE
            fgcolor = BLACK
        elif record.levelno == logging.CRITICAL:
            bgcolor = RED
            fgcolor = BLACK
        else:
            bgcolor = BLACK
            fgcolor = WHITE

        self.setTextBackgroundColor(bgcolor)
        self.setTextColor(fgcolor)
        self.setFont(DEFAULT_FONT)
        record = logging.Handler.format(self, record)
        return record

    @QtCore.pyqtSlot()
    def autoScroll(self):
        self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().maximum())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.status_handler = QHandler()
        self.setCentralWidget(self.status_handler)

        logging.getLogger().addHandler(self.status_handler)
        self.status_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().setLevel(logging.DEBUG)
    
        timer = QtCore.QTimer(self, interval=1000, timeout=self.on_timeout)
        timer.start()

    def on_timeout(self):
        logging.info('From Gui Thread {}'.format(QtCore.QDateTime.currentDateTime().toString()))


class Subprocess_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('Subprocess Thread Created')

    def run(self):
        while True:
            t = random.choice(["info", "warning", "error", "critical"])
            msg = "Type: {}, thread: {}".format(t, threading.currentThread())
            getattr(self.logger, t)("Hola " + msg)
            QtCore.QThread.sleep(1)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle('Fusion')
    w = MainWindow()
    w.show()
    th = Subprocess_Thread()
    th.daemon = True
    th.start()
    sys.exit(app.exec_())
