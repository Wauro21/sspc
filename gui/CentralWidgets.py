import sys 
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide2.QtCore import QObject, QThread
from gui.ConnectionFields import ConnectionFields
from gui.ChannelSelection import ChannelSelection
from gui.ControlFields import ControlFields
from core.Dispatcher import Dispatcher
from gui.MessageBox import InformationBox
from gui.ManualWidget import ManualControl
import os

__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'

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
        self.control_wdg.stop_signal.connect(self.stopSequence)
        self.channels_wdg.manual_signal.connect(self.manualRoutine)

        # Layout
        layout = QVBoxLayout()
        
        layout.addWidget(self.connection_wdg)
        layout.addWidget(self.channels_wdg)
        layout.addWidget(self.control_wdg)
        layout.addStretch()

        self.setLayout(layout)

    def disconnectLock(self):
        self.comms = None
        self.channels_wdg.setEnabled(False)
        self.control_wdg.setEnabled(False)

    def connectUnlock(self):
        self.comms = self.connection_wdg.getComms()
        self.channels_wdg.setEnabled(True)
        self.control_wdg.setEnabled(True)


    def runTest(self):
        # Lock Control fields during Thread operation
        self.lockForRun()

        # Reset progress bar
        self.resetBar()

        # Create a thread
        self.Thread = QThread()
        

        # Create a Dispatcher
        
        # -> Get Channel
        channel = int(self.channels_wdg.getChannel())*2

        # -> Get Route 
        self.route = self.control_wdg.getRoute()

        # -> Generate dispatcher ctrl
        self.dispatcher_ctrl = {'abort':False}
        self.dispatcher_ctrl['stop'] = False

        self.Dispatcher = Dispatcher(self.comms, channel, self.route, self.dispatcher_ctrl)

        # Assign worker to thread
        self.Dispatcher.moveToThread(self.Thread)

        # Connect signals
        self.Thread.started.connect(self.Dispatcher.run)
        self.Dispatcher.finished.connect(self.Thread.quit)
        self.Dispatcher.finished.connect(self.Dispatcher.deleteLater)
        self.Thread.finished.connect(self.Thread.deleteLater)
        self.Thread.finished.connect(self.ThreadEnd)
        self.Dispatcher.progress.connect(self.updateBar)
        # Start Dispatcher on thread
        self.Thread.start()    
    
    def abortSequence(self):
        # Stop any running threads
        if self.Thread and self.Thread.isRunning():
            
            # Disable thread ability to send cmds to device
            self.dispatcher_ctrl['abort'] = True

            # Wait for thread to end
            self.Thread.quit()
            self.Thread.wait()

            # Clean before ending
            self.dispatcher_ctrl = None
            self.route = None
        
        else:
            # No thread is running
            self.abortRoutine()

            
        # Clear Thread
        self.Thread = None

        msg = InformationBox('Abort sequence ended. All channels were set to zero')
        msg.exec_()

        # Restore progress bar
        self.resetBar()
    
    def lockForRun(self):
        # Lock channel 
        self.channels_wdg.lockChannels()

        # Lock fields
        self.control_wdg.lockFields()


    def stopSequence(self):
        if self.Thread and self.Thread.isRunning():
            
            # Disable thread ability to send cmds to device
            self.dispatcher_ctrl['stop'] = True

            # Wait for thread to end
            self.Thread.quit()
            self.Thread.wait()

            # Clean before ending
            self.dispatcher_ctrl = None
            self.route = None
        
        # Clear Thread
        self.Thread = None

        # Reset progress bar
        self.resetBar()

    def abortRoutine(self):
        # Set all channels to zero
        for i in range(1,5):
            CMD = ABORT_CMD.format(channel=2*i).encode('utf_8')
            self.comms.write(CMD)

    def ThreadEnd(self):
        # Unlock fields
        self.lockForRun()
        self.control_wdg.stopHandler()

    def manualRoutine(self):
        # Generate Window
        channel = int(self.channels_wdg.getChannel())*2
        manual_window = ManualControl(self.comms, channel, self)

        # Lock automatic control fields 
        self.lockForRun()

        # Signals 
        manual_window.finished.connect(self.lockForRun)

        # Start Window
        manual_window.exec_()

    def updateBar(self, val):
        self.control_wdg.progressHandler(val)


    def resetBar(self):
        self.control_wdg.resetBar()


if __name__ == '__main__':
    app = QApplication([])
    if os.name == 'nt':
        app.setStyle('Fusion')
    widget = CentralWidget()
    widget.show()
    sys.exit(app.exec_())