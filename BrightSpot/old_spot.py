# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 21:58:41 2023

@author: User
"""

import time

import torch 

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from torch.fft import fft2
from torch.fft import ifft2
from torch.fft import fftfreq
from torch.fft import fftshift
from torch.fft import fftfreq

from numba import jit, complex128, float64

def viewProfile(profile1, profile2, xRange, yRange):       
    figure, axis = plt.subplots(1, 2,sharey=True) 
    for ax in axis:
        ax.set_aspect('equal')
    axis[0].pcolormesh(xRange*100,yRange*100,np.abs(profile1), cmap = "hot")
    axis[1].pcolormesh(xRange*100,yRange*100,np.abs(profile2), cmap = "hot")
     
    axis[0].set_ylabel('Y coordinate (cm)')
    axis[0].set_xlabel('X coordinate (cm)')
    axis[1].set_xlabel('X coordinate (cm)')

    plt.show()
    
def viewFourierSpace(profile):                       #function to visualize profiles
    plt.figure(figsize = (5,5))
    plt.pcolormesh(fftshift(kxRange),fftshift(kyRange),np.abs(fftshift(profile)))
    plt.xlabel("K space X coordinate (1/m)")
    plt.ylabel("K space Y (1/m)")
    plt.show()
    
def createGeometry(beamProfile, objectProfile): #create the final geometry based on the blocking object
    geometry = beamProfile & (~objectProfile)
    return geometry.astype(float)

def propagate(objectFourier,distance, k, kxRange, kyRange):
    return ifft2(objectFourier * np.exp(-1j * distance * np.sqrt(k**2 - kxRange**2 - kyRange**2)))

def main():
    start_time = time.time()
    
    #Problem Variables
    simulationRange = 12e-3
    samplingPoints  = 4000

    distance        = (75.6-48)*1e-2
    wavelenght      = 532e-9
    kVectorValue    = 2 * np.pi / wavelenght

    #Geometry Variables
    beamWidth       = 15e-3/2
    circleRadius    = 4.72e-3
    squareSize      = 8e-3 / 2

    #Creates a symmetric area where the simulation will happen
    xSampling = np.linspace(-simulationRange,simulationRange,samplingPoints)
    xRange, yRange = np.meshgrid(xSampling,xSampling)

    #Creates the fourier space grid
    kSampling        = fftfreq(len(xSampling), np.diff(xSampling)[0]) * 2 *np.pi
    kxRange, kyRange = np.meshgrid(kSampling,kSampling)

    #creates a circular beam profile using boolean variables
    beamProfile  = (np.sqrt( xRange**2 + yRange**2) < beamWidth)

    circleTruthTable = (np.sqrt( xRange**2 + yRange**2) < circleRadius)
    circle = createGeometry(beamProfile, circleTruthTable)

    squareTruthTable   = ((abs(xRange) < squareSize) * (abs(yRange) < squareSize ))
    square = createGeometry(beamProfile, squareTruthTable)

    #Solves the propagation of the given profile
    currentObject = circle
    objectFourier = fft2(torch.from_numpy(currentObject))
    screenProfile = propagate(objectFourier, distance, kVectorValue, kxRange, kyRange)
    
    end_time = time.time()
    delta = end_time - start_time
    print(delta)

    viewProfile(currentObject,screenProfile, xRange, yRange)

main()
