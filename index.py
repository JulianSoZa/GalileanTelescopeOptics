import numpy as np
from PIL import Image #Image file handling
from scipy.interpolate import griddata #for image interpolation
from scipy import interpolate
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from functions import*

df = pd.read_json("lenses.json") 

obj = Image.open("img/mars.jpg", "r")

n1 = 1
nl = 1
R1 = 1
R2 = 2
dl = 1
 
CHIEF_RAY = 0
PARALLEL_RAY = 1

res = 40/63

so = 1320

f1 = df.loc['objective','mainSystem']['f']
f2 = df.loc['eyespace','mainSystem']['f']

si1 = (f1*so)/(so-f1)
so2 = si1-(f1-f2)
si2 = (f2*si1)/(si1-f2)

Mt = (-si1/so)*(si2/so2)

width, height = obj.size
width_output = int(width*(abs(Mt)*res))
height_output = int(height*(abs(Mt)*res))

width_output = int(width)
height_output = int(height)

image = Image.new("RGB", (width_output, height_output), "white")

pixels = image.load()

#Interpolation ?
interpolate = False

#Compute the image with chief ray
#pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, nl, R1, R2, dl, aberration, pixels, width_output, height_output, si2, Mt)

#Compute the cummulated image with parallel ray
pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, nl, R1, R2, dl, pixels, width_output, height_output, si2, Mt)

#Interpolating
if (interpolate):
  pixels = interpolation(pixels, width_output, height_output)
  print ("Interpolation performed")
  pass

image.save('img/nuevaImagen.png', format='PNG')