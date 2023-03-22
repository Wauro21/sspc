from PySide2 import QtGui
from PySide2.QtWidgets import QMainWindow
from gui.CentralWidgets import CentralWidget


class SSP(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)

        # objects

        # widgets
        self.SPD_Widget = CentralWidget(self)

        # init routines
        self.setWindowTitle('SSPC - Serial Set Point Controller')
        self.setCentralWidget(self.SPD_Widget)
        self.setWindowIcon(QtGui.QIcon('rsrcs/icon.png'))

        # signals and slots

        # layout
