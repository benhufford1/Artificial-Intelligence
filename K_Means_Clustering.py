#Problem Statement: use a k-means-clustering algorithm to group geographical data for earthquakes 

import numpy as np
import matplotlib.pyplot as plt
import math 
import random


quake_file = open ('earthquakes.txt', 'r')
quakes = [ ]
for line in quake_file:
    line = line.split()
    latitude = float(line[3])
    longitude = float(line[4])
    quakes.append((latitude,longitude))
    
def distance(pt1, pt2): 
    """takes in two tuples with two elements and computes euclidean distance 
    between them"""
    d = math.sqrt((pt1[0]-pt2[0])**2 +(pt1[1]-pt2[1])**2)
    return d

def init_centers(data, k): 
    """picks k random data points from the earthquake data to serve as initial 
    centers"""
    return random.sample(data, k) 

def new_centers(categories): 
    """given a set of categories (dictionary with each point assigned to a key 1,...,k),
    it calculates the average center of each cluster/category and returns the 
    new centers"""
    new_centers = []
    for key in categories: 
        number = len(categories[key])
        total_lat = 0
        total_long = 0 
        for element in categories[key]: 
            total_lat+=element[0]
            total_long+=element[1]
        new_centers.append(((total_lat/number),(total_long/number)))
    return new_centers
            
def assign_categories(data, centers): 
    """given a set of centers (tuples) and datapoints, it calculates which 
    center each datapoint is closet to and assign that point to the cluster around 
    that center. Returns a dictionary with keys = 1,...k and the values assigned 
    to those keys are the datapoints in that cluster."""
    categories = {}
    for i in range(len(centers)): 
        categories[i]=[]
    for i in data: 
        d = 1000
        for j in centers: 
            if distance(i,j)<=d: 
                d = distance(i,j)
                x = centers.index(j) 
        categories[x].append(i) 
    return categories, centers

def graph_kmeans(categories, centers): 
    """Graphs a scaterplot of the different categories and their centers"""
    zipped_categories = []
    for key in categories: 
        zipped_categories.append(list(zip(*categories[key])))
    for category in zipped_categories: 
        plt.scatter(category[0],category[1])
    zipped_centers = list(zip(*centers))
    plt.scatter(zipped_centers[0], zipped_centers[1], marker = 'x')

def largest_shift(old_centers, new_centers):
    """calculates the largest shift from one set of centers to a new set of 
    centers""" 
    greatest_distance = 0
    for i in range(len(old_centers)): 
        if distance(old_centers[i],new_centers[i])>greatest_distance: 
            greatest_distance = distance(old_centers[i],new_centers[i])
    return greatest_distance
        
def iter_kmeans(data, k, error_tol): 
    """Given k and an error tolerance, it randomely chooses k initial centers, 
    assigns each datapoint to a cluster, generates new centers, and repeats. 
    It repeats until the largest shift in a center is less than the given error 
    tolerance. It outputs the final categories and centers, and graphs them."""
    centers = init_centers(data, k)
    error = error_tol + 1
    while error>error_tol: 
        categories, old_centers = assign_categories(data, centers)
        graph_kmeans(categories, old_centers) 
        centers = new_centers(categories)
        error = largest_shift(old_centers, centers) 
        print(largest_shift(old_centers, centers))
    final_centers = new_centers(categories) 
    graph_kmeans(categories, final_centers) 
    return categories, final_centers

cats, cents = iter_kmeans(quakes, 4, 10**(-7))
