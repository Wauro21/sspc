# Fields to control the test
import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QPushButton, QApplication, QHBoxLayout, QDoubleSpinBox, QFormLayout, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt, pyqtSignal
import math
import numpy as np
from MessageBox import WarningBox
__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'

# Constants for operation
# -> SP rate parameters
LOWEST_SP = 0.000
HIGHEST_SP = 999.999
STEP_INCREMENT = 0.001
USE_DECIMALS = 3
SP_UNITS = '\tsl/min'
SP_TOLERANCE = STEP_INCREMENT/10.0


# -> Time parameters: In seconds
MIN_TIME_STEP = 5 # s
MAX_TIME_STEP = 120 #s
TIME_STEP_INCREMENT = 1
TIME_DECIMALS = 0
TIME_UNITS = '\t s'


class ControlFields(QWidget):
    start_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    abort_signal = pyqtSignal()

    def __init__(self, parent=None):
        
        super().__init__(parent)

        # Objects
        self.step_route = None
        self.status = True
        self.verifed = True

        # Widgets
        # -> Test fields
        self.initial_sp_rate = QDoubleSpinBox()
        self.final_sp_rate = QDoubleSpinBox()
        self.step_size = QDoubleSpinBox()
        self.time_step = QDoubleSpinBox()

        # -> Progress bar
        self.progress = QProgressBar()

        # -> Bot buttons
        self.verify_btn = QPushButton('Verify')
        self.start_stop_btn = QPushButton('Start')
        self.abort_btn = QPushButton('ABORT')


        # -> list of lockable fields
        self.fields = [self.initial_sp_rate, self.final_sp_rate, self.step_size, self.time_step]

        # Init routine 
        self.SPBoxesConfig()
        self.abort_btn.setStyleSheet('background-color : red; font-weight : bold')
        self.start_stop_btn.setEnabled(False)
        self.TimeBoxConfig(self.time_step)
        self.SPStepBoxConfig(self.step_size)

        # Signals and slots
        self.verify_btn.clicked.connect(self.verify)
        self.start_stop_btn.clicked.connect(self.StartStopHandler)
        self.abort_btn.clicked.connect(lambda: self.abort_signal.emit())
        self.initial_sp_rate.valueChanged.connect(self.fieldsChanged)
        self.final_sp_rate.valueChanged.connect(self.fieldsChanged)
        self.step_size.valueChanged.connect(self.fieldsChanged)
        self.time_step.valueChanged.connect(self.fieldsChanged)


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
        right_fields.addRow('Step Size', self.step_size)
        right_fields.addRow('Time Step', self.time_step)
        form_cols.addLayout(right_fields)

        layout.addLayout(form_cols)

        # -> Progrss bar
        layout.addWidget(self.progress)

        # -> Bottom buttons
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.verify_btn)
        btn_row.addWidget(self.start_stop_btn)
        btn_row.addWidget(self.abort_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)

        
    def SPBoxesConfig(self):
        boxes = [self.initial_sp_rate, self.final_sp_rate]
        for box in boxes:
            self.SPBoxConfig(box)


    def SPBoxConfig(self, box):
        box.setMinimum(LOWEST_SP)
        box.setMaximum(HIGHEST_SP)
        box.setSingleStep(STEP_INCREMENT)
        box.setDecimals(USE_DECIMALS)
        box.setSuffix(SP_UNITS)
    
    def SPStepBoxConfig(self,box):
        box.setMinimum(STEP_INCREMENT)
        box.setMaximum(HIGHEST_SP)
        box.setSingleStep(STEP_INCREMENT)
        box.setDecimals(USE_DECIMALS)
        box.setSuffix(SP_UNITS)

    def TimeBoxConfig(self,box):
        box.setMinimum(MIN_TIME_STEP)
        box.setMaximum(MAX_TIME_STEP)
        box.setSingleStep(TIME_STEP_INCREMENT)
        box.setDecimals(TIME_DECIMALS)
        box.setSuffix(TIME_UNITS)

    def getFieldsValues(self):
        ret_dict = {
            'initial':self.initial_sp_rate.value(),
            'final':self.final_sp_rate.value(),
            'sp_step':self.step_size.value(),
            'time_step':self.time_step.value()
        }
        return ret_dict

    def colorSpin(self, spin, color='#f86e6c'):
        spin.setStyleSheet('background-color : {};'.format(color))

    def fieldsChanged(self):
        # If any of the controls fields change and the last values were verified, lock everything as start
        if(self.verifed):
            self.verifed = not self.verifed
            self.start_stop_btn.setEnabled(False)

        else:
            return

    def verify(self):
        values = self.getFieldsValues()
        
        delta_sp = values['final'] - values['initial']

        # Check if Initial and Final SP are over SP_TOLERANCE
        if (math.isclose(delta_sp, 0.0, rel_tol = SP_TOLERANCE, abs_tol = 0.0)):
            self.colorSpin(self.initial_sp_rate)
            self.colorSpin(self.final_sp_rate)
            warning_msg = WarningBox('Initial and Final SP rates are too close, less than tolerance: {}'.format(SP_TOLERANCE), self)
            warning_msg.exec_()
            self.colorSpin(self.initial_sp_rate, color='')
            self.colorSpin(self.final_sp_rate, color='')
            return

        steps = np.sign(delta_sp)*values['sp_step']
        f_steps = delta_sp/steps # Needed steps
        n_steps = math.floor(f_steps) # Complete steps 
        last_flag = False


        # Check if required steps are factible
        last_step = 0.0
        if not (math.isclose(f_steps, n_steps, rel_tol=SP_TOLERANCE, abs_tol=0.0)):
            last_step = delta_sp - n_steps*steps
            # if not(math.isclose(last_step, STEP_INCREMENT, rel_tol=SP_TOLERANCE, abs_tol=0.0)):
            #     self.colorSpin(self.step_size)
            #     warning_msg = WarningBox('<b>Last step for run is not factible with the given step size</b>. Last Step needed {:.3f}, Step size needed {:.3f}'.format(last_step, values['sp_step']))
            #     warning_msg.exec_()
            #     self.colorSpin(self.step_size,color='')
            #     return
            last_flag = True

        # Generate steps for thread
        step_list = []
        # 1- Initial point
        step_list.append(values['initial'])

        # 2- Generate steps
        i_step = values['initial']
        for i in range(n_steps):
            i_step += steps
            step_list.append(i_step)

        # 3- Add last step if necessary
        if(last_flag):
            i_step += last_step
            step_list.append(i_step)        

        self.step_route = {
            'initial':values['initial'],
            'final':values['final'],
            'delta_sp':delta_sp,
            'n_steps':n_steps,
            'step_size':steps,
            'last_flag':last_flag,
            'last_step':last_step,
            'time_step':values['time_step'],
            'step_list':step_list
        }

        # If everything checks, enable start button
        self.verifed = True
        self.start_stop_btn.setEnabled(True)

    def StartStopHandler(self):
        # Check button status
        btn_status = self.start_stop_btn.text()
        
        if btn_status == 'Start':
            btn_text = 'Stop'
            self.verify_btn.setEnabled(False)
            self.start_signal.emit()

        else:
            btn_text = 'Start'
            self.verify_btn.setEnabled(True)
            self.stop_signal.emit()

        self.start_stop_btn.setText(btn_text)


    def stopHandler(self):
        self.verify_btn.setEnabled(True)
        self.start_stop_btn.setText('Start')

    def getRoute(self):
        return self.step_route

    def lockFields(self):
        self.status = not self.status

        for item in self.fields:
            item.setEnabled(self.status)



    def progressHandler(self):
        print(self.step_route)


if __name__ == '__main__':
    app = QApplication([])
    widget = ControlFields()
    widget.show()
    sys.exit(app.exec_())