import numpy as np
from PIL import Image #Image file handling
import pandas as pd
from modules.tracer import*

def triplet_system():
  df = pd.read_json("data/lenses.json") 

  obj = Image.open("img/nuevaImagen.png", "r")

  n1 = 1
  
  CHIEF_RAY = 0
  PARALLEL_RAY = 1

  m = '1'

  res = 40/63

  so = 1320

  f1 = df.loc['objective2','mainSystem']['f']
  f2 = df.loc['eyespace2','mainSystem']['f']

  si1 = [(f1[0]*so)/(so-f1[0]), (f1[1]*so)/(so-f1[1]), (f1[2]*so)/(so-f1[2])]
  so2 = [-(si1[0]-(f1[0]+f2[0])), -(si1[1]-(f1[1]+f2[1])), -(si1[2]-(f1[2]+f2[2]))]
  si2 = [(f2[0]*so2[0])/(so2[0]-f2[0]), (f2[1]*so2[1])/(so2[1]-f2[1]), (f2[2]*so2[2])/(so2[2]-f2[2])]

  print(si2)

  so = [18 + (11+13+11)/2 - si2[0], 18 + (11+13+11)/2 - si2[1], 18 + (11+13+11)/2 - si2[2]]

  f1 = df.loc['convergentLens','triplet']['f']
  f2 = df.loc['divergentLens','triplet']['f']
  f3 = df.loc['planarConvergentLens','triplet']['f']

  f = [1/((1/f1[0])+(1/f2[0])+(1/f3[0])), 1/((1/f1[1])+(1/f2[1])+(1/f3[1])), 1/((1/f1[2])+(1/f2[2])+(1/f3[2]))]

  si = [(f[0]*so[0])/(so[0]-f[0]), (f[1]*so[1])/(so[1]-f[1]), (f[2]*so[2])/(so[2]-f[2])]

  print(si)

  width, height = obj.size

  width_output = int(width)
  height_output = int(height)

  image = Image.new("RGB", (width_output, height_output), "white")

  pixels = image.load()

  #Compute the image with chief ray
  pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m)

  #Compute the cummulated image with parallel ray
  pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m)

  image.save('img/nuevaImagenAberracionCorregida.png', format='PNG')