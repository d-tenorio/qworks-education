# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 11:10:09 2019

Python 3.x
@authors: David Tenorio
"""

import pandas as pd
import folium # https://python-visualization.github.io/folium/

def importData(fname):    
    
    df = pd.read_csv(fname, sep='\t', header=0) #tab separated file    
    return df    

def makeMap(df):
    nrows, ncols = df.shape
    
    init_coord = [35.111135, -106.633373]
    
    m = folium.Map(
    location= init_coord,
    zoom_start=11   
    )
    
    for r in range(nrows):
        long = round(df.loc[r]["Long"],6)
        lat = round(df.loc[r]["Lat"],6)
        name =  df.loc[r]["School Name"]
        
        
        folium.Marker(
        location= [long,lat],
        popup= name,
        icon=folium.Icon(color="green",prefix="fa",icon='graduation-cap')
        ).add_to(m)

    m.save('index.html')
    
if __name__ == "__main__":
    
    fname = "data_schools.tsv"
    df = importData(fname)
    
    map_data = makeMap(df)
    

