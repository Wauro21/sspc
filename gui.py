# Simple GUI for the controller

import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QFormLayout, QHBoxLayout, QComboBox, QDoubleSpinBox, QMenu, QPushButton, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import serial
from serial_comms import abortSequence
# Constants for operation
LOWEST_SP = 0.000
HIGHEST_SP = 999.999
STEP_INCREMENT = 0.001
USE_DECIMALS = 3
SP_UNITS = '\tsl/min'

__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'

class CentralWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.connection_wdg = ConnectionWidget(self)
        self.control_wdg = ControlFields(self)
        central_layout = QVBoxLayout()
        # Bottom buttons
        self.verify_btn = QPushButton('Verify')
        self.start_stop_btn = QPushButton('Start')
        self.abort_btn = QPushButton('ABORT')
        self.abort_btn.setStyleSheet('background-color : red; font-weight : bold')
        # Disable buttons at start
        self.disablesButtons()

        # Botton intermediate layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.verify_btn)
        btn_layout.addWidget(self.start_stop_btn)
        btn_layout.addWidget(self.abort_btn)



        # Connect Signals and slots
        self.connection_wdg.connect_signal.connect(self.control_wdg.unlock)
        self.connection_wdg.disconnect_signal.connect(self.control_wdg.lock)
        self.connection_wdg.connect_signal.connect(self.enableButtons)
        self.connection_wdg.disconnect_signal.connect(self.disablesButtons)
        self.verify_btn.clicked.connect(self.validate)
        self.abort_btn.clicked.connect(lambda: abortSequence(self.connection_wdg.serial_comms))
        # Add to layout
        central_layout.addWidget(self.connection_wdg)
        central_layout.addWidget(self.control_wdg)
        central_layout.addLayout(btn_layout)
        
        
        self.setLayout(central_layout)


    def disablesButtons(self):
        buttons = [self.verify_btn, self.start_stop_btn, self.abort_btn]
        for button in buttons:
            button.setEnabled(False)
    def enableButtons(self):
        buttons = [self.verify_btn, self.abort_btn]
        for button in buttons:
            button.setEnabled(True)

    def validate(self):
        # Get data from widget
        to_validate = {
            'initial':'',
            'final':'',
            'progress':'',
            'p_val':''
        }
        self.control_wdg.getValues(to_validate)
        print(to_validate)
        # Validation steps
        if to_validate['progress'] == 'Step':
            step_size = to_validate['p_val']
            if not(step_size > 0):
                print("NOT VALID STEP - TO BE IMPLEMENTED")

            if (to_validate['initial'] < to_validate['final']):
                n_steps = (to_validate['final'] - to_validate['initial'])/step_size
                print(n_steps)

class ConnectionWidget(QWidget):
    connect_signal = QtCore.pyqtSignal()
    disconnect_signal = QtCore.pyqtSignal()

    def __init__(self,parent =None):
        super().__init__(parent)

        # Connection Options for the device
        self.serial_comms = None
        self.connect_btn = QPushButton('Connect')
        self.connect_btn.clicked.connect(self.handleConnection)
        self.status_label = QLabel('Connection status: {}'.format('Not Connected'))
        self.status_label.setAlignment(Qt.AlignCenter)
        layout = QHBoxLayout()
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    # If not connected: 
    #                   1) Try/except connection
    #                   2) If sucessfull emit signal
    # If connected:
    #                   1) Try/except disconnect
    #                   2) if sucessfull emit signal

    def handleConnection(self):
        if self.serial_comms:
            # Object is not null, disconnect routine
            try:
                self.serial_comms.close()
                self.serial_comms = None
                self.disconnect_signal.emit()
                text_val = 'Connect'
                text_status = 'Not Connected'
            except:
                raise Exception('Connection could not be ended.')
        
        else:
            # Object is null, connection routine
            try:
                self.serial_comms = serial.Serial('/dev/ttyUSB0')
                self.connect_signal.emit()
                text_val = 'Disconnect'
                text_status = 'Connected'
            except:
                raise Exception('Connection could not be made')
        self.connect_btn.setText(text_val)
        self.status_label.setText('Connection Status: {}'.format(text_status))     
        


class ControlFields(QWidget):
    # Fields to operate
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Connect lock
        self.locked = None

        # Fields 
        validator = QDoubleValidator(LOWEST_SP, HIGHEST_SP, 3,  notation=QDoubleValidator.StandardNotation)
        self.initial_sp_rate = QDoubleSpinBox()
        self.final_sp_rate = QDoubleSpinBox()
        self.steps_time_val = QDoubleSpinBox()
        self.initSpinBoxes()
        self.steps_time_sel = QComboBox()
        # Connect selector to sel value label field
        self.steps_time_sel.activated.connect(self.selection)
        self.steps_time_sel.addItems(['Step', 'Time'])
        self.step_time_label = QLabel('Step Size')


        # Construct view
        layout = QHBoxLayout()
        # Left side
        left_fields = QFormLayout()
        left_fields.addRow('Initial SP rate', self.initial_sp_rate)
        left_fields.addRow('Final SP rate', self.final_sp_rate)
        layout.addLayout(left_fields)
        # Right side
        right_fields = QFormLayout()
        right_fields.addRow('Progress', self.steps_time_sel)
        right_fields.addRow(self.step_time_label, self.steps_time_val)
        layout.addLayout(right_fields)

        self.setLayout(layout)
        # Start locked, when connected unlock
        self.lock()

    def selection(self):
        val_selected = self.steps_time_sel.currentText()
        # Clear values
        self.steps_time_val.cleanText()
        if val_selected == 'Step':
            label_text = 'Step Size'
            # Change properties of val field
            self.initSpinBox(self.steps_time_val)
        else:
            label_text = 'Test Duration'
            self.TimeSpinBox(self.steps_time_val)
        
        self.step_time_label.setText(label_text)
    
    def initSpinBoxes(self):
        boxes = [self.initial_sp_rate, self.final_sp_rate, self.steps_time_val]
        for box in boxes:
            self.initSpinBox(box)

    def initSpinBox(self,box):
        box.setMinimum(LOWEST_SP)
        box.setMaximum(HIGHEST_SP)
        box.setSingleStep(STEP_INCREMENT)
        box.setDecimals(USE_DECIMALS)
        box.setSuffix(SP_UNITS)
    
    def TimeSpinBox(self,box):
        box.setMaximum(1)
        box.setMaximum(999)
        box.setSingleStep(1)
        box.setDecimals(0)
        box.setSuffix("\t min")

    def lock(self):
        items = [self.initial_sp_rate, self.final_sp_rate, self.steps_time_val, self.steps_time_sel]
        for item in items:
            item.setEnabled(False)
        self.locked = True

    def unlock(self):
        items = [self.initial_sp_rate, self.final_sp_rate, self.steps_time_val, self.steps_time_sel]
        for item in items:
            item.setEnabled(True)

        self.locked = False

    def getValues(self, value_dict):
        value_dict['initial']=self.initial_sp_rate.value()
        value_dict['final'] = self.final_sp_rate.value()
        value_dict['progress']=self.steps_time_sel.currentText()
        value_dict['p_val']=self.steps_time_val.value()




class ControllerGUI(QMainWindow):
    # Controller GUI
    def __init__(self, parent=None):
        super().__init__(parent)
        # Window parameters
        self.setWindowTitle('Brooks Simple Serial Controller')
        # Internal layout
        self.setCentralWidget(CentralWidget(self))


if __name__ == '__main__':
    controllerApp = QApplication([])
    controllerInt = ControllerGUI()
    controllerInt.show()
    sys.exit(controllerApp.exec_())