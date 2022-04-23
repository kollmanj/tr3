#########
#NOTES
# need to have i2c connect on other side to work consistently
# maybe pull up resistor is an issue?
#
#########
import time
import i2cdriver
import struct

###########################################
# Constants
###########################################
""" Address """
DEVICE_ADDRESS = 0x2A

""" Register Map """
NAU7802_PU_CTRL = 0x00
NAU7802_CTRL1 = 0x01
NAU7802_CTRL2 = 0x02
NAU7802_OCAL1_B2 = 0x03
NAU7802_OCAL1_B1 = 0x04
NAU7802_OCAL1_B0 = 0x05
NAU7802_GCAL1_B3 = 0x06
NAU7802_GCAL1_B2 = 0x07
NAU7802_GCAL1_B1 = 0x08
NAU7802_GCAL1_B0 = 0x09
NAU7802_OCAL2_B2 = 0x0A
NAU7802_OCAL2_B1 = 0x0B
NAU7802_OCAL2_B0 = 0x0C
NAU7802_GCAL2_B3 = 0x0D
NAU7802_GCAL2_B2 = 0x0E
NAU7802_GCAL2_B1 = 0x0F
NAU7802_GCAL2_B0 = 0x10
NAU7802_I2C_CONTROL = 0x11
NAU7802_ADCO_B2 = 0x12
NAU7802_ADCO_B1 = 0x13
NAU7802_ADCO_B0 = 0x14
NAU7802_ADC = 0x15  # Shared ADC and OTP 32:24
NAU7802_OTP_B1 = 0x16 # OTP 23:16 or 7:0?
NAU7802_OTP_B0 = 0x17 # OTP 15:8
NAU7802_PGA = 0x1B
NAU7802_PGA_PWR = 0x1C
NAU7802_DEVICE_REV = 0x1F

""" Bits within the PU_CTRL register """
NAU7802_PU_CTRL_RR = 0
NAU7802_PU_CTRL_PUD = 1
NAU7802_PU_CTRL_PUA = 2
NAU7802_PU_CTRL_PUR = 3
NAU7802_PU_CTRL_CS = 4
NAU7802_PU_CTRL_CR = 5
NAU7802_PU_CTRL_OSCS = 6
NAU7802_PU_CTRL_AVDDS = 7

""" Bits within the CTRL1 register """
NAU7802_CTRL1_GAIN = 2
NAU7802_CTRL1_VLDO = 5
NAU7802_CTRL1_DRDY_SEL = 6
NAU7802_CTRL1_CRP = 7

""" Bits within the CTRL2 register """
NAU7802_CTRL2_CALMOD = 0
NAU7802_CTRL2_CALS = 2
NAU7802_CTRL2_CAL_ERROR = 3
NAU7802_CTRL2_CRS = 4
NAU7802_CTRL2_CHS = 7

""" Bits within the PGA register """
NAU7802_PGA_CHP_DIS = 0
NAU7802_PGA_INV = 3
NAU7802_PGA_BYPASS_EN = 4
NAU7802_PGA_OUT_EN = 5
NAU7802_PGA_LDOMODE = 6
NAU7802_PGA_RD_OTP_SEL = 7

""" Bits within the PGA PWR register """
NAU7802_PGA_PWR_PGA_CURR = 0
NAU7802_PGA_PWR_ADC_CURR = 2
NAU7802_PGA_PWR_MSTR_BIAS_CURR = 4
NAU7802_PGA_PWR_PGA_CAP_EN = 7

""" Allowed Low drop out regulator voltages """
NAU7802_LDO_2V4 = 0b111
NAU7802_LDO_2V7 = 0b110
NAU7802_LDO_3V0 = 0b101
NAU7802_LDO_3V3 = 0b100
NAU7802_LDO_3V6 = 0b011
NAU7802_LDO_3V9 = 0b010
NAU7802_LDO_4V2 = 0b001
NAU7802_LDO_4V5 = 0b000

""" Allowed gains """
NAU7802_GAIN_128 = 0b111
NAU7802_GAIN_64 = 0b110
NAU7802_GAIN_32 = 0b101
NAU7802_GAIN_16 = 0b100
NAU7802_GAIN_8 = 0b011
NAU7802_GAIN_4 = 0b010
NAU7802_GAIN_2 = 0b001
NAU7802_GAIN_1 = 0b000

""" Allowed samples per second """
NAU7802_SPS_320 = 0b111
NAU7802_SPS_80 = 0b011
NAU7802_SPS_40 = 0b010
NAU7802_SPS_20 = 0b001
NAU7802_SPS_10 = 0b000

""" Select between channel values """
NAU7802_CHANNEL_1 = 0
NAU7802_CHANNEL_2 = 1

""" Calibration state """
NAU7802_CAL_SUCCESS = 0
NAU7802_CAL_IN_PROGRESS = 1
NAU7802_CAL_FAILURE = 2


###########################################
# Classes
###########################################
class NAU7802:
    """ Class to communicate with the NAU7802 """
#    _i2cPort: smbus2.SMBus = None
    _zeroOffset = 0
    _calibrationFactor = 1.0
    def begin(self, wire_port= i2cdriver.I2CDriver("/dev/ttyUSB0"), initialize: bool = True) -> bool:
        self._i2cPort = wire_port
        
        # Check if the device ACK's over I2C
        if not self.isConnected():
            # There are rare times when the sensor is occupied and doesn't ACK. A 2nd try resolves this.
            if not self.isConnected():
                return False

        result = True  # Accumulate a result as we do the setup
        if initialize:
            result &= self.reset()  # Reset all registers            
            result &= self.powerUp()  # Power on analog and digital sections of the scale
            result &= self.setLDO(NAU7802_LDO_3V3)  # Set LDO to 3.3V
            result &= self.setGain(NAU7802_GAIN_128)  # Set gain to 128
            result &= self.setSampleRate(NAU7802_SPS_80)  # Set samples per second to 10
            result &= self.setRegister(NAU7802_ADC, 0x30)  # Turn off CLK_CHP. From 9.1 power on sequencing.
            result &= self.setBit(NAU7802_PGA_PWR_PGA_CAP_EN, NAU7802_PGA_PWR)  # Enable 330pF decoupling cap on ch. 2.
           # # From 9.14 application circuit note.
            result &= self.calibrateAFE()  # Re - cal analog frontend when we change gain, sample rate, or channel

        return result
    
    def isConnected(self) -> bool:
        """ Returns true if device ACK's at the I2C address """
        try:
            self._i2cPort.start(0x75, 1)
            self._i2cPort.read(1)
            self._i2cPort.stop()
            #self._i2cPort.regrd(DEVICE_ADDRESS,0)
            return True  # All good
        except OSError:
            return False  # Sensor did not ACK
        


    def available(self) -> bool:
        """ Returns true if Cycle Ready bit is set (conversion is complete) """
        return self.getBit(NAU7802_PU_CTRL_CR, NAU7802_PU_CTRL)
        #return True
 
    def powerUp(self) -> bool:
        """ Power up digital and analog sections of scale, ~2 mA """
        self.setBit(NAU7802_PU_CTRL_PUD, NAU7802_PU_CTRL)
        self.setBit(NAU7802_PU_CTRL_PUA, NAU7802_PU_CTRL)

        #self.clearBit(NAU7802_PU_CTRL_RR,NAU7802_PU_CTRL)

        # Wait for Power Up bit to be set - takes approximately 200us
        counter = 0
        while not self.getBit(NAU7802_PU_CTRL_PUR, NAU7802_PU_CTRL):
            time.sleep(0.001)
            if counter > 100:
                return False  # Error
            counter += 1

        return True   
 
    def setGain(self, gain_value: int) -> bool:
        """ Set the gain.x1, 2, 4, 8, 16, 32, 64, 128 are available """
        if gain_value > 0b111:
            gain_value = 0b111  # Error check

        value = self.getRegister(NAU7802_CTRL1)
        value &= 0b11111000  # Clear gain bits
        value |= gain_value  # Mask in new bits

        return self.setRegister(NAU7802_CTRL1, value)
    
    def getReading(self) -> int:
        """ Returns 24 bit reading. Assumes CR Cycle Ready bit
        (ADC conversion complete) has been checked by .available() """
        value_list = []
        try:
            value_list.append(self._i2cPort.regrd(DEVICE_ADDRESS, NAU7802_ADCO_B2))
            value_list.append(self._i2cPort.regrd(DEVICE_ADDRESS, NAU7802_ADCO_B1))
            value_list.append(self._i2cPort.regrd(DEVICE_ADDRESS, NAU7802_ADCO_B0))

        except OSError:
            return False  # Sensor did not ACK

        value = int.from_bytes(value_list, byteorder='big', signed=True)

        return value

    def getAverage(self, average_amount: int) -> int:
        """ Return the average of a given number of readings """
        total = 0
        samples_acquired = 0

        start_time = time.time()

        while samples_acquired < average_amount:
            if self.available():
                total += self.getReading()
                samples_acquired += 1

            if time.time() - start_time > 1.0:
                return 0  # Timeout - Bail with error

            time.sleep(0.001)

        total /= average_amount

        return total
   
    def setLDO(self, ldo_value: int) -> bool:
        """ Set the on board Low - Drop - Out voltage regulator to a given value.
        2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.2, 4.5 V are available """
        if ldo_value > 0b111:
            ldo_value = 0b111  # Error check

        # Set the value of the LDO
        value = self.getRegister(NAU7802_CTRL1)
        value &= 0b11000111  # Clear LDO bits
        value |= ldo_value << 3  # Mask in new LDO bits
        self.setRegister(NAU7802_CTRL1, value)

        return self.setBit(NAU7802_PU_CTRL_AVDDS, NAU7802_PU_CTRL)  # Enable the internal LDO
 
    def setSampleRate(self, rate: int) -> bool:
        """ Set the readings per second. 10, 20, 40, 80, and 320 samples per second is available """
        if rate > 0b111:
            rate = 0b111  # Error check

        value = self.getRegister(NAU7802_CTRL2)
        value &= 0b10001111  # Clear CRS bits
        value |= rate << 4  # Mask in new CRS bits

        return self.setRegister(NAU7802_CTRL2, value)
 
    def calibrateAFE(self) -> bool:
        """ Synchronous calibration of the analog front end of the NAU7802.
        Returns true if CAL_ERR bit is 0 (no error) """
        self.beginCalibrateAFE()
        return self.waitForCalibrateAFE(1000)   

    def beginCalibrateAFE(self) -> None:
        """ Begin asynchronous calibration of the analog front end of the NAU7802.
        Poll for completion with calAFEStatus() or wait with waitForCalibrateAFE(). """
        self.setBit(NAU7802_CTRL2_CALS, NAU7802_CTRL2)

    def waitForCalibrateAFE(self, timeout_ms: int = 0) -> bool:
        """ Wait for asynchronous AFE calibration to complete with optional timeout. """
        timeout_s = timeout_ms/1000
        begin = time.time()
        cal_ready = self.calAFEStatus()

        while cal_ready == NAU7802_CAL_IN_PROGRESS:
            if (timeout_ms > 0) & ((time.time() - begin) > timeout_s):
                break
            time.sleep(0.001)
            cal_ready = self.calAFEStatus()

        if cal_ready == NAU7802_CAL_SUCCESS:
            return True
        else:
            return False

    def calAFEStatus(self) -> int:
        """ Check calibration status. """
        if self.getBit(NAU7802_CTRL2_CALS, NAU7802_CTRL2):
            return NAU7802_CAL_IN_PROGRESS

        if self.getBit(NAU7802_CTRL2_CAL_ERROR, NAU7802_CTRL2):
            return NAU7802_CAL_FAILURE

        # Calibration passed
        return NAU7802_CAL_SUCCESS

    def getWeight(self, allow_negative_weights: bool = True, samples_to_take: int = 8) -> float:
        """ Once you 've set zero offset and cal factor, you can ask the library to do the calculations for you. """
        on_scale = self.getAverage(samples_to_take)

        # Prevent the current reading from being less than zero offset. This happens when the scale
        # is zero'd, unloaded, and the load cell reports a value slightly less than zero value
        # causing the weight to be negative or jump to millions of pounds

        if not allow_negative_weights:
            if on_scale < self._zeroOffset:
                on_scale = self._zeroOffset  # Force reading to zero

        weight = (on_scale - self._zeroOffset)/self._calibrationFactor
        return weight

    def reset(self) -> bool:
        """ Resets all registers to Power Of Defaults """
        self.setBit(NAU7802_PU_CTRL_RR, NAU7802_PU_CTRL)  # Set RR
        time.sleep(0.001)
        return self.clearBit(NAU7802_PU_CTRL_RR, NAU7802_PU_CTRL)  # Clear RR to leave reset state

    def setBit(self, bit_number: int, register_address: int) -> bool:
        """ Mask & set a given bit within a register """
        value = self.getRegister(register_address)
        value |= (1 << bit_number)  # Set this bit
        return self.setRegister(register_address, value)
 

 
    
    def clearBit(self, bit_number: int, register_address: int) -> bool:
        """ Mask & clear a given bit within a register """
        value = self.getRegister(register_address)
        value &= ~(1 << bit_number)  # Set this bit
        return self.setRegister(register_address, value)

    def getBit(self, bit_number: int, register_address: int) -> bool:
        """ Return a given bit within a register """
        value = self.getRegister(register_address)
        value &= (1 << bit_number)  # Clear all but this bit
        return bool(value)
    
    def getRegister(self, register_address: int) -> int:
        """ Get contents of a register """
        try:
            return self._i2cPort.regrd(DEVICE_ADDRESS, register_address)

        except OSError:
            return -1  # Sensor did not ACK
        
    def setRegister(self, register_address: int, value: int) -> bool:
        """ Send a given value to be written to given address.Return true if successful """
        try:
            self._i2cPort.regwr(DEVICE_ADDRESS, register_address, value)
            return True

        except OSError:
            return False
        
    def calculateZeroOffset(self, average_amount: int = 8) -> None:
        """ Also called taring. Call this with nothing on the scale """
        self.setZeroOffset(self.getAverage(average_amount))
        
    def setZeroOffset(self, new_zero_offset: int) -> None:
        """ Sets the internal variable. Useful for users who are loading values from NVM. """
        self._zeroOffset = new_zero_offset

    def getZeroOffset(self) -> int:
        """ Ask library for this value.Useful for storing value into NVM. """
        return self._zeroOffset
    
    def calculateCalibrationFactor(self, weight_on_scale: float, average_amount: int = 8) -> None:
        """ Call this with the value of the thing on the scale.
        Sets the calibration factor based on the weight on scale and zero offset. """
        onScale = self.getAverage(average_amount)
        newCalFactor = (onScale - self._zeroOffset)/weight_on_scale
        self.setCalibrationFactor(newCalFactor)
        
    def getCalibrationFactor(self) -> float:
        """ Ask library for this value.Useful for storing value into NVM. """
        return self._calibrationFactor
        
    def calibrateScale(self):
        print("Scale Calibration\n")
        anykey = input("Setup scale with no weight on it.  Press a key when ready.\n")
        self.calculateZeroOffset(64); #Zero or Tare the scale. Average over 64 readings.
        anykey = input("Place known weight on scale. Press a key when weight is in place and stable.\n")
        anykey = input("Please enter the weight, without units, currently sitting on the scale (for example '4.25'): \n")
        print("New cal factor: ")
        print(ws.getCalibrationFactor())
if __name__ == "__main__":
    
    ws = NAU7802()
    a = ws.begin()
    print(ws.available())
    ws.calibrateScale()
 
#    time.sleep(1)
#    print(ws.available())
#    time.sleep(1)
#    print(ws.available())
#    print(ws.calAFEStatus())
    while True:
        b = ws.getWeight(samples_to_take=2)
        print(b)
