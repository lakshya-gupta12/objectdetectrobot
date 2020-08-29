# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import RPi.GPIO as GPIO
# Motor Control Functions:
def MotorInit(F,B,R,L,EN,_EN):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(F, GPIO.OUT)
    GPIO.setup(B, GPIO.OUT)
    GPIO.setup(R, GPIO.OUT)
    GPIO.setup(L, GPIO.OUT)
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(_EN, GPIO.OUT)
    FBspeed=GPIO.PWM(EN,1000)
    RLspeed=GPIO.PWM(_EN,1000)
    return FBspeed,RLspeed
def MotorFB(Dir,F,B):
    if Dir==0:
        GPIO.output(F,HIGH)
        GPIO.output(B,LOW)
    else:
        GPIO.output(F,LOW)
        GPIO.output(B,HIGH)
def MotorRL(Dir,R,L):
        if Dir==0:
            GPIO.output(R,HIGH)
            GPIO.output(L,LOW)
        else:
            GPIO.output(R,LOW)
            GPIO.output(L,HIGH)
def MotorCleanup(PIN,Pin):
    PIN.stop()
    Pin.stop()
    GPIO.cleanup()
# Motor Intilizing:
EN,_EN = MotorInit(29,31,33,35,36,38)
EN.ChangeDutyCycle(25) # forward moving speed
_EN.ChangeDutyCycle(75) # Right-Left Turn 3 second and 1 second forward to 120 deg.
# Tracking oject Function :
def TrackObject(label,BoundingBox):
    CameraArea=500*500
    ObjectArea=BoundingBox[0]*BoundingBox[1]
    print('Object area is :',ObjectArea)
    if ObjectArea<CameraArea*0.5:
        print('Moving Forward to track:',label)
    else:
        print('No need to track:threshold reached')
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
    help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
    help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.8,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
# initialize the video stream, allow the camera sensor to warm up,
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
fps = FPS().start()
# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=600)
    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (500, 500)),
        0.007843, (300, 300), 127.5)
    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()
    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]
        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx],
                confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            #print('Object detected is:',label)
            #print('Bounding Box:',box.astype("int"),'\n')
            Box=box.astype("int")
            print(Box)
            TrackObject(label,[Box[2]-Box[0],Box[3]-Box[1]])
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
# show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    # update the FPS counter
    fps.update()
# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
MotorCleanup(EN,_EN)