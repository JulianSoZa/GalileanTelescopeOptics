import numpy as np
import math
from PIL import Image #Image file handling
from scipy.interpolate import griddata #for image interpolation
from scipy import interpolate

def interpolation (pixels, width_output, height_output):

    arry = np.zeros((width_output, height_output))
    for i in range(width_output):
        for j in range(height_output):
            arry[i,j] = pixels[i,j][0]

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

    #Fill white pixels locations with interpolated values
    for i in range(int_out.shape[0]):
        pixels[white_coords[i,0], white_coords[i,1] ] = ( int_out[i], pixels[white_coords[i,0], white_coords[i,1] ][1], pixels[white_coords[i,0], white_coords[i,1] ][2])

    #Returne pixels array with interpolated values
    return pixels

def interpolationG (pixels, width_output, height_output):

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

def compute_lens_matrix(nl, R1, R2, dl):
    #A = np.array([[-0.00142039, 915.284], [-0.0012025, 70.8481]])
    AR = np.array([[1/70, 690], [0, 70]])
    AG = np.array([[0.0144265, 690], [0, 69.3168]])
    AB = np.array([[0.0148487, 690], [0, 67.3462]])
    
    A = np.array([[[1/70, 0.0144265, 0.0148487], [690, 690, 690]], [[0, 0, 0], [70, 69.3168, 67.3462]]])
    return A

#Ray tracing function with spherical aberration
def ray_tracing(width, height, rayo, so, n1, obj, res, nl, R1, R2, dl, aberration, pixels, width_output, height_output, si2, Mt):

    # Iterate over each pixel of the image
    for i in range(width):
        for j in range(height):

            # Get pixel value and calculate its position relative to the center of the image
            pos_x = i
            pos_y = j
            pixel = obj.getpixel((pos_x, pos_y))

            x = pos_x - width/2
            y = pos_y - height/2

            # Calculate the distance from the particular pixel to the center of the object (in pixels)
            r = math.sqrt( x*x + y*y ) + 1#Rounding correction

            #Input ray vector (point in the object plane)
            y_objeto = r*res # Conversion to real world coordinates
            #Corrected image distance for each point
            si = si2

            # Compute lens matrix using parameters nl, R1, R2, and dl
            A = compute_lens_matrix(nl, R1, R2, dl)

            # Define propagation matrices after and before the lens
            """P2 = np.array([[1,si/n1],[0,1]])
            P1 = np.array([[1,so/n1],[0,1]])"""
            
            P2 = np.array([[[1, 1, 1], [si/n1, si/n1, si/n1]],[[0, 0, 0], [1, 1, 1]]])
            P1 = np.array([[[1, 1, 1], [so/n1, so/n1, so/n1]],[[0, 0, 0], [1, 1, 1]]])

            if rayo == 0: #principal
                alpha_entrada = math.atan(y_objeto/so) #This ray enters towards the center of the lens
            elif rayo == 1: #parallel
                alpha_entrada = 0 #This ray enters parallel to the optical axis
            V_entrada = np.array([[y_objeto, y_objeto, y_objeto], [n1*alpha_entrada, n1*alpha_entrada, n1*alpha_entrada]])

            #Output ray vector calculation
            res1 = np.einsum('ikj,kj->ij', P1, V_entrada)
            res2 = np.einsum('ikj,kj->ij', A, res1)
            V_salida = np.einsum('ikj,kj->ij', P2, res2)

            #Transversal magnification
            y_imagen = V_salida[0]
            if rayo == 0: #principal
                #Mt = -y_imagen/y_objeto #atan correction
                Mt = [-y_imagen[0]/y_objeto, -y_imagen[1]/y_objeto, -y_imagen[2]/y_objeto]
            elif rayo == 1: #parallel
                #Mt = y_imagen/y_objeto
                Mt = [y_imagen[0]/y_objeto, y_imagen[1]/y_objeto, y_imagen[2]/y_objeto]

            #Conversion from image coordinates to lens coordinates
            """x_prime = Mt*x*(126/1.6)
            y_prime = Mt*y*(126/1.6)
            pos_x_prime = int(x_prime + width_output/2)
            pos_y_prime = int(y_prime + height_output/2)
            """
            x_prime = [x*(126/1.6)*Mt[0], x*(126/1.6)*Mt[1], x*(126/1.6)*Mt[2]]
            y_prime = [y*(126/1.6)*Mt[0], y*(126/1.6)*Mt[1], y*(126/1.6)*Mt[2]]
            pos_x_prime = [int(x_prime[0] + width_output/2), int(x_prime[1] + width_output/2), int(x_prime[2] + width_output/2)]
            pos_y_prime = [int(y_prime[0] + height_output/2), int(y_prime[1] + height_output/2), int(y_prime[2] + height_output/2)]
            
            if  pos_x_prime[0] < 0 or pos_x_prime[0] >= width_output:
                continue
            if  pos_x_prime[1] < 0 or pos_x_prime[1] >= width_output:
                continue
            if  pos_x_prime[2] < 0 or pos_x_prime[2] >= width_output:
                continue

            if  pos_y_prime[0] < 0 or pos_y_prime[0] >= height_output:
                continue
            if  pos_y_prime[1] < 0 or pos_y_prime[1] >= height_output:
                continue
            if  pos_y_prime[2] < 0 or pos_y_prime[2] >= height_output:
                continue

            if rayo == 0: #principal
                pixels[pos_x_prime[0], pos_y_prime[0]] = (pixel[0], pixel[1], pixel[2])
                pixels[pos_x_prime[1], pos_y_prime[1]] = (pixel[0], pixel[1], pixel[2])
                pixels[pos_x_prime[2], pos_y_prime[2]] = (pixel[0], pixel[1], pixel[2])
                next
            elif rayo == 1: #parallel
                """new_gray = (int(pixel) + pixels[pos_x_prime, pos_y_prime][0])/2
                pix_fin = ( int(new_gray), int(new_gray), int(new_gray) )
                pixels[pos_x_prime, pos_y_prime] = pix_fin"""
                new_gray = [(int(pixel[0]) + pixels[pos_x_prime[0], pos_y_prime[0]][0])/2, (int(pixel[1]) + pixels[pos_x_prime[1], pos_y_prime[1]][0])/2, (int(pixel[2]) + pixels[pos_x_prime[2], pos_y_prime[2]][0])/2]
                pix_fin = ( int(new_gray[0]), int(new_gray[1]), int(new_gray[2]) )
                pixels[pos_x_prime[0], pos_y_prime[0]] = (pix_fin[0], pixels[pos_x_prime[0], pos_y_prime[0]][1],pixels[pos_x_prime[0], pos_y_prime[0]][2])
                pixels[pos_x_prime[1], pos_y_prime[1]] = (pixels[pos_x_prime[1], pos_y_prime[1]][0], pix_fin[1], pixels[pos_x_prime[1], pos_y_prime[1]][2])
                pixels[pos_x_prime[2], pos_y_prime[2]] = (pixels[pos_x_prime[2], pos_y_prime[2]][0],pixels[pos_x_prime[2], pos_y_prime[2]][1], pix_fin[2])
    print(V_salida)
    print(V_entrada)
    return pixels
