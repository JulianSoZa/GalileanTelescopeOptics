from PIL import Image #Image file handling
import pandas as pd
import numpy as np
from packages.tracer import*

def main_system():
    df = pd.read_json("lenses.json") 
    obj = Image.open("img/mars.jpg", "r")

    n1 = 1
    
    CHIEF_RAY = 0
    PARALLEL_RAY = 1

    res = 40/63

    m = '0'

    so = 1320

    f1 = df.loc['objective2','mainSystem']['f']
    f2 = df.loc['eyespace2','mainSystem']['f']

    si1 = [(f1[0]*so)/(so-f1[0]), (f1[1]*so)/(so-f1[1]), (f1[2]*so)/(so-f1[2])]
    so2 = [-(si1[0]-(f1[0]+f2[0])), -(si1[1]-(f1[1]+f2[1])), -(si1[2]-(f1[2]+f2[2]))]
    si2 = [(f2[0]*so2[0])/(so2[0]-f2[0]), (f2[1]*so2[1])/(so2[1]-f2[1]), (f2[2]*so2[2])/(so2[2]-f2[2])]

    print(si2)

    width, height = obj.size

    width_output = int(width)
    height_output = int(height)

    image = Image.new("RGB", (width_output, height_output), "white")

    pixels = image.load()

    #Compute the image with chief ray
    pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si2, m)

    #Compute the cummulated image with parallel ray
    pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si2, m)

    image.save('img/nuevaImagen.png', format='PNG')