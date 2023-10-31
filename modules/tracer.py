import numpy as np
import math
import pandas as pd

def compute_lens_matrix(l):
    df = pd.read_json("data/lenses.json")
    
    if l == 'd':
        #------------------- Sistema de lentes delgadas -------------
        f1 = np.array(df.loc['objective2','mainSystem']['f'])
        f2 = np.array(df.loc['eyespace2','mainSystem']['f'])
        
        d = f1 + f2
        A = np.array([[-f2/f1, d], [[0, 0, 0], -f1/f2]])
        
    elif l == 'g':
        # ------------------ Sistema de lentes gruesas --------------
        
        nA = np.array(df.loc['objective2','mainSystem']['n'])
        rA = np.array(df.loc['objective2','mainSystem']['R'])
        dA = np.array(df.loc['objective2','mainSystem']['d'])
        nB = np.array(df.loc['eyespace2','mainSystem']['n'])
        rB = np.array(df.loc['eyespace2','mainSystem']['R'])
        dB = np.array(df.loc['eyespace2','mainSystem']['d'])
        
        fA = 1/((nA-1)*((1/rA)-(1/(-rA))+(((nA-1)*dA)/(nA*rA*(-rA)))))
        fB = 1/((nB-1)*((1/(-rB))-(1/(rB))+(((nB-1)*dB)/(nB*rB*(-rB)))))
        
        A = []
        for i in range(3):
            R5 = np.array([[1, 0] , [(nB[i]-1)/(rB), 1]])
            T56 = np.array([[1, dB/nB[i]] , [0, 1]])
            R6 = np.array([[1, 0] , [(1-nB[i])/(-rB), 1]])
            T67 = np.array([[1, fA[i] + fB[i]] , [0, 1]])
            R7 = np.array([[1, 0] , [(nA[i]-1)/(-rA), 1]])
            T78 = np.array([[1, dA/nA[i]] , [0, 1]])
            R8 = np.array([[1, 0] , [(1-nA[i])/(rA), 1]])
            
            A.append(R5@T56@R6@T67@R7@T78@R8)
        
        AR, AG, AB = A[0], A[1], A[2]

        A = np.array([[[AR[0][0], AG[0][0], AB[0][0]], [AR[0][1], AG[0][1], AB[0][1]]] , [[AR[1][0], AG[1][0], AB[1][0]], [AR[1][1], AG[1][1], AB[1][1]]]])
    return A

def triplet(l):
    df = pd.read_json("data/lenses.json")
    
    if l == 'd': 
        #------------------- Sistema de lentes delgadas -------------
        f1 = np.array(df.loc['convergentLens','triplet']['f'])
        f2 = np.array(df.loc['divergentLens','triplet']['f'])
        f3 = np.array(df.loc['planarConvergentLens','triplet']['f'])
        
        T = np.array([[[1, 1, 1], [0, 0, 0]], [-(f1*f2 + f1*f3 + f2*f3)/(f1*f2*f3), [1, 1, 1]]])
        
    elif l == 'g':
        # ------------------ Sistema de lentes gruesas --------------
        
        dE = np.array(df.loc['planarConvergentLens','triplet']['d'])
        nE = np.array(df.loc['planarConvergentLens','triplet']['n'])
        nD = np.array(df.loc['divergentLens','triplet']['n'])
        rD = np.array(df.loc['divergentLens','triplet']['R'])
        dD = np.array(df.loc['divergentLens','triplet']['d'])
        nC = np.array(df.loc['convergentLens','triplet']['n'])
        dC = np.array(df.loc['convergentLens','triplet']['d'])
        rC = np.array(df.loc['convergentLens','triplet']['R'])
        
        T = []
        for i in range(3):
            R1 = np.array([[1, 0] , [0, 1]])
            T12 = np.array([[1, dE/nE[i]] , [0, 1]])
            R2 = np.array([[1, 0] , [(nD[i]-nE[i])/rD, 1]])
            T23 = np.array([[1, dD/nD[i]] , [0, 1]])
            R3 = np.array([[1, 0] , [(nC[i]-nD[i])/(-rD), 1]])
            T34 = np.array([[1, dC/nC[i]] , [0, 1]])
            R4 = np.array([[1, 0] , [(1-nC[i])/(rC), 1]])

            T.append(R1@T12@R2@T23@R3@T34@R4)
            
        TR, TG, TB = T[0], T[1], T[2]

        T = np.array([[[TR[0][0], TG[0][0], TB[0][0]], [TR[0][1], TG[0][1], TB[0][1]]] , [[TR[1][0], TG[1][0], TB[1][0]], [TR[1][1], TG[1][1], TB[1][1]]]])
        
    return T

def ray_tracing(width, height, rayo, so, n1, obj, res, pixels, width_output, height_output, si2, m, l):
    
    si = si2

    if(m == '0'):
        A = compute_lens_matrix(l)
        # Define propagation matrices after and before the lens
        P2 = np.array([[[1, 1, 1], [si[0]/n1, si[1]/n1, si[2]/n1]],[[0, 0, 0], [1, 1, 1]]])
        P1 = np.array([[[1, 1, 1], [so/n1, so/n1, so/n1]],[[0, 0, 0], [1, 1, 1]]])
        
    elif(m == '1'):
        T = triplet(l)
        P2 = np.array([[[1, 1, 1], [si[0]/n1, si[1]/n1, si[2]/n1]],[[0, 0, 0], [1, 1, 1]]])
        P1 = np.array([[[1, 1, 1], [so[0]/n1, so[1]/n1, so[2]/n1]],[[0, 0, 0], [1, 1, 1]]])
        
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

            #Output ray vector calculation
            if(m == '0'):
                if rayo == 0: #principal
                    alpha_entrada = -math.atan(y_objeto/so) #This ray enters towards the center of the lens
                elif rayo == 1: #parallel
                    alpha_entrada = 0 #This ray enters parallel to the optical axis
                V_entrada = np.array([[y_objeto, y_objeto, y_objeto], [n1*alpha_entrada, n1*alpha_entrada, n1*alpha_entrada]])
            
                res1 = np.einsum('ikj,kj->ij', P1, V_entrada)
                res2 = np.einsum('ikj,kj->ij', A, res1)
                V_salida = np.einsum('ikj,kj->ij', P2, res2)
                
            elif(m == '1'):
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
                x_prime = x*(127.5/1.6)*Mt
                y_prime = y*(127.5/1.6)*Mt
                
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
                pixels[pos_x_prime[0], pos_y_prime[0]] = (pixel[0], pixels[pos_x_prime[0], pos_y_prime[0]][1], pixels[pos_x_prime[0], pos_y_prime[0]][2])
                pixels[pos_x_prime[1], pos_y_prime[1]] = (pixels[pos_x_prime[1], pos_y_prime[1]][0], pixel[1], pixels[pos_x_prime[1], pos_y_prime[1]][2])
                pixels[pos_x_prime[2], pos_y_prime[2]] = (pixels[pos_x_prime[2], pos_y_prime[2]][0], pixels[pos_x_prime[2], pos_y_prime[2]][1], pixel[2])
                next
            elif rayo == 1: #parallel
                pixels[pos_x_prime[0], pos_y_prime[0]] = (pixel[0], pixels[pos_x_prime[0], pos_y_prime[0]][1], pixels[pos_x_prime[0], pos_y_prime[0]][2])
                pixels[pos_x_prime[1], pos_y_prime[1]] = (pixels[pos_x_prime[1], pos_y_prime[1]][0], pixel[1], pixels[pos_x_prime[1], pos_y_prime[1]][2])
                pixels[pos_x_prime[2], pos_y_prime[2]] = (pixels[pos_x_prime[2], pos_y_prime[2]][0], pixels[pos_x_prime[2], pos_y_prime[2]][1], pixel[2])
    return pixels