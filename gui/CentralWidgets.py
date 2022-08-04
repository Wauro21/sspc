import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QObject, QThread
from ConnectionFields import ConnectionFields
from ChannelSelection import ChannelSelection
from ControlFields import ControlFields
from Dispatcher import Dispatcher
from MessageBox import InformationBox
__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'



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
        print("STARTING A THREAD")
        # Lock Control fields during Thread operation
        self.lockForRun()

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
        self.Thread.finished.connect(self.lockForRun)
        #self.Thread.finished.connect(self.control_wdg.StartStopHandler)
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

        msg = InformationBox('Abort sequence ended. All channels were set to zero')
        msg.exec_()


    
    def lockForRun(self):
        # Lock channel 
        self.channels_wdg.setEnabled(not self.channels_wdg.isEnabled())

        # Lock fields
        self.control_wdg.lockFields()


    def stopSequence(self):
        if self.Thread and self.Thread.isRunning():
            
            # Disable thread ability to send cmds to device
            self.dispatcher_ctrl['stop'] = True

            # Wait for thread to end
            self.Thread.quit()
            self.Thread.wait()
            print('THREAD ENDED')

            # Clean before ending
            self.dispatcher_ctrl = None
            self.route = None




if __name__ == '__main__':
    app = QApplication([])
    widget = CentralWidget()
    widget.show()
    sys.exit(app.exec_())