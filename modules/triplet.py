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

  print(si)

  width, height = obj.size

  width_output = int(width)
  height_output = int(height)

  image = Image.new("RGB", (width_output, height_output), "white")

  pixels = image.load()

  #Compute the image with chief ray
  pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, f1, f2, f3)

  #Compute the cummulated image with parallel ray
  pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, f1, f2, f3)

  image.save('img/nuevaImagenAberracionCorregida.png', format='PNG')