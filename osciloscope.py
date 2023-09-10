import time
import matplotlib.pyplot as plt
from drawnow import *
import serial
import numpy as np
val = [ ]
cnt = 0
port = serial.Serial('/dev/tty.usbserial-B00054LQ', 115200, timeout=0.5)
plt.figure()
p = plt.plot(0, 'ro-', label='Channel 0')
plt.ylim(-1023,1023)
plt.title('Osciloscope')
plt.grid(True)
plt.ylabel('ADC outputs')
plt.legend(loc='lower right')
# plt.show()
plt.ion()     

while (True):
    port.write(b's') #handshake with Arduino
    if (port.inWaiting()):# if the arduino replies
        value = port.readline()# read the reply
        number = float(str(value[:-2])[2:-1]) #convert received data to integer 
        time.sleep(0.01)
        val.append(int(number))
        p[0].set_ydata(val)
        p[0].set_xdata(list(range(len(val))))
        plt.draw()
        plt.pause(.000001)
        cnt = cnt+1
    if(cnt>50):
        val.pop(0)#keep the plot fresh by deleting the data at position 0