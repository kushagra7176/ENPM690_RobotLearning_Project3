# -*- coding: utf-8 -*-
"""

Robot Learning Assignment 3

@author: kushagra
"""

import sys

from pynput.keyboard import Key, Listener

import vrep
from threading import Thread
from time import sleep

debug = False

Speed = 4

def threaded_function():
    while True:
        errorCode, detectionState1, detectedPoint1, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, front_left, vrep.simx_opmode_streaming)
        if debug:
            print (detectionState1)
        errorCode, detectionState2, detectedPoint2, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, front_right, vrep.simx_opmode_streaming)
        if debug:
            print (detectionState2)
        errorCode, detectionState3, detectedPoint3, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, sLeft, vrep.simx_opmode_streaming)
        if debug:
            print (detectionState3)
        errorCode, detectionState4, detectedPoint4, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, sRight, vrep.simx_opmode_streaming)
        if debug:
            print (detectionState4)
        print ("Front left Sensor Reading :{}\n".format(int(detectedPoint1[2]*100) if detectionState1 else "Nothing in Range"))
        print ("Front Right Sensor Reading :{}\n".format(int(detectedPoint2[2]*100) if detectionState2 else "Nothing in Range"))
        print ("Left Sensor Reading :{}\n".format(int(detectedPoint3[2]*100) if detectionState3 else "Nothing in Range"))
        print ("Right Sensor Reading :{}\n".format(int(detectedPoint4[2]*100) if detectionState4 else "Nothing in Range"))

        sleep(0.5)
        print ("______________________________________________")


def on_press(event):
    if event == Key.up:
        if debug:
            print ("UP")
        vrep.simxSetJointTargetVelocity(clientID, LeftMotor, Speed, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID, RightMotor, Speed, vrep.simx_opmode_streaming)
        print ('--------------------------------- Direction Straight')
    elif event == Key.right:
        if debug:
            print ("Right")
        vrep.simxSetJointTargetVelocity(clientID, LeftMotor, Speed, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID, RightMotor, -Speed, vrep.simx_opmode_streaming)
        print ('--------------------------------- Direction turn right')
    elif event == Key.left:
        if debug:
            print ("Left")
        vrep.simxSetJointTargetVelocity(clientID, RightMotor, Speed, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID, LeftMotor, -Speed, vrep.simx_opmode_streaming)
        print ('--------------------------------- Direction turn left')
    elif event == Key.down:
        if debug:
            print ("down")
        vrep.simxSetJointTargetVelocity(clientID, LeftMotor, -Speed, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID, RightMotor, -Speed, vrep.simx_opmode_streaming)
        print ('--------------------------------- Direction turn Back')


def on_release(key):
    if debug:
        print ("{} released".format(key))
    vrep.simxSetJointTargetVelocity(clientID, LeftMotor, 0, vrep.simx_opmode_streaming)
    vrep.simxSetJointTargetVelocity(clientID, RightMotor, 0, vrep.simx_opmode_streaming)


print ('Program started')
vrep.simxFinish(-1)  # just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to V-REP

if clientID != -1:
    print ('Connected to remote API server')

    errorCode, LeftMotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor", vrep.simx_opmode_oneshot_wait)
    print (errorCode)
    print (LeftMotor)
    errorCode, RightMotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", vrep.simx_opmode_oneshot_wait)
    print (errorCode)
    print (RightMotor)
    errorCode, front_left = vrep.simxGetObjectHandle(clientID, "Front_Left",vrep.simx_opmode_oneshot_wait)
    errorCode, front_right = vrep.simxGetObjectHandle(clientID, "Front_Right",vrep.simx_opmode_oneshot_wait)
    errorCode, sLeft = vrep.simxGetObjectHandle(clientID, "Left",vrep.simx_opmode_oneshot_wait)
    errorCode, sRight = vrep.simxGetObjectHandle(clientID, "Right",vrep.simx_opmode_oneshot_wait)
    thread = Thread(target=threaded_function)
    thread.start()
    #  Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
else:
    print ('Failed connecting to remote API server')
    sys.exit("Connection failed")
