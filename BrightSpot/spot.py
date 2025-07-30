
from tqdm import tqdm
import time
import torch
import numpy as np
import matplotlib.pyplot as plt
from torch.fft import fft2, ifft2, fftshift, fftfreq

def transpose(matrix):
    transposed_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return transposed_matrix

def viewSweep(matrix, distances, xRange):
    n = len(matrix)
    
    fig, ax = plt.subplots()
    img = ax.imshow(matrix, cmap='hot', extent=[min(distances), max(distances), min(xRange), max(xRange)], aspect='auto')

    ax.set_xlabel('Distance (d)')
    ax.set_ylabel('Y coordinate (cm)')
    ax.set_title('Intensity Profile')

    cbar = plt.colorbar(img)
    fig.savefig("profile.png")
    plt.show()
    
def viewProfile(profile1, profile2, xRange, yRange):
    figure, axis = plt.subplots(1, 2, sharey=False)
    for ax in axis:
        ax.set_aspect('equal')
    axis[0].pcolormesh(xRange * 100, yRange * 100, torch.abs(profile1), cmap="hot")    
    axis[1].pcolormesh(xRange * 100, yRange * 100, torch.abs(profile2), cmap="hot")    

    # axis[1].set_xlim(-0.25, 0.25)
    # axis[1].set_ylim(-0.25, 0.25)

    axis[0].set_ylabel('Y coordinate (cm)')
    axis[0].set_xlabel('X coordinate (cm)')
    axis[1].set_xlabel('X coordinate (cm)')
    plt.savefig("spot.png", dpi=1200)
    plt.show()

def viewFourierSpace(profile, kxRange, kyRange):
    plt.figure(figsize=(5, 5))
    plt.pcolormesh(fftshift(kxRange), fftshift(kyRange), torch.abs(fftshift(profile)))
    plt.xlabel("K space X coordinate (1/m)")
    plt.ylabel("K space Y (1/m)")
    plt.savefig("fourier_space.png")
    plt.show()
    
def createGeometry(beamProfile, objectProfile):
    geometry = beamProfile & (~objectProfile)
    return geometry.to(torch.float)

def propagate(objectFourier, distance, k, kxRange, kyRange): 
    return ifft2(objectFourier * torch.exp(-1j * distance * torch.sqrt(k**2 - kxRange**2 - kyRange**2)))

#----------------------------------------------------------------------------------------------------------------

def run_simulation():
    # Problem Variables
    simulationRange = 12e-3
    samplingPoints = 2000

    distance = (250 - 100-10) * 1e-2
    wavelength = 532e-9
    kVectorValue = 2 * np.pi / wavelength

    # Geometry Variables
    beamWidth = 5e-2 / 2
    circleRadius = 8e-3
    squareSize = 8e-3 / 2
    hexagonApotema = 5e-3
    hexagonSide    = (2*hexagonApotema)/np.sqrt(3) 
    
    # Creates a symmetric area where the simulation will happen
    xSampling = np.linspace(-simulationRange, simulationRange, samplingPoints)
    xRange, yRange = np.meshgrid(xSampling, xSampling)

    # Creates the Fourier space grid
    kSampling = fftfreq(len(xSampling), np.diff(xSampling)[0]) * 2 * np.pi
    kxRange, kyRange = np.meshgrid(kSampling, kSampling)
    kxRange = torch.tensor(kxRange)
    kyRange = torch.tensor(kyRange)
    
    # Creates a circular beam profile using boolean variables
    beamProfile = (torch.sqrt(torch.tensor(xRange)**2 + torch.tensor(yRange)**2) < beamWidth)

    # Objects --------------------

    circleTruthTable = (torch.sqrt(torch.tensor(xRange)**2 + torch.tensor(yRange)**2) < circleRadius)
    circle = createGeometry(beamProfile, circleTruthTable)

    squareTruthTable = ((torch.abs(torch.tensor(xRange)) < squareSize) * (torch.abs(torch.tensor(yRange)) < squareSize))
    square = createGeometry(beamProfile, squareTruthTable)

    # hexagon
    # table = np.zeros(shape=(len(yRange),len(xRange))) 
    # hexagonTruthTable = torch.tensor(table, dtype=torch.bool)
    # for i in range(len(yRange)):
    #     for j in range(len(xRange)):
    #         px = np.abs(xRange[i, j])
    #         py = np.abs(yRange[i, j])
    #         p  = np.array([px, py])
    #         s  = np.array([1, np.sqrt(3)])
    #         value = (max(np.dot(p, s*0.5), px) - hexagonSide)
    #         if(value < 0):
    #             hexagonTruthTable[i, j] = True
    #         else:
    #             hexagonTruthTable[i, j] = False
    # hexagon = createGeometry(beamProfile, hexagonTruthTable)    
             
    # Objects ---------------------

    # Solves the propagation of the given profile
    currentObject = circle
    objectFourier = fft2(currentObject)  
    screenProfile = propagate(objectFourier, distance, kVectorValue, kxRange, kyRange)
 
    # Sweep anteparo ----------
    d_initial = 0 
    d_final   = (250 - 100-10)*1e-2
    samples = 10
    distance_sweep = np.linspace(d_initial, d_final, samples)
    xProfile = np.linspace(-1, 1, samples)

    # print(distance_sweep)
    #
    # intensityProfile_sweep = []
    # for i in tqdm(range(len(distance_sweep))):
    #     profile = torch.abs(propagate(objectFourier, distance_sweep[i], kVectorValue, kxRange, kyRange))
    #     mid     = len(profile)//2
    #     intensityProfile_sweep.append(profile[mid].tolist()) 
    #
    # intensityProfile_sweep = transpose(intensityProfile_sweep)
    # viewSweep(intensityProfile_sweep, distance_sweep, xProfile) 
    
    return currentObject, screenProfile, xRange, yRange, kxRange, kyRange

def main():
    start_time = time.time()
    currentObject, screenProfile, xRange, yRange, kxRange, kyRange = run_simulation() 
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds") 
    viewProfile(currentObject, screenProfile, xRange, yRange)
    # viewFourierSpace(screenProfile, kxRange, kyRange)

main()
