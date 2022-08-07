import sys 
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QFormLayout, QDialog, QVBoxLayout, QHBoxLayout, QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal
import serial
from MessageBox import InformationBox

WRITE_CMD = 'AZ.{channel}P1={sp_value:.3f}\r'
ABORT_CMD = 'az.{channel}P1=0.000\r'

# Manual SP Parameters
LOWEST_SP = 0.000
HIGHEST_SP = 5.000
STEP_INCREMENT = 0.001
USE_DECIMALS = 3
SP_UNITS = '\tsl/min'

# Label Display
LBL_DISPLAY = '{value:.3f}'+SP_UNITS


class ManualControl(QDialog):
    manual_signal = pyqtSignal()
    auto_signal = pyqtSignal()

    def __init__(self, comms, channel , parent=None):
        super().__init__(parent)

        # Objects
        self.comms = comms
        self.channel = channel

        # Widgets 
        self.set_btn = QPushButton('Set')
        self.sp =QDoubleSpinBox()
        self.abort_btn = QPushButton('Abort')
        self.reported_label = QLabel('None')


        # Init Routine
        self.abort_btn.setStyleSheet('background-color : red; font-weight : bold')
        self.SPBoxConfig(self.sp)


        # Fields        
        fields_layout = QFormLayout()
        fields_layout.addRow('Set SP-Rate', self.sp)
        fields_layout.addRow('Device Reported SP-Rate', self.reported_label)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.set_btn)
        buttons_layout.addWidget(self.abort_btn)

        # Signals and slots
        self.set_btn.clicked.connect(self.toDevice)
        self.abort_btn.clicked.connect(self.abortSequence)

        # Layout
        layout = QVBoxLayout()
        layout.addLayout(fields_layout)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
    
    def SPBoxConfig(self,box):
        box.setMinimum(LOWEST_SP)
        box.setMaximum(HIGHEST_SP)
        box.setSingleStep(STEP_INCREMENT)
        box.setDecimals(USE_DECIMALS)
        box.setSuffix(SP_UNITS)


    def toDevice(self):

        # Send cmd
        sp = self.sp.value()
        cmd = WRITE_CMD.format(channel=self.channel, sp_value=sp).encode('utf_8')
        self.comms.write(cmd)

        # Read response and update label
        device_response = self.comms.readline().decode('utf_8')
        device_response = device_response.split(',')
        to_display = LBL_DISPLAY.format(value=float(device_response[4]))
        self.reported_label.setText(to_display)


    def abortSequence(self):
        # Set all channels to zero
        for i in range(1,5):
            CMD = ABORT_CMD.format(channel=2*i).encode('utf_8')
            self.comms.write(CMD)

        to_display = LBL_DISPLAY.format(value=0)
        self.reported_label.setText(to_display)
        
        msg = InformationBox('Abort sequence ended. All channels were set to zero')
        msg.exec_()        








if __name__ == '__main__':
    comms = serial.Serial('/dev/ttyUSB0')
    app = QApplication([])
    window = ManualControl(comms, 2)
    window.show()
    sys.exit(app.exec_())
