# Serial comms manager

import serial.tools.list_ports
import serial


# STRINGS AND COMMANDS
WRITE_VALUE = 'AZ.{channel}P{parameter}={value}\r'



def abortSequence(serial_comms, parameter=1):
    for i in range(4):
        channel = 2*(i + 1)
        packet = bytes(WRITE_VALUE.format(channel=channel, parameter=parameter, value=0.00),'utf-8')
        try:
            serial_comms.write(packet)
        except:
            raise Exception('Abort Sequence FAILED, please turn off device manually!')

def setValue(serial_comms, channel, parameter, value):
    packet = bytes(WRITE_VALUE.format(channel=channel, parameter=parameter, value=value),'utf-8')
    print(packet)
    try:
        serial_comms.write(packet)
    except:
        print("WOW no esta implementada esta excepcion")

def getPorts():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

if __name__ == '__main__':
    #getPorts()

    serial_comms = serial.Serial('/dev/ttyUSB0') # timeout=5.0
    serial_comms.write(b'azi\r')
    response = serial_comms.readline()
    response= response.decode('utf-8')
    print(response.strip())
    #serial_comms.close()

    #setValue(serial_comms, 8,1,1.01)
    #abortSequence(serial_comms)
    serial_comms.close()