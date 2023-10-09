import numpy as np
import math

def compute_lens_matrix():
    #A = np.array([[-0.00142039, 915.284], [-0.0012025, 70.8481]]) para lentes gruesas
    AR = np.array([[1/70, 690], [0, 70]])
    AG = np.array([[101/7001, 690], [0, 7001/101]])
    AB = np.array([[104/7004, 690], [0, 7004/104]])
    
    A = np.array([[[1/70, 101/7001, 104/7004], [690, 690, 690]], [[0, 0, 0], [70, 7001/101, 7004/104]]])
    
    return A

def triplet():
    T = np.array([[[0.95193, 0.951955, 0.952031], [22.6353, 22.635,  22.634]], [[-0.000748969, -0.000749235, -0.000750021], [1.03269, 1.03265, 1.03255]]])
    return T

def ray_tracing(width, height, rayo, so, n1, obj, res, pixels, width_output, height_output, si2, m):

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
            A = compute_lens_matrix()
            T = triplet()

            #Output ray vector calculation
            if(m == '0'):
                # Define propagation matrices after and before the lens
                P2 = np.array([[[1, 1, 1], [si[0]/n1, si[1]/n1, si[2]/n1]],[[0, 0, 0], [1, 1, 1]]])
                P1 = np.array([[[1, 1, 1], [so/n1, so/n1, so/n1]],[[0, 0, 0], [1, 1, 1]]])

                if rayo == 0: #principal
                    alpha_entrada = -math.atan(y_objeto/so) #This ray enters towards the center of the lens
                elif rayo == 1: #parallel
                    alpha_entrada = 0 #This ray enters parallel to the optical axis
                V_entrada = np.array([[y_objeto, y_objeto, y_objeto], [n1*alpha_entrada, n1*alpha_entrada, n1*alpha_entrada]])
            
                res1 = np.einsum('ikj,kj->ij', P1, V_entrada)
                res2 = np.einsum('ikj,kj->ij', A, res1)
                V_salida = np.einsum('ikj,kj->ij', P2, res2)
            elif(m == '1'):
                P2 = np.array([[[1, 1, 1], [si[0]/n1, si[1]/n1, si[2]/n1]],[[0, 0, 0], [1, 1, 1]]])
                P1 = np.array([[[1, 1, 1], [so[0]/n1, so[1]/n1, so[2]/n1]],[[0, 0, 0], [1, 1, 1]]])

                if rayo == 0: #principal
                    alpha_entrada = [-math.atan(y_objeto/so[0]), -math.atan(y_objeto/so[1]), -math.atan(y_objeto/so[2])]
                elif rayo == 1: #parallel
                    alpha_entrada = [0, 0, 0] #This ray enters parallel to the optical axis
                V_entrada = np.array([[y_objeto, y_objeto, y_objeto], [n1*alpha_entrada[0], n1*alpha_entrada[1], n1*alpha_entrada[2]]])
                
                res1 = np.einsum('ikj,kj->ij', P1, V_entrada)
                res2 = np.einsum('ikj,kj->ij', T, res1)
                V_salida = np.einsum('ikj,kj->ij', P2, res2)

            #Transversal magnification
            y_imagen = V_salida[0]

            Mt = y_imagen/y_objeto

            #Conversion from image coordinates to lens coordinates
            if(m == '0'):
                x_prime = x*(126/1.6)*Mt
                y_prime = y*(126/1.6)*Mt
            elif(m == '1'):
                x_prime = x*Mt
                y_prime = y*Mt
            
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
                pixels[pos_x_prime[0], pos_y_prime[0]] = (pixel[0], pixels[pos_x_prime[0], pos_y_prime[0]][1], pixels[pos_x_prime[0], pos_y_prime[0]][2])
                pixels[pos_x_prime[1], pos_y_prime[1]] = (pixels[pos_x_prime[1], pos_y_prime[1]][0], pixel[1], pixels[pos_x_prime[1], pos_y_prime[1]][2])
                pixels[pos_x_prime[2], pos_y_prime[2]] = (pixels[pos_x_prime[2], pos_y_prime[2]][0], pixels[pos_x_prime[2], pos_y_prime[2]][1], pixel[2])
    return pixels