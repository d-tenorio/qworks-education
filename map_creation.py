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
import random
from geojson import Polygon, Feature, FeatureCollection, dump # 

def importData(fname):    
    """imports a tsv, returns a pandas DataFrame"""
    df = pd.read_csv(fname, sep='\t', header=0) #tab separated file    
    return df    

def squareMaker(lat,long):
    """helper function to return a list of coordinates representing a square centered on 
        the two coordinates provided as inputs"""
    SIZE = .002 #make the square bigger or smaller by changing this
    return[
           (lat+SIZE,long+SIZE),
           (lat+SIZE,long-SIZE),
           (lat-SIZE,long-SIZE),
           (lat-SIZE,long+SIZE),
           (lat+SIZE,long+SIZE)
           ]

def makeMap(df):
    """takes in a pandas DataFrame, uses folium to produce a map of the different schools"""
    nrows, ncols = df.shape
    
    init_coord = [35.111135, -106.633373]
    
    m = folium.Map(
    location= init_coord,
    zoom_start=11
    )
    
    #for now, make some dummy data to show that we can plot data when we have it
    dummy = []
    for x in range(35):
        dummy.append(random.randint(1,100))
    
    df["dummy_data"] = dummy
    #df["dummy_data"] = range(35)
    
    features = [] #for geoJSON data
    
    #go through each school
    for r in range(nrows):
        #get the coordinates and name
        long = round(df.loc[r]["Long"],6)
        lat = round(df.loc[r]["Lat"],6)
        name =  df.loc[r]["School Name"]
        
        #use geoJSON to create a square centered around each school
        coords = squareMaker(lat,long) #for geoJSON, use the order lat, long
        poly = Polygon([coords])
        
        
        features.append(Feature(geometry=poly, id= name))
        
        #make a marker for each school using folium
        folium.Marker(
        location= [long,lat], #for folium, use the order long,lat
        popup= name,
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
    data=df,
    columns=["School Name", "dummy_data"],
    key_on='feature.id',
    fill_color='BuPu', #change the colors here - uses color brewer (http://colorbrewer2.org/) sequential palettes
    fill_opacity=0.7,
    line_opacity=0.9,
    legend_name='Dummy Data',
    highlight=True
    ).add_to(m)
    
    #folium.TileLayer(tiles='Stamen Terrain',name="Terrain").add_to(m)
    folium.LayerControl().add_to(m)
    
    #save the map to an html file
    m.save('index.html')
    
    
if __name__ == "__main__":
    
    fname = "data_schools.tsv"
    df = importData(fname)
    
    makeMap(df)

    

