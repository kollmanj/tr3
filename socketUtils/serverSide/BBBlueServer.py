from __future__ import print_function
import qwiic_alphanumeric
import time
import sys
import base

def functionToPassIn(x):
        
    print("\nSparkFun Qwiic Alphanumeric - Example 4: Print String")
    my_display = qwiic_alphanumeric.QwiicAlphanumeric()

    if my_display.begin() == False:
        print("\nThe Qwiic Alphanumeric isn't connected to the system. Please check your connection.", \
            file=sys.stderr)
        return
    
    print("\nQwiic Alphanumeric ready!")

    # b = base.Base(function = '')
    
    # while True:
    # b.OilTemp()    
            
        
    x = str(int(1000*x))
    
    my_display.print(str(x))
    # my_display.print('1234')

def main():
    
    print("\nSparkFun Qwiic Alphanumeric - Example 4: Print String")
    my_display = qwiic_alphanumeric.QwiicAlphanumeric()

    if my_display.begin() == False:
        print("\nThe Qwiic Alphanumeric isn't connected to the system. Please check your connection.", \
            file=sys.stderr)
        return
    
    print("\nQwiic Alphanumeric ready!")

    b = base.Base(function = '')
    
    # while True:
    b.OilTemp(additionalFunction=functionToPassIn)    
            
        

    
    # my_display.print(str(potVal))


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding")
        sys.exit(0)