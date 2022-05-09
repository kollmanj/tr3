import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import pickle
import time

class Base:
    def __init__(self, ip='10.0.0.187',port=1234):
        self.ip = ip
        self.port = port

    def test(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.ip,self.port))
        msg = s.recv(1024)
        print(msg.decode("utf-8"))

def BBNAU7802():
    try:
        m = socketPlotter('10.0.0.87',24)
        
        fig, ax = plt.subplots()
        scope = Scope(ax,ylim_min=11000,ylim_max=19000)
        
        # pass a generator in "emitter" to produce data for the update func
        ani = animation.FuncAnimation(fig, scope.update, m.loop, interval=10,
                                      blit=True)
        
        plt.show()
    except KeyboardInterrupt:
        print('Interrupted')
        m.sock.close()

def MPU9250_BBBlue():
    try:
        m = MPU9250('10.0.0.223')
        
        fig, ax = plt.subplots()
        scope = Scope(ax,ylim_min=-11,ylim_max=11)
        
        # pass a generator in "emitter" to produce data for the update func
        ani = animation.FuncAnimation(fig, scope.update, m.loop, interval=10,
                                      blit=True)
        
        plt.show()
    except KeyboardInterrupt:
        print('Interrupted')
        m.sock.close()

def tr3BBB():
    try:
        m = tr3('10.0.0.224') # ip address

       
        # temperature plot
        fig1, ax1 = plt.subplots()
        scope1 = Scope(ax1)
        plt.title('Temperature')
        
        # pass a generator in "emitter" to produce data for the update func
        ax1.set(ylim=(90, 300))
        ani1 = animation.FuncAnimation(fig1, scope1.update, m.loop('temp'), interval=10,
                                      blit=True)
        
        # rpm plot
        fig2, ax2 = plt.subplots()
        scope2 = Scope(ax2)
        plt.title('RPM')
        
        # pass a generator in "emitter" to produce data for the update func
        ani2 = animation.FuncAnimation(fig2, scope2.update, m.loop('rpm'), interval=10,
                                      blit=True)
        #speed plot
        fig3, ax3 = plt.subplots()
        scope3 = Scope(ax3)
        plt.title('Speed')
        
        # pass a generator in "emitter" to produce data for the update func
        ani3 = animation.FuncAnimation(fig3, scope3.update, m.loop('speed'), interval=10,
                                      blit=True)
        #plt.autoscale(enable=True, axis='both', tight=None)
        plt.show()
    except KeyboardInterrupt:
        print('Interrupted')
        s.close()



class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02,ylim_min=-10,ylim_max=10):
        ylim_min = ylim_min   # TODO adjust this 
        ylim_max = ylim_max
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(ylim_min, ylim_max)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

class socketPlotter():
    def __init__(self,ip='10.0.0.223',msgSize=231):
        self.msgSize = msgSize  #  specific to the message, has to be right, find size of msg being sent, put it here
        self.serverIP = ip
        self.serverPort = 1234
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.serverIP,self.serverPort))
        self.msg = []
        
    def loop(self):  # this is the emmitter is the example
        while True:
            msg_bytes = self.sock.recv(self.msgSize)
            self.msg = pickle.loads(msg_bytes)
            accel_dict = self.msg[0] 
            #accel_data = accel_dict['accel']   # for accelerometer
            yield accel_dict      # for weight
            #yield accel_data[0]  # for accelerometer

# reads data coming from the MPU9250 on the beaglebone blue
class MPU9250(socketPlotter):
    def __init__(self,ip='10.0.0.223',msgSize=253):
        self.msgSize = msgSize  #  specific to the message, has to be right, find size of msg being sent, put it here
        self.serverIP = ip
        self.serverPort = 1234
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.serverIP,self.serverPort))
        self.msg = []
    def loop(self):  # this is the emmitter is the example
        while True:
            msg_bytes = self.sock.recv(self.msgSize)
            self.msg = pickle.loads(msg_bytes)   #######################################ERROR HERE
            accel_dict = self.msg[0] 
            accel_data = accel_dict['accel']   # for accelerometer
            yield accel_data[0]  # for accelerometer
            
class OilTemp(socketPlotter):
    def __init__(self,ip='10.0.0.223',msgSize=41):
        self.msgSize = msgSize  #  specific to the message, has to be right, find size of msg being sent, put it here
        self.serverIP = ip
        self.serverPort = 1234
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.serverIP,self.serverPort))
        self.msg = []
    def loop(self):  # this is the emmitter is the example
        while True:
            msg_bytes = self.sock.recv(self.msgSize)
            self.msg = pickle.loads(msg_bytes)   #######################################ERROR HERE
            accel_dict = self.msg
            accel_data = accel_dict['OilTemp']   # for accelerometer
            yield accel_data  # for accelerometer
            
# this class is for reading a data pickled and sent
class tr3():
     def __init__(self,ip='10.0.0.223'):
        self.msgSize = 41
        self.serverIP = ip
        self.serverPort = 1234
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.serverIP,self.serverPort))
        self.msg = []
        self.temperature = 0
        self.rpm = 0
        self.speed = 0
        self.sample_rate = 0

        
     def loop(self,dataType='temp'):
        while True:
            msg_bytes = self.sock.recv(self.msgSize)
            self.msg = pickle.loads(msg_bytes)
            #self.temperature = self.msg[0]
            # self.rpm= self.msg[1]
            # self.speed = self.msg[2]
            # self.sample_rate = self.msg[3]
            if dataType == 'temp':
                reading = self.msg[0] 
                # convert reading to Volts
                Vmax = 1.8
                V = Vmax*reading
                R = 22  # resistor in the voltage divider
                # convert voltage to resistance
                ohms = R*V/(Vmax-V)
                # convert from ohms to temperature
                y2 = 852.51*ohms**-0.296
            #     output = y2
            #     print(output,end='\t')
            # elif dataType == 'rpm':
            #     output = self.msg[1]
            #     print(output,end='\t')
            # else:
            #     output = self.msg[2]
            #     print(output,end='\r')
            # yield output

           

if __name__ == '__main__':
    #MPU9250_BBBlue()  # for the accelerometer
    #tr3BBB()     # for the temperature
    #BBNAU7802()
    a = tr3()
    a.loop()
    
