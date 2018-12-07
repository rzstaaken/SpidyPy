# TrialPCA.py
# Servo motors driven by PCA9685 chip

from smbus import SMBus
from PCA9685 import PWM
import time
#Achse 0 min = 2, max = 6 Fuß
#Achse 1 min = 2, max = 9.5
#Achse 2 min = 2, max = 9
class Trial:
    fPWM = 50
    i2c_address = 0x40 # (standard) adapt to your module
    #channel = 0 # adapt to your wiring
    a = 8.5 # adapt to your servo
    b = 2   # adapt to your servo

    def __init__(self):
        global pwm
        bus = SMBus(1) # Raspberry Pi revision 2
        pwm = PWM(bus, self.i2c_address)
        pwm.setFreq(self.fPWM)

    def setDirection(self,direction,channel=0):
        duty = self.a / 180 * direction + self.b
        pwm.setDuty(channel, duty)
        print ("direction =", direction,"channel =",channel, "-> duty =", duty)
        time.sleep(0.1) # allow to settle

    def start(self,channel=0):  
        print ("starting")
        #setup()
        for direction in range(0, 181, 10):
            self.setDirection(direction,channel)
        direction = 0    
        self.setDirection(0,channel)    
        print ("done")
        
    def schritt(self,pos=2.0,channel=0):
        pwm.setDuty(channel, pos)
        #print("Hi")
        
if __name__ == "__main__":
    trial=Trial()
    trial.schritt(pos=5.0,channel=0)
    #trial.start(2)  
    print ("done")
