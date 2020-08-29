import RPi.GPIO as GPIO
import time
import numpy as np

def MotorInit(F,B,R,L,EN,_EN):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(F, GPIO.OUT)
    GPIO.setup(B, GPIO.OUT)
    GPIO.setup(R, GPIO.OUT)
    GPIO.setup(L, GPIO.OUT)
    FBspeed=GPIO.PWM(EN,1000)
    RLspeed=GPIO.PWM(_EN,1000)
    return FBspeed,RLspeed
def MotorFB(Dir,F,B):
    if Dir==0:
		Atime=time.time()
		while time.time()-Atime<1:
			GPIO.output(F,HIGH)
			GPIO.output(B,LOW)
		GPIO.output(F,LOW)
		GPIO.output(B,LOW)
    else:
		Atime=time.time()
		while time.time()-Atime<1:
			GPIO.output(F,LOW)
			GPIO.output(B,HIGH)
		GPIO.output(F,LOW)
		GPIO.output(B,LOW)
def MotorRL(Dir,R,L):
        if Dir==0:
			Atime=time.time()
			while time.time()-Atime<1:
				GPIO.output(R,HIGH)
				GPIO.output(L,LOW)
			GPIO.output(R,LOW)
			GPIO.output(L,LOW)
        else:
			Atime=time.time()
			while time.time()-Atime<1:
				GPIO.output(R,LOW)
				GPIO.output(L,HIGH)
			GPIO.output(R,LOW)
			GPIO.output(L,LOW)
def MotorCleanup(PIN,Pin):
    PIN.stop()
    Pin.stop()
    GPIO.cleanup()
