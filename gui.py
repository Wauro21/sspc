# Simple GUI for the controller

import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QFormLayout, QHBoxLayout, QComboBox, QDoubleSpinBox, QMenu, QPushButton, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
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

        # Connect Signals and slots
        self.connection_wdg.connect_signal.connect(self.control_wdg.unlock)
        self.connection_wdg.disconnect_signal.connect(self.control_wdg.lock)
        central_layout.addWidget(self.connection_wdg)
        central_layout.addWidget(self.control_wdg)
        
        self.setLayout(central_layout)
        


class ConnectionWidget(QWidget):
    connect_signal = QtCore.pyqtSignal()
    disconnect_signal = QtCore.pyqtSignal()

    def __init__(self,parent =None):
        super().__init__(parent)

        # Connection Options for the device
        self.status = False
        self.connect_btn = QPushButton('Connect')
        self.connect_btn.clicked.connect(self.connect)
        self.status_label = QLabel('Connection status: {}'.format(self.status))
        self.status_label.setAlignment(Qt.AlignCenter)
        layout = QHBoxLayout()
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def connect(self):
        # WIP TO BE IMPLEMENTED - Just a placeholder
        self.status = not self.status
        if self.status:
            # If connection successfull emit signal
            self.connect_signal.emit()
            text_val = 'Disconnect'
        else:
            text_val = 'Connect'
            self.disconnect_signal.emit()
        self.connect_btn.setText(text_val)
        self.status_label.setText('Connection status: {}'.format(self.status))
        print("NADA NO HACE ABSOLUTAMENTE NADA")        
        


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