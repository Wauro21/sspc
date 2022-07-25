# Selection of the channel of operation

import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QApplication, QFormLayout
from PyQt5.QtCore import Qt

__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'

class ChannelSelection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.channels = QComboBox()

        # Init routines
        self.channels.addItems(['1','2','3','4'])

        # Layout 
        layout = QFormLayout()
        layout.addRow('Select Channel: \t', self.channels)

        self.setLayout(layout)

    def getChannel(self):
        return self.channels.currentText()

if __name__ == '__main__':
    app = QApplication([])
    widget = ChannelSelection()
    widget.show()
    sys.exit(app.exec_())