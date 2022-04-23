#!/usr/bin/env python3
# Read and display IMU
# Based on: https://raw.githubusercontent.com/mcdeoliveira/rcpy/master/examples/rcpy_test_imu.py
# import python libraries
import time
import getopt, sys
import time
import pickle
import socket
import PyNAU7802
import smbus2

bus = smbus2.SMBus(2)

scale = PyNAU7802.NAU7802()
if scale.begin(bus):
    print("Connected! \n")
else:
    print("Not Connected\n")

    

#  tcp socket HEADER
#HEADERSIZE = 15
#HEADER_MSG = f"The time is! {time.time()}"
#HEADER = "{:<1{HEADERSIZE}}".format(HEADER_MSG)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1234))
s.listen(5)  # que


print('Wait for Socket Connection')
clientsocket, address = s.accept()
#print(f"Connection from {address} has been established!")
print("Connection from has been established!")

print("Press Ctrl-C to exit")

# header for server text
print("   Accel XYZ (m/s^2) |"
      "    Gyro XYZ (deg/s) |", end='')
print("  Mag Field XYZ (uT) |", end='')
print(' Temp (C) |', end='')
print(' Time (s)')



try:    # keep running
    while True:
        w = scale.getWeight()
        #if rcpy.get_state() == rcpy.RUNNING:
        #    temp = mpu9250.read_imu_temp()
        #    data = mpu9250.read()
            
        #    formatted_txt = ('\r{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
        #           '{1[0]:6.1f} {1[1]:6.1f} {1[2]:6.1f} |'
        #           '{2[0]:6.1f} {2[1]:6.1f} {2[2]:6.1f} |'
        #           '   {3:6.1f} |' '   {4:6.1f}').format(data['accel'],
        #                                 data['gyro'],
        #                                 data['mag'],
        #                                 temp,
        #                                 time.time())
                  
        #    print(formatted_txt,end='')

            # now do the socket thing
        msg = pickle.dumps((w,w))  # TODO, just sending twice because I am lazy
            #msg = bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8") + msg
            #msg = bytes(f'{len(msg):<{HEADERSIZE}}'+formatted_txt,"utf-8")
            
        clientsocket.send(msg)
            
        time.sleep(0.1)  # sleep some
        
except KeyboardInterrupt:
    # Catch Ctrl-C
    pass

finally:
    print("\nBye BeagleBone!")

