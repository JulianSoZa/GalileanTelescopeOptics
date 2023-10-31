from PIL import Image #Image file handling
import pandas as pd
import numpy as np
from modules.tracer import *

def telescope_system(m, l, url):
    df = pd.read_json("data/lenses.json") 
    
    if m == '0':
        obj = Image.open(url, "r")
    elif m == '1':
        obj = Image.open("img/nuevaImagen.png", "r")
        
    width, height = obj.size

    n1 = 1
    
    CHIEF_RAY = 0
    PARALLEL_RAY = 1

    so = df.loc['mars','object']['so']
    do = df.loc['mars','object']['do']
    dio = df.loc['objective2','mainSystem']['di']
    
    res = dio/height
    
    f1 = np.array(df.loc['objective2','mainSystem']['f'])
    f2 = np.array(df.loc['eyespace2','mainSystem']['f'])
    
    si1 = (f1*so)/(so-f1)
    so2 = -(si1-(f1+f2))
    si2 = (f2*so2)/(so2-f2)
    
    print("si2: ", si2)
    
    if m == '0':
        
        f3 = 0
        si = si2

    elif m == '1':
    
        d1 = df.loc['convergentLens','triplet']['d']
        d2 = df.loc['divergentLens','triplet']['d']
        d3 = df.loc['planarConvergentLens','triplet']['d']

        so = 18*2 + (d1+d2+d3)/2 - si2

        f1 = np.array(df.loc['convergentLens','triplet']['f'])
        f2 = np.array(df.loc['divergentLens','triplet']['f'])
        f3 = np.array(df.loc['planarConvergentLens','triplet']['f'])

        f = 1/((1/f1)+(1/f2)+(1/f3))

        si = (f*so)/(so-f)
        print("so: ", so)
        print("si: ", si)

    width_output = int(width)
    height_output = int(height)

    image = Image.new("RGB", (width_output, height_output), "white")

    pixels = image.load()

    if m == '0':
        #Compute the cummulated image with parallel ray
        pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)
        pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)    
        image.save('img/nuevaImagen.png', format='PNG')
        
    elif m == '1':
        #Compute the cummulated image with parallel ray
        pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)
        pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)    
        image.save('img/nuevaImagenAberracionCorregida.png', format='PNG')