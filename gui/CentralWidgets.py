import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from ConnectionFields import ConnectionFields
from ChannelSelection import ChannelSelection
from ControlFields import ControlFields
__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        # Widgets
        # ->Connection Widget
        self.connection_wdg = ConnectionFields(self)
        
        # ->Channel Selector Widget
        self.channels_wdg  = ChannelSelection(self)

        # ->Control fields Widget
        self.control_wdg = ControlFields(self)


        # Layout
        layout = QVBoxLayout()
        
        layout.addWidget(self.connection_wdg)
        layout.addWidget(self.channels_wdg)
        layout.addWidget(self.control_wdg)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    widget = CentralWidget()
    widget.show()
    sys.exit(app.exec_())