import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from mpl_point_clicker import clicker 
import matplotlib.image as mpimg

import re
import os
import csv
import shlex
import subprocess
import itertools

#------------------------------------------------------

img_path = "data/image.jpeg"

def write_points_to_csv(points, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile) 
        # Write each point to the CSV file
        for point in points:
            csv_writer.writerow(point)

def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def generate_all_edges(points):
    all_combinations = itertools.combinations(points, 2)
    edges = [(p1, p2, euclidean_distance(p1, p2)) for p1, p2 in all_combinations]
    return edges

#-------------------------------------------------------

def plot_edges(terminals, steiner_points, edges):
    plt.figure(figsize=(8, 6)) 
    img = mpimg.imread("../"+img_path)
    plt.imshow(img)

    for edge in edges:
        point1, point2, _ = edge
        plt.plot([point1[0], point2[0]], [point1[1], point2[1]], color='black', linestyle='-', linewidth=1)
 
    if(len(terminals) > 0):
        x_terms, y_terms = zip(*terminals)
        plt.scatter(x_terms, y_terms, color='red', label='Terminals')
    
    if(len(steiner_points) > 0):
        x_coords, y_coords = zip(*steiner_points) 
        plt.scatter(x_coords, y_coords, color='blue', label='Steiner Points')    
        
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.savefig("../Steiner_tree.png", dpi=1200)
    plt.show()
    
def minimum_spanning_tree(graph_edges):
    G = nx.Graph()
    for edge in graph_edges:
        G.add_edge(edge[0], edge[1], weight = edge[2]) 
    mst_edges = nx.minimum_spanning_edges(G, algorithm='kruskal')
    return list(mst_edges)

def euclidean_steiner_tree(terminals, steiner_points):
    complete_G = generate_all_edges(terminals+steiner_points)
    mst        = minimum_spanning_tree(complete_G) 
    plot_edges(terminals, steiner_points, mst)

def run_geosteiner():
    os.chdir("geosteiner-5.3")
    
    subprocess.call(shlex.split("make demo1"))
    result = subprocess.run(['./demo1'], stdout=subprocess.PIPE) 
    geosteiner_output = result.stdout.decode('utf-8')

    pattern_x = r'\[([^]]*)\]' 
    matches_x = re.findall(pattern_x, geosteiner_output)
   
    pattern_y = r'\{(.*?)\}'
    matches_y = re.findall(pattern_y, geosteiner_output)
    
    terminals = []
    for i in range(len(matches_x)):
        x = float(matches_x[i])
        y = float(matches_y[i])
        terminals.append((x,y)) 
    
    return terminals

def main():
    # Click as input
    fig, ax = plt.subplots(constrained_layout=True, figsize=(8,6)) 
    klicker = clicker(ax, ["event"], markers=["o"], colors=['r'])
    img = mpimg.imread(img_path)
    ax.imshow(img)
    fig.savefig("input_img.png", dpi=1200)
    plt.show()
    
    terminals = klicker.get_positions()['event']
    terminals = [tuple(pt) for pt in terminals]
    write_points_to_csv(terminals, "points.csv")
    
    steiner_points = run_geosteiner() 
    euclidean_steiner_tree(terminals, steiner_points)
    
main()

