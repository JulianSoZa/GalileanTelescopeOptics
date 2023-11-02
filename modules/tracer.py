import numpy as np
import math
import pandas as pd

def compute_lens_matrix_singlet(l):
    df = pd.read_json("data/lenses.json")
    
    if l == 'd':
        #------------------- Sistema de lentes delgadas -------------
        f1 = np.array(df.loc['objective','mainSystem']['f'])
        f2 = np.array(df.loc['eyespace','mainSystem']['f'])
        
        d = f1 + f2
        A = np.array([[-f2/f1, d], [[0, 0, 0], -f1/f2]])
        
    elif l == 'g':
        # ------------------ Sistema de lentes gruesas --------------
        nA = np.array(df.loc['objective','mainSystem']['n'])
        rA = np.array(df.loc['objective','mainSystem']['R'])
        dA = np.array(df.loc['objective','mainSystem']['d'])
        nB = np.array(df.loc['eyespace','mainSystem']['n'])
        rB = np.array(df.loc['eyespace','mainSystem']['R'])
        dB = np.array(df.loc['eyespace','mainSystem']['d'])
        
        fA = 1/((nA-1)*((1/rA)-(1/(-rA))+(((nA-1)*dA)/(nA*rA*(-rA)))))
        fB = 1/((nB-1)*((1/(-rB))-(1/(rB))+(((nB-1)*dB)/(nB*rB*(-rB)))))
        
        print(fA, fB)
        
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

def compute_lens_matrix_triplet(l):
    df = pd.read_json("data/lenses.json") 
    if l == 'd':

        f1 = np.array(df.loc['convergentLens','objetiveTriplet']['f'])
        f2 = np.array(df.loc['divergentMeniscusLens','objetiveTriplet']['f'])
        f3 = np.array(df.loc['concavePlaneLens','objetiveTriplet']['f'])

        fo = 1/(1/f1 + 1/f2 + 1/f3)

        f1 = np.array(df.loc['divergentLens','eyespaceTriplet']['f'])
        f2 = np.array(df.loc['convergentMeniscusLens','eyespaceTriplet']['f'])
        f3 = np.array(df.loc['convexPlaneLens','eyespaceTriplet']['f'])

        fe = 1/(1/f1 + 1/f2 + 1/f3)

        d = fo + fe
        A = np.array([[-fe/fo, d], [[0, 0, 0], -fo/fe]])
        
    elif l == 'g':
        # --- Objetivo -----
        n1O =  np.array(df.loc['convergentLens','objetiveTriplet']['n'])
        r1O = df.loc['convergentLens','objetiveTriplet']['R']
        d1O = df.loc['convergentLens','objetiveTriplet']['d']
        
        n2O =  np.array(df.loc['divergentMeniscusLens','objetiveTriplet']['n'])
        r2O = df.loc['divergentMeniscusLens','objetiveTriplet']['R']
        d2O = df.loc['divergentMeniscusLens','objetiveTriplet']['d']
        
        n3O =  np.array(df.loc['concavePlaneLens','objetiveTriplet']['n'])
        r3O = df.loc['concavePlaneLens','objetiveTriplet']['R']
        d3O = df.loc['concavePlaneLens','objetiveTriplet']['d']
        
        # --- Ocular -----
        n1e =  np.array(df.loc['divergentLens','eyespaceTriplet']['n'])
        r1e = df.loc['divergentLens','eyespaceTriplet']['R']
        d1e = df.loc['divergentLens','eyespaceTriplet']['d']
        
        n2e = np.array(df.loc['convergentMeniscusLens','eyespaceTriplet']['n'])
        r2e = df.loc['convergentMeniscusLens','eyespaceTriplet']['R']
        d2e = df.loc['convergentMeniscusLens','eyespaceTriplet']['d']
        
        n3e = np.array(df.loc['convexPlaneLens','eyespaceTriplet']['n'])
        r3e = df.loc['convexPlaneLens','eyespaceTriplet']['R']
        d3e = df.loc['convexPlaneLens','eyespaceTriplet']['d']
        
        fo = 1/(1/(1/((n1O - 1)*(1/r1O - 1/r2O + (n1O - 1)*d1O/(n1O*r1O*r2O)))) + 1/(1/((n2O - 1)*(1/r2O - 1/r3O + (n2O - 1)*d2O/(n2O*r2O*r3O)))) + 1/(1/((n3O - 1)*(1/r3O))))
        
        fe = 1/(1/(1/((n1e - 1)*(1/r1e - 1/r2e + (n1e - 1)*d1e/(n1e*r1e*r2e)))) + 1/(1/((n2e - 1)*(1/r2e - 1/r3e + (n2e - 1)*d2e/(n2e*r2e*r3e)))) + 1/(1/((n3e - 1)*(1/r3e))))

        f2 = 1/(1/(1/((n2O - 1)*(1/r2O - 1/r3O + (n2O - 1)*d2O/(n2O*r2O*r3O)))) + 1/(1/((n3O - 1)*(1/r3O))))
        print(f2)
        
        hv = fo*12/f2 - 1
        
        dsep = fo + fe + hv
        
        A = []
        for i in range(3):
            R1 = np.array([[1, 0] , [0, 1]])
            T12 = np.array([[1, d3e/n3e[i]] , [0, 1]])
            R2 = np.array([[1, 0] , [(n2e[i]-n3e[i])/r3e, 1]])
            T23 = np.array([[1, d2e/n2e[i]] , [0, 1]])
            R3 = np.array([[1, 0] , [(n1e[i]-n2e[i])/r2e, 1]])
            T34 = np.array([[1, d1e/n1e[i]] , [0, 1]])
            R4 = np.array([[1, 0] , [(1-n1e[i])/r1e, 1]])
            
            T45 = np.array([[1, dsep[i]/1] , [0, 1]])
            
            R5 = np.array([[1, 0] , [0, 1]])
            T56 = np.array([[1, d3O/n3O[i]] , [0, 1]])
            R6 = np.array([[1, 0] , [(n2O[i]-n3O[i])/r3O, 1]])
            T67 = np.array([[1, d2O/n2O[i]] , [0, 1]])
            R7 = np.array([[1, 0] , [(n1O[i]-n2O[i])/r2O, 1]])
            T78 = np.array([[1, d1O/n1O[i]] , [0, 1]])
            R8 = np.array([[1, 0] , [(1-n1O[i])/r1O, 1]])
            
            A.append(R1@T12@R2@T23@R3@T34@R4@T45@R5@T56@R6@T67@R7@T78@R8)
        
        AR, AG, AB = A[0], A[1], A[2]

        A = np.array([[[AR[0][0], AG[0][0], AB[0][0]], [AR[0][1], AG[0][1], AB[0][1]]] , [[AR[1][0], AG[1][0], AB[1][0]], [AR[1][1], AG[1][1], AB[1][1]]]])
        
    return A

def ray_tracing(width, height, rayo, so, n1, obj, res, pixels, width_output, height_output, si2, m, l):
    
    si = si2

    if(m == '0'):
        A = compute_lens_matrix_singlet(l)
        # Define propagation matrices after and before the lens
        P2 = np.array([[[1, 1, 1], [si[0]/n1, si[1]/n1, si[2]/n1]],[[0, 0, 0], [1, 1, 1]]])
        P1 = np.array([[[1, 1, 1], [so/n1, so/n1, so/n1]],[[0, 0, 0], [1, 1, 1]]])
        
    elif(m == '1'):
        T = compute_lens_matrix_triplet(l)
        P2 = np.array([[[1, 1, 1], [si[0]/n1, si[1]/n1, si[2]/n1]],[[0, 0, 0], [1, 1, 1]]])
        P1 = np.array([[[1, 1, 1], [so/n1, so/n1, so/n1]],[[0, 0, 0], [1, 1, 1]]])
        
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
                    alpha_entrada = [-math.atan(y_objeto/so), -math.atan(y_objeto/so), -math.atan(y_objeto/so)]
                elif rayo == 1: #parallel
                    alpha_entrada = [0, 0, 0] #This ray enters parallel to the optical axis
                V_entrada = np.array([[y_objeto, y_objeto, y_objeto], [n1*alpha_entrada[0], n1*alpha_entrada[1], n1*alpha_entrada[2]]])
                
                res1 = np.einsum('ikj,kj->ij', P1, V_entrada)
                res2 = np.einsum('ikj,kj->ij', T, res1)
                V_salida = np.einsum('ikj,kj->ij', P2, res2)

            #Transversal magnification
            y_imagen = V_salida[0]

            Mt = y_imagen/y_objeto

            if Mt[0] != Mt[1] or Mt[0] != Mt[2] or Mt[1] != Mt[2]
                w=0

            #Conversion from image coordinates to lens coordinates
            if(m == '0'):
                x_prime = x*(126/1.6)*Mt
                y_prime = y*(126/1.6)*Mt
                
            elif(m == '1'):
                x_prime = x*(126/1.6)*Mt
                y_prime = y*(126/1.6)*Mt
            
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