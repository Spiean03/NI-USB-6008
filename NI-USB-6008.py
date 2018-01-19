# -*- coding: utf-8 -*-
"""
This script allows to control analog (any value between 0 and 5V) and digital (0 or 5V) outputs of a NI-USB-6008 using the PyDAQmx module
Additional outputs can be added following the same model
"""
from __future__ import division 
from PyDAQmx import Task, DAQmx_Val_ChanPerLine, DAQmx_Val_Volts, DAQmx_Val_GroupByChannel
import numpy as np
from ctypes import *

'''
Pin List
- P1.0 : Digital/Bit Channel 1
- P1.1 : Digital/Bit Channel 2 

- AO 0 : Volt Channel 1
- AO 1 : Volt Channel 2
''' 

# Defining Numerical/Binary values for digital outputs
Num0 = np.array([0], dtype=np.uint8) #  0V
Num1 = np.array([1], dtype=np.uint8) # +5V

# Create 1 Task object/pin
List_Task  = [BitTask1,BitTask2,VTask1,VTask2] = [Task() for i in range(4)]
List_Bit   = [BitTask1,BitTask2]
List_Volt  = [VTask1, VTask2]

# Assign digital Pin ON/OFF 0/+5V
BitTask1.CreateDOChan("Dev1/port1/line0","BitTask1",DAQmx_Val_ChanPerLine)
BitTask2.CreateDOChan("Dev1/port1/line1","BitTask2",DAQmx_Val_ChanPerLine)

# Assign Analogue Pin for Voltage output
VTask1.CreateAOVoltageChan("Dev1/ao0","VTask1",0,5,DAQmx_Val_Volts,None)
VTask2.CreateAOVoltageChan("Dev1/ao1","VTask2",0,5,DAQmx_Val_Volts, None)

# Define Functions for digital ON/OFF and Analogue

def SetBitOn(MyBitTask):
    '''Apply 5V output to a digital pin corresponding to the given task'''
    MyBitTask.WriteDigitalLines(1,1,-1,DAQmx_Val_GroupByChannel,Num1,None,None)
    MyBitTask.StopTask() # Task must be stopped in order to be able to play with the other channels/tasks
    
def SetBitOff(MyBitTask):
    '''Apply 0V output to a digital pin corresponding to the given task'''    
    MyBitTask.WriteDigitalLines(1,1,-1,DAQmx_Val_GroupByChannel,Num0,None,None)
    MyBitTask.StopTask()


def Voltage(MyVTask,Percentage):
    '''Apply voltage (in % : 100% = 5V) to an analogue pin corresponding to the given task'''
    VoltOut = 5 * Percentage/100
    MyVTask.WriteAnalogScalarF64(1,-1,VoltOut,None)
    # Syntax : WriteAnalogScalarF64 (TaskHandle taskHandle, bool32 autoStart, float64 timeout, float64 value, bool32 *reserved);
    MyVTask.StopTask()


def Reset():
    '''Set all pin in List_Bit and List_Volt to 0V output'''
    for i in List_Bit:
        i.WriteDigitalLines(1,1,-1,DAQmx_Val_GroupByChannel,Num0,None,None) # switch off lasers
    
    for i in List_Volt:
        i.WriteAnalogScalarF64(1,-1,0,None)


def Quit():
    Reset() # 0V to all pins
    for i in List_Task:
        i.ClearTask() # free the hardware