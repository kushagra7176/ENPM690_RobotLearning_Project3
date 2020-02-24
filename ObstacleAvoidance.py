# -*- coding: utf-8 -*-
"""
Robot Learning Assignment 3

@author: kushagra
"""

import sys
import vrep
from time import sleep
from random import randint

debug = False

StopTurnProbability = 60
TurnProbability = 40
DirectionProbability = 50
Turning = False

LeftMotorSignal = 2
RightMotorSignal = 2

Speed = 2

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
    errorCode, front_right = vrep.simxGetObjectHandle(clientID, "Front_Left",vrep.simx_opmode_oneshot_wait)
    errorCode, sLeft = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_ultrasonicSensor2", vrep.simx_opmode_oneshot_wait)
    errorCode, sRight = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_ultrasonicSensor7",vrep.simx_opmode_oneshot_wait)
    while True:
        errorCode, detectionState1, detectedPoint1, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, front_left, vrep.simx_opmode_streaming)
        front_left_distance = int(100 * detectedPoint1[2])
        if front_left_distance == 0:
            front_left_distance = 100
        if debug:
            print (detectionState1)
        errorCode, detectionState2, detectedPoint2, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, front_right, vrep.simx_opmode_streaming)
        front_right_distance = int(100 * detectedPoint2[2])
        if front_right_distance == 0:
            front_right_distance = 100
        if debug:
            print (detectionState2)
        errorCode, detectionState3, detectedPoint3, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, sLeft, vrep.simx_opmode_streaming)
        side_left_distance = int(100 * detectedPoint3[2])
        if side_left_distance == 0:
            side_left_distance = 100
        if debug:
            print (detectionState3)
        errorCode, detectionState4, detectedPoint4, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, sRight, vrep.simx_opmode_streaming)
        side_right_distance = int(100 * detectedPoint4[2])
        if side_right_distance == 0:
            side_right_distance = 100
        if debug:
            print (detectionState4)
        print ("Front left Reading :{}\n".format(int(detectedPoint1[2] * 100) if detectionState1 else "Nothing in Range"))
        print ("Front Right Reading :{}\n".format(int(detectedPoint2[2] * 100) if detectionState2 else "Nothing in Range"))
        print ("Left Reading :{}\n".format(int(detectedPoint3[2] * 100) if detectionState3 else "Nothing in Range"))
        print ("Right Reading :{}\n".format(int(detectedPoint4[2] * 100) if detectionState4 else "Nothing in Range"))

        front_distance = (front_left_distance + front_right_distance) / 2
        if side_left_distance < 30:
            print ("---------------------------------- Side and front Turn right")
            LeftMotorSignal = Speed / 4
            RightMotorSignal = -Speed / 4
        elif side_right_distance < 30:
            print ("---------------------------------- Side and front Turn left")
            LeftMotorSignal = -Speed / 4
            RightMotorSignal = Speed / 4
        elif front_distance < 30:
            LeftMotorSignal = -Speed
            RightMotorSignal = -Speed
            sleep(1)
            print ("---------------------------------- Random Turn")
            if 50 > randint(0, 100):
                LeftMotorSignal = -Speed / 4
                RightMotorSignal = Speed / 4
            else:
                LeftMotorSignal = Speed / 4
                RightMotorSignal = -Speed / 4
        elif front_right_distance == 100:
            if 30 > randint(0, 100):
                if 50 > randint(0, 100):
                    print ("---------------------------------- Random Turn")
                    LeftMotorSignal = -Speed / 4
                    RightMotorSignal = Speed / 4
                else:
                    print ("---------------------------------- Random Turn")
                    LeftMotorSignal = Speed / 4
                    RightMotorSignal = -Speed / 4
            else:
                LeftMotorSignal = Speed
                RightMotorSignal = Speed
        else:
            LeftMotorSignal = Speed
            RightMotorSignal = Speed

        vrep.simxSetJointTargetVelocity(clientID, LeftMotor, LeftMotorSignal, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID, RightMotor, RightMotorSignal, vrep.simx_opmode_streaming)
        sleep(0.5)
        print ("______________________________________________")
else:
    print ('Failed connecting to remote API server')
    sys.exit("Connection failed")
