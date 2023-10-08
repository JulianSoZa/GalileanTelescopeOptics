import cv2
import numpy as np
from scipy.interpolate import griddata #for image interpolation
import pandas as pd

def interpolation(pixels, width_output, height_output):
  arry = np.zeros((width_output, height_output))
  for i in range(width_output):
      for j in range(height_output):
          arry[i,j] = pixels[i,j]

  # Get the coordinates of the non-white pixels
  nonwhite_coords = np.argwhere(arry != 255)
  # Get the coordinates of the white pixels
  white_coords = np.argwhere(arry == 255)

  # Get the pixel values of the non-white pixels
  nonwhite_pixels = arry[nonwhite_coords[:,0], nonwhite_coords[:,1]]

  # Interpolate the pixel values of the white pixels
  interpolated_pixels = griddata(nonwhite_coords, nonwhite_pixels, white_coords, method='linear', rescale=True)

  #Change resulting NaN values with some value (zero, for instance)
  interpolated_pixels = np.nan_to_num(interpolated_pixels, nan=127.0)

  #Round interpolated values to integers
  int_out = np.round(interpolated_pixels).astype(int)
  print(int_out.shape[0])
  #Fill white pixels locations with interpolated values
  for i in range(int_out.shape[0]):
      pixels[white_coords[i,0], white_coords[i,1] ] = int_out[i]

  #Returne pixels array with interpolated values
  return pixels


def interpolation_system(imgName, m):
  images = pd.read_json("data/images.json")
  # imagen
  img = cv2.imread(images[imgName[m-1]]['url']) # matriz principal

  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib

  R,G,B = cv2.split(img) # se extraen los canales

  width_output = 252
  height_output = 252

  pixelsR, pixelsG, pixelsB = R, G, B
  
  interpolate = True

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

  cv2.imwrite(images[imgName[m+1]]['url'], imgre)