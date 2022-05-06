import time
import getopt, sys
import pickle
import socket
# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.mpu9250 as mpu9250


class Base:
    def __init__(self, ip = '10.0.0.187', port = 1234, function='test'):
        self.ip = ip
        self.port = port
        if function == 'test':
            self.test()
        elif function == 'mpu9250':
            self.mpu9250()
        else:
            self.test()

    def test(self):
        self.socketConnect()

        while True:
            print('Waiting for client to connect')
            clientsocket, address = self.s.accept()
            print(f"Connection from {self.ip} has been established!")
            clientsocket.send(bytes("Welcome to the server!", "utf-8"))
    
    # method to keep connecting method consistent 
    def socketConnect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('',self.port))
        self.s.listen(5)
        
    def mpu9250(self):
        print('todo')
        
        
        ##############################

        
        
        
        
        rcpy.set_state(rcpy.RUNNING)
        mpu9250.initialize(enable_magnetometer = True)
        
        #  tcp socket HEADER
        #HEADERSIZE = 15
        #HEADER_MSG = f"The time is! {time.time()}"
        #HEADER = "{:<1{HEADERSIZE}}".format(HEADER_MSG)
        
        self.socketConnect()
        
        
        print('Wait for Socket Connection')
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")
        
        print("Press Ctrl-C to exit")
        
        # header for server text
        print("   Accel XYZ (m/s^2) |"
              "    Gyro XYZ (deg/s) |", end='')
        print("  Mag Field XYZ (uT) |", end='')
        print(' Temp (C) |', end='')
        print(' Time (s)')
        
        
        
        try:    # keep running
            while True:
                if rcpy.get_state() == rcpy.RUNNING:
                    temp = mpu9250.read_imu_temp()
                    data = mpu9250.read()
                    
                    formatted_txt = ('\r{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                           '{1[0]:6.1f} {1[1]:6.1f} {1[2]:6.1f} |'
                           '{2[0]:6.1f} {2[1]:6.1f} {2[2]:6.1f} |'
                           '   {3:6.1f} |' '   {4:6.1f}').format(data['accel'],
                                                 data['gyro'],
                                                 data['mag'],
                                                 temp,
                                                 time.time())
                          
                    print(formatted_txt,end='')
        
                    # now do the socket thing
                    msg = pickle.dumps((data,temp))
                    #msg = bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8") + msg
                    #msg = bytes(f'{len(msg):<{HEADERSIZE}}'+formatted_txt,"utf-8")
                    
                    clientsocket.send(msg)
                    
                time.sleep(0.1)  # sleep some
                
        except KeyboardInterrupt:
            # Catch Ctrl-C
            pass
        
        finally:
            print("\nBye BeagleBone!")
        ##############################
        
if __name__ == '__main__':
    # b = Base()
    b = Base(function = 'mpu9250')

