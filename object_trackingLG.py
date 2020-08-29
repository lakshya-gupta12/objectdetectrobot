import RPi.GPIO as GPIO
import time
import numpy as np
Choice=[0,1]
# Servo Intiliatios:

def ServoInit(PIN,Freq):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)
    Servo=GPIO.PWM(PIN,Freq)
    return Servo
def ServoTurnRight(PIN,Freq):
    Pulse=(1/Freq)*100 +(Freq/((1/Freq)*100))
    PIN.ChangeDutyCycle(Pulse)
def ServoTurnLeft(PIN,Freq):
    Pulse=(1/Freq)*100 -(Freq/((1/Freq)*100))
    PIN.ChangeDutyCycle(Pulse)    
# if np.random.choice(Choice)==1:
#     ServoTurnRight(PIN,Freq)
# else:
#     ServoTurnLeft(PIN,Freq)
def ServoCleanup(PIN):
    PIN.stop()
    GPIO.cleanup()
Servo=ServoInit(12,1000)
def objtrack(x1,y1,x2,y2):
    width = x2-x1
    height = y2-y1
    found_area = width * height
    center_x = x + (width / 2)
    center_y = y + (height / 2)
    if found_area > 0:
        rect_location = [found_area,center_x,center_y]
    else:
        rect_location = None
    if rect_location:
        if rect_location[1] > (center_x + (width/3)):
                ServoTurnRight(Servo,25): 
                print("Turning right")
        elif rect_location[1] < (center_x - (width/3)):
                ServoTurnLeft(Servo,75)
                print("Turning left")
        else:
                #motor going forward 
                print("Forward")
    else:
        #add keep searching
        print("Target not found, searching")
	