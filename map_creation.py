# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 11:10:09 2019

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
    
    df = pd.read_csv(fname, sep='\t', header=0) #tab separated file    
    return df    

def squareMaker(long,lat):
    size = 1
    return[
           (long+size,lat+size),
           (long-size,lat+size),
           (long-size,lat-size),
           (long+size,lat-size),
           (long+size,lat+size)
           ]

def makeMap(df):
    nrows, ncols = df.shape
    
    init_coord = [35.111135, -106.633373]
    
    m = folium.Map(
    location= init_coord,
    zoom_start=11
    )
    
    dummy = []
    for x in range(35):
        dummy.append(random.randint(1,100))
    
    #df["dummy_data"] = dummy
    df["dummy_data"] = range(35)
    
    features = [] #for geoJSON data
    
    for r in range(nrows):
        long = round(df.loc[r]["Long"],6)
        lat = round(df.loc[r]["Lat"],6)
        name =  df.loc[r]["School Name"]
        
        
        coords = squareMaker(long,lat)
        poly = Polygon([coords])
        print(poly)
        features.append(Feature(geometry=poly, id= name))
        
        
        folium.Marker(
        location= [long,lat],
        popup= name,
        icon=folium.Icon(color="green",prefix="fa",icon='graduation-cap')
        ).add_to(m)
        
    
    feature_collection = FeatureCollection(features)
    with open('myfile.geojson', 'w') as f:
        dump(feature_collection, f)
    f.close()
    
    #creating the heat map
    folium.Choropleth(
    #geo_data= 'other.json',
    geo_data= feature_collection,
    name='choropleth',
    
    key_on='feature.id',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.9,
    legend_name='Dummy Data',
    highlight=True
    ).add_to(m)
    
    #folium.TileLayer(tiles='Stamen Terrain',name="Terrain").add_to(m)
    folium.LayerControl().add_to(m)
    
    m.save('index2.html')
    
    
if __name__ == "__main__":
    
    fname = "data_schools.tsv"
    df = importData(fname)
    
    makeMap(df)

    

