# A thread-worker that dispatches the commands used by the flowmeter
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import serial
import time

WRITE_CMD = 'AZ.{channel}P1={sp_value:.3f}\r'

class Dispatcher(QObject):
    finished = pyqtSignal()

    def __init__(self, serial_comms, channel, step_route):
        super().__init__()
        self.serial_comms = serial_comms
        self.channel = channel
        self.step_route = step_route

    def run(self):
        print("WOW im running")
        initial_sp = self.step_route['initial']
        step_delay = self.step_route['time_step']

        # Setup initial sp rate
        self.serial_comms.write(self.setupSP(self.channel, initial_sp))        
        time.sleep(step_delay)

        # Start with the n-steps that are covered by the step_size
        next_step = initial_sp
        for step in range(self.step_route['n_steps']):
            next_step += self.step_route['step_size']
            self.serial_comms.write(self.setupSP(self.channel, next_step))
            time.sleep(step_delay)
        
        # If last_step is needed, send the command
        if(self.step_route['last_flag']):
            next_step += self.step_route['last_step']
            self.serial_comms.write(self.setupSP(self.channel, next_step))


        

    def setupSP(self,channel, sp_value):
        cmd = WRITE_CMD.format(channel=channel, sp_value=sp_value)
        print(cmd)
        return cmd.encode('utf_8')
