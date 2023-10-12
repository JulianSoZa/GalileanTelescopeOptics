from PIL import Image #Image file handling
import pandas as pd
import numpy as np
from modules.tracer import *

def main_system(m):
    df = pd.read_json("data/lenses.json") 
    if m == '0':
        obj = Image.open("img/mars.jpg", "r")
    else:
        obj = Image.open("img/nuevaImagen.png", "r")

    n1 = 1
    
    CHIEF_RAY = 0
    PARALLEL_RAY = 1

    res = 40/63

 
    so = 1320
    
    if m=='0':
        f1 = np.array(df.loc['objective2','mainSystem']['f'])
        f2 = np.array(df.loc['eyespace2','mainSystem']['f'])
        f3 = 0
        si1 = (f1*so)/(so-f1)
        so2 = -(si1-(f1+f2))
        si2 = (f2*so2)/(so2-f2)
        si = si2

    else:
        f1 = np.array(df.loc['objective2','mainSystem']['f'])
        f2 = np.array(df.loc['eyespace2','mainSystem']['f'])

        si1 = (f1*so)/(so-f1)
        so2 = -(si1-(f1+f2))
        si2 = (f2*so2)/(so2-f2)
    
        print(si2)
    
        d1 = df.loc['convergentLens','triplet']['d']
        d2 = df.loc['divergentLens','triplet']['d']
        d3 = df.loc['planarConvergentLens','triplet']['d']

        so = 18*2 + (d1+d2+d3)/2 - si2

        f1 = np.array(df.loc['convergentLens','triplet']['f'])
        f2 = np.array(df.loc['divergentLens','triplet']['f'])
        f3 = np.array(df.loc['planarConvergentLens','triplet']['f'])

        f = 1/((1/f1)+(1/f2)+(1/f3))

        si = (f*so)/(so-f)

    width, height = obj.size

    width_output = int(width)
    height_output = int(height)

    image = Image.new("RGB", (width_output, height_output), "white")

    pixels = image.load()

    
    if m=='1':
        #Compute the cummulated image with parallel ray
        pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, f1, f2, f3)
        pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, f1, f2, f3)    
        image.save('img/nuevaImagenAberracionCorregida.png', format='PNG')
    else:
        #Compute the cummulated image with parallel ray
        pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, f1, f2, f3)
        pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, f1, f2, f3)    
        image.save('img/nuevaImagen.png', format='PNG') 