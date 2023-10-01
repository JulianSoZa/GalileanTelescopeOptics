import cv2
import numpy as np
import matplotlib.pyplot as plt
from functions import*

# imagen
img = cv2.imread("img/nuevaImagen.png") # matriz principal

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib

R,G,B = cv2.split(img) # se extraen los canales

width_output = 252
height_output = 252

pixelsR, pixelsG, pixelsB = R, G, B

if (interpolate):
  pixelsR = interpolation(pixelsR, width_output, height_output)
  print ("Interpolation performed")
  pass

if (interpolate):
  pixelsG = interpolation(pixelsG, width_output, height_output)
  print ("Interpolation performed")
  pass

if (interpolate):
  pixelsB = interpolation(pixelsB, width_output, height_output)
  print ("Interpolation performed")
  pass

imgre = cv2.merge((pixelsB, pixelsG, pixelsR))

cv2.imwrite("img/nuevaImagenInterpolada.png", imgre)