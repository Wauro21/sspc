# Fields to control the test
import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QPushButton, QApplication, QHBoxLayout, QDoubleSpinBox, QFormLayout, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt

__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'

# Constants for operation
LOWEST_SP = 0.000
HIGHEST_SP = 999.999
STEP_INCREMENT = 0.001
USE_DECIMALS = 3
SP_UNITS = '\tsl/min'



class ControlFields(QWidget):

    def __init__(self, parent=None):
        
        super().__init__(parent)

        # Widgets
        # -> Test fields
        self.initial_sp_rate = QDoubleSpinBox()
        self.final_sp_rate = QDoubleSpinBox()
        self.steps_time_val = QDoubleSpinBox()
        self.steps_time_sel = QComboBox()
        self.step_time_label = QLabel('Step Size')
        # -> Bot buttons
        self.verify_btn = QPushButton('Verify')
        self.start_stop_btn = QPushButton('Start')
        self.abort_btn = QPushButton('ABORT')

        # Init routine 
        self.initSpinBoxes()
        self.steps_time_sel.addItems(['Step', 'Time'])
        self.abort_btn.setStyleSheet('background-color : red; font-weight : bold')

        # Signals and slots
        self.steps_time_sel.activated.connect(self.selectStep)

        # Layout
        layout = QVBoxLayout()
        form_cols = QHBoxLayout()

        # -> left column
        left_fields = QFormLayout()
        left_fields.addRow('Initial SP rate', self.initial_sp_rate)
        left_fields.addRow('Final SP rate', self.final_sp_rate)
        form_cols.addLayout(left_fields)
        
        # -> right column
        right_fields = QFormLayout()
        right_fields.addRow('Progress', self.steps_time_sel)
        right_fields.addRow(self.step_time_label, self.steps_time_val)
        form_cols.addLayout(right_fields)

        layout.addLayout(form_cols)

        # -> Bottom buttons
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.verify_btn)
        btn_row.addWidget(self.start_stop_btn)
        btn_row.addWidget(self.abort_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)

        
    def initSpinBoxes(self):
        boxes = [self.initial_sp_rate, self.final_sp_rate, self.steps_time_val]
        for box in boxes:
            self.initSpinBox(box)


    def initSpinBox(self, box):
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

    def selectStep(self):
        selection = self.steps_time_sel.currentText()

        # Clear Values
        self.steps_time_val.cleanText()

        if selection == 'Step':
            text_label = 'Step Size'
            self.initSpinBox(self.steps_time_val)

        else:
            text_label = 'Test Duration'
            self.TimeSpinBox(self.steps_time_val)

if __name__ == '__main__':
    app = QApplication([])
    widget = ControlFields()
    widget.show()
    sys.exit(app.exec_())