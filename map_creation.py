# -*- coding: utf-8 -*-
"""
Created on Sat Aug 3 11:10:09 2019

Python 3.x
@authors: David Tenorio

took inspiration from:
    https://codeburst.io/how-i-understood-displaying-interactive-maps-using-python-leaflet-js-and-folium-bd9b98c26e0e?gi=412697adb20b
    https://python-visualization.github.io/folium/quickstart.html#Getting-Started
"""

import pandas as pd
import folium #https://python-visualization.github.io/folium/
from geojson import Polygon, Feature, FeatureCollection, dump # 
import numpy as np

def importData(fname):    
    """imports a tsv, returns a pandas DataFrame"""
    df = pd.read_csv(fname, sep='\t', header=0) #tab separated file    
    return df    

def squareMaker(lat,long):
    """helper function to return a list of coordinates representing a square centered on 
        the two coordinates provided as inputs"""
    SIZE = .003 #make the square bigger or smaller by changing this
    return[
           (lat+SIZE,long+SIZE),
           (lat+SIZE,long-SIZE),
           (lat-SIZE,long-SIZE),
           (lat-SIZE,long+SIZE),
           (lat+SIZE,long+SIZE)
           ]

def makeMap(df_coords, df_data):
    """takes in a pandas DataFrame, uses folium to produce a map of the different schools"""
    nrows, ncols = df_coords.shape
    
    init_coord = [35.111135, -106.633373] #starting coordinates, just about in the middle
    
    m = folium.Map(
    location= init_coord,
    zoom_start=11
    )
    
    #get sample data
    grad_data = []
    names_orig = df_coords.School.unique()
    all_schools = df_data.school.unique()
    
    
    for i,name in enumerate(names_orig):
        if name in all_schools:
            #sample data: All Students, 2018
            datum = df_data.loc[(df_data['school'] == name) & (df_data['group'] == 'All Students') & (df_data['Cohort'] == 2018)]['rate']
            grad_data.append(float(datum)) #convert, add it
        else:
            grad_data.append(np.NaN)
            
    df_coords["Data"] = grad_data
    
    features = [] #for geoJSON data
    
    #go through each school
    for r in range(nrows):
        #get the coordinates and name
        long = round(df_coords.loc[r]["Long"],6)
        lat = round(df_coords.loc[r]["Lat"],6)
        name =  df_coords.loc[r]["School"]
        val = df_coords.loc[r]["Data"]
        
        #skip schools we have no data for
        if np.isnan(val):
            continue
        
        #use geoJSON to create a square centered around each school
        coords = squareMaker(lat,long) #for geoJSON, use the order lat, long
        poly = Polygon([coords])
        
        features.append(Feature(geometry=poly, id= name))
        
        ttip = name + ': ' + str(val) + '%'
        
        #make a marker for each school using folium
        folium.Marker(
        location= [long,lat], #for folium, use the order long,lat
        tooltip= ttip,
        icon=folium.Icon(color="green",prefix="fa",icon='graduation-cap')
        ).add_to(m)
        
    #save the geojson file locally
    feature_collection = FeatureCollection(features)
    with open('myfile.geojson', 'w') as f:
        dump(feature_collection, f)
    f.close()
    
    #creating the choropleth map, which is a map based on a data value
    folium.Choropleth(
    #geo_data= 'other.json',
    geo_data= feature_collection,
    name='choropleth',
    data=df_coords,
    columns=["School", "Data"], #label, then value
    key_on='feature.id',
    fill_color='BuPu', #change the colors here - uses color brewer (http://colorbrewer2.org/) sequential palettes
    fill_opacity=0.7,
    line_opacity=0.9,
    legend_name='2018 Cohort Graduation Data by School for All Students',
    highlight=True
    ).add_to(m)
    
    folium.TileLayer(tiles='Stamen Terrain',name="Terrain").add_to(m)
    folium.LayerControl().add_to(m)
    
    #save the map to an html file
    m.save('index.html')
    
    
if __name__ == "__main__":
    #coordinates for each school if interest
    fname_coords = "name_coordinates.tsv"
    df_coords = importData(fname_coords)
    
    #actual grad data for every NM school
    fname_data = "grad_data_per_school.txt"
    df_data = importData(fname_data) 


    makeMap(df_coords,df_data)