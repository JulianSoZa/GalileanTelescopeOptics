from PIL import Image #Image file handling
import pandas as pd
import numpy as np
from modules.tracer import*

def main_system():
    df = pd.read_json("data/lenses.json") 
    obj = Image.open("img/mars.jpg", "r")

    n1 = 1
    
    CHIEF_RAY = 0
    PARALLEL_RAY = 1

    res = 40/63

    m = '0'

    so = 1320

    f1 = np.array(df.loc['objective2','mainSystem']['f'])
    f2 = np.array(df.loc['eyespace2','mainSystem']['f'])
    f3 = 0

    si1 = (f1*so)/(so-f1)
    so2 = -(si1-(f1+f2))
    si2 = (f2*so2)/(so2-f2)

    print(si2)

    width, height = obj.size

    width_output = int(width)
    height_output = int(height)

    image = Image.new("RGB", (width_output, height_output), "white")

    pixels = image.load()

    #Compute the image with chief ray
    pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si2, m, f1, f2, f3)

    #Compute the cummulated image with parallel ray
    #pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si2, m, f1, f2, f3)

    image.save('img/nuevaImagen.png', format='PNG')