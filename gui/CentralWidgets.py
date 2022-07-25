import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QObject, QThread
from ConnectionFields import ConnectionFields
from ChannelSelection import ChannelSelection
from ControlFields import ControlFields
from dispatcher import Dispatcher
__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'


# Constants
ABORT_CMD = 'az.{channel}P1=0.000\r'


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Objects 
        self.Thread = None
        self.Dispatcher = None
        self.dispatcher_ctrl = None
        self.route = None
        self.comms = None

        # Widgets
        # ->Connection Widget
        self.connection_wdg = ConnectionFields(self)
        
        # ->Channel Selector Widget
        self.channels_wdg  = ChannelSelection(self)

        # ->Control fields Widget
        self.control_wdg = ControlFields(self)


        # Init routines
        self.channels_wdg.setEnabled(False)
        self.control_wdg.setEnabled(False)

        # Signals and Slots
        self.connection_wdg.connect_signal.connect(self.connectUnlock)
        self.connection_wdg.disconnect_signal.connect(self.disconnectLock)
        self.control_wdg.start_signal.connect(self.runTest)
        self.control_wdg.abort_signal.connect(self.abortSequence)

        # Layout
        layout = QVBoxLayout()
        
        layout.addWidget(self.connection_wdg)
        layout.addWidget(self.channels_wdg)
        layout.addWidget(self.control_wdg)

        self.setLayout(layout)

    def disconnectLock(self):
        self.channels_wdg.setEnabled(False)
        self.control_wdg.setEnabled(False)

    def connectUnlock(self):
        self.channels_wdg.setEnabled(True)
        self.control_wdg.setEnabled(True)


    def runTest(self):
        # Create a thread
        self.Thread = QThread()
        

        # Create a Dispatcher
        # -> Get serial_comms 
        self.comms = self.connection_wdg.getComms()
        
        # -> Get Channel
        channel = int(self.channels_wdg.getChannel())*2

        # -> Get Route 
        self.route = self.control_wdg.getRoute()

        # -> Generate dispatcher ctrl
        self.dispatcher_ctrl = {'allowed':True}

        self.Dispatcher = Dispatcher(self.comms, channel, self.route, self.dispatcher_ctrl)

        # Assign worker to thread
        self.Dispatcher.moveToThread(self.Thread)

        # Connect signals
        self.Thread.started.connect(self.Dispatcher.run)
        self.Dispatcher.finished.connect(self.Thread.quit)
        self.Dispatcher.finished.connect(self.Dispatcher.deleteLater)
        self.Thread.finished.connect(self.Thread.deleteLater)
        

        # Start Dispatcher on thread
        self.Thread.start()

    def abortSequence(self):

        # Stop any running threads
        if self.Thread and self.Thread.isRunning():
            
            # Disable thread ability to send cmds to device
            self.dispatcher_ctrl['allowed'] = False
            
            # Set thread timer to zero
            self.route['time_step'] = 0.0

            # Wait for thread to end
            self.Thread.quit()
            self.Thread.wait()

            # Send stop commands to all channels
            self.abortCMD()

            # Clean before ending
            self.dispatcher_ctrl = None
            self.route = None
            
    def abortCMD(self):
        for i in range(1,5):
            channel = i*2
            self.comms.write(ABORT_CMD.format(channel=channel).encode('utf_8'))




if __name__ == '__main__':
    app = QApplication([])
    widget = CentralWidget()
    widget.show()
    sys.exit(app.exec_())