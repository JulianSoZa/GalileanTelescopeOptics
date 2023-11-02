import numpy as np
import math
import pandas as pd

"""En este modulo se hace el trazado de rayos dependiendo si el usuario escoge lentes gruesas o lentes delgadas,
se hace el trazado para dos rayos: paralelos y jefes. Ademas de que se hace el trazado de rayos para los tres colores al mismo tiempo,
el orden de las dimensiones es: (Rojo, Verde, Azul).
Tambien se calcula la aberracion cromatica lateral
En este codigo se trabaja con vectores y matrices de tres dimensiones independientes (Rojo, Verde, Azul)"""

def compute_lens_matrix_singlet(l): # funcion para hallar la matriz del sistema para lentes gruesas y delgadas, para la configuracion de singletes
    df = pd.read_json("data/lenses.json") # se leen los parametros de las lentes
    
    if l == 'd': # Calculo de la matriz del sistema para lentes delgadas
        #------------------- Sistema de lentes delgadas -------------
        f1 = np.array(df.loc['objective','mainSystem']['f']) # focales del objetivo para cada color
        f2 = np.array(df.loc['eyespace','mainSystem']['f']) # focales del ocular para cada color
        
        d = f1 + f2 # separacion entre las lentes
        A = np.array([[-f2/f1, d], [[0, 0, 0], -f1/f2]]) # matriz del sistema para las tres dimensiones (Rojo, Verde, Azul)
    
        print(f'\nFocales del objetivo:\n{f1}\n')
        print(f'\nFocales del ocular:\n{f2}\n')    
    
    elif l == 'g': # Calculo de la matriz del sistema para lentes gruesas
        # ------------------ Sistema de lentes gruesas --------------
        nA = np.array(df.loc['objective','mainSystem']['n']) # indices de refraccion de la lente objetivo para cada uno de los colores 
        rA = np.array(df.loc['objective','mainSystem']['R']) # radio de la lente objetivo
        dA = np.array(df.loc['objective','mainSystem']['d']) # espesor de la lentes objetivo
        nB = np.array(df.loc['eyespace','mainSystem']['n']) # indices de refraccion de la lente ocular para cada uno de los colores 
        rB = np.array(df.loc['eyespace','mainSystem']['R']) # radio de la lente ocular
        dB = np.array(df.loc['eyespace','mainSystem']['d']) # espesor de la lente ocular
        
        fA = 1/((nA-1)*((1/rA)-(1/(-rA))+(((nA-1)*dA)/(nA*rA*(-rA))))) # focal de la lente objetivo segun el indice de refraccion
        fB = 1/((nB-1)*((1/(-rB))-(1/(rB))+(((nB-1)*dB)/(nB*rB*(-rB))))) # focal de la lente ocular segun el indice de refraccion
        
        A = [] # se crea la variable de la matriz del sistema
        for i in range(3): #se halla la matriz del sistema para cada color
            R5 = np.array([[1, 0] , [(nB[i]-1)/(rB), 1]]) # Matriz de refraccion de la segunda superficie de la lente ocular
            T56 = np.array([[1, dB/nB[i]] , [0, 1]]) # Matriz de transmision de la lente ocular
            R6 = np.array([[1, 0] , [(1-nB[i])/(-rB), 1]]) # Matriz de refraccion de la primera superficie de la lente ocular
            T67 = np.array([[1, fA[i] + fB[i]] , [0, 1]]) # Matriz de transmision entre las dos lentes
            R7 = np.array([[1, 0] , [(nA[i]-1)/(-rA), 1]]) # Matriz de refraccion de la segunda superficie de la lente objetivo
            T78 = np.array([[1, dA/nA[i]] , [0, 1]]) # Matriz de transmision de la lente objetivo
            R8 = np.array([[1, 0] , [(1-nA[i])/(rA), 1]]) # Matriz de refraccion de la primera superficie de la lente objetivo
            
            A.append(R5@T56@R6@T67@R7@T78@R8) # Se halla la matriz del sistema para cada color
        
        AR, AG, AB = A[0], A[1], A[2] # Se gurada la matriz del sistema para cada color de manera independiente

        #Se halla la matriz del sistema con tres dimensiones (Rojo, Verde, Azul)
        A = np.array([[[AR[0][0], AG[0][0], AB[0][0]], [AR[0][1], AG[0][1], AB[0][1]]] , [[AR[1][0], AG[1][0], AB[1][0]], [AR[1][1], AG[1][1], AB[1][1]]]])

        print(f'\nFocales del objetivo:\n{fA}\n')
        print(f'\nFocales del ocular:\n{fB}\n')
    
    print(f'\nMatriz del sistema:\n{A}\n')
    
    return A

def compute_lens_matrix_triplet(l): # funcion para hallar la matriz del sistema para lentes gruesas y delgadas, para la configuracion de tripletes
    df = pd.read_json("data/lenses.json") # se leen los parametros de las lentes
    
    if l == 'd': # Calculo de la matriz del sistema para lentes delgadas
        f1 = np.array(df.loc['convergentLens','objetiveTriplet']['f']) #focales de la primera lente del triplete objetivo segun el color
        f2 = np.array(df.loc['divergentMeniscusLens','objetiveTriplet']['f']) #focales de la segunda lente del triplete objetivo segun el color
        f3 = np.array(df.loc['concavePlaneLens','objetiveTriplet']['f']) #focales de la tercera lente del triplete objetivo segun el color

        fo = 1/(1/f1 + 1/f2 + 1/f3) #focal equivalente del triplete objetivo segun el color

        f1 = np.array(df.loc['divergentLens','eyespaceTriplet']['f']) #focales de la primera lente del triplete ocular segun el color
        f2 = np.array(df.loc['convergentMeniscusLens','eyespaceTriplet']['f']) #focales de la segunda lente del triplete ocular segun el color
        f3 = np.array(df.loc['convexPlaneLens','eyespaceTriplet']['f']) #focales de la tercera lente del triplete ocular segun el color

        fe = 1/(1/f1 + 1/f2 + 1/f3) #focal equivalente del triplete ocular segun el color

        d = fo + fe # separacion entre las lentes
        
        A = np.array([[-fe/fo, d], [[0, 0, 0], -fo/fe]]) # matriz del sistema para las tres dimensiones (Rojo, Verde, Azul)
        
    elif l == 'g': # Calculo de la matriz del sistema para lentes gruesas
        # --- Objetivo -----
        n1O =  np.array(df.loc['convergentLens','objetiveTriplet']['n']) # indices de refraccion de la primera lente del triplete objetivo para cada uno de los colores 
        r1O = df.loc['convergentLens','objetiveTriplet']['R'] # primer radio del triplete objetivo
        d1O = df.loc['convergentLens','objetiveTriplet']['d'] # espesor de la primera lente del triplete objetivo
        
        n2O =  np.array(df.loc['divergentMeniscusLens','objetiveTriplet']['n']) #indices de refraccion de la segunda lente del triplete objetivo para cada uno de los colores 
        r2O = df.loc['divergentMeniscusLens','objetiveTriplet']['R'] #segundo radio del triplete objetivo
        d2O = df.loc['divergentMeniscusLens','objetiveTriplet']['d'] #espesor de la segunda lente del triplete objetivo
        
        n3O =  np.array(df.loc['concavePlaneLens','objetiveTriplet']['n']) #indices de refraccion de la tercera lente del triplete objetivo para cada uno de los colores 
        r3O = df.loc['concavePlaneLens','objetiveTriplet']['R'] #tercer radio del triplete objetivo
        d3O = df.loc['concavePlaneLens','objetiveTriplet']['d'] #espesor de la tercera lente del triplete objetivo
        
        # --- Ocular -----
        n1e =  np.array(df.loc['divergentLens','eyespaceTriplet']['n']) # indices de refraccion de la primera lente del triplete ocular para cada uno de los colores 
        r1e = df.loc['divergentLens','eyespaceTriplet']['R'] # primer radio del triplete ocular
        d1e = df.loc['divergentLens','eyespaceTriplet']['d'] # espesor de la primera lente del triplete ocular
        
        n2e = np.array(df.loc['convergentMeniscusLens','eyespaceTriplet']['n']) # indices de refraccion de la segunda lente del triplete ocular para cada uno de los colores 
        r2e = df.loc['convergentMeniscusLens','eyespaceTriplet']['R'] # segundo radio del triplete ocular
        d2e = df.loc['convergentMeniscusLens','eyespaceTriplet']['d'] # espesor de la segunda lente del triplete ocular
        
        n3e = np.array(df.loc['convexPlaneLens','eyespaceTriplet']['n']) # indices de refraccion de la tercera lente del triplete ocular para cada uno de los colores
        r3e = df.loc['convexPlaneLens','eyespaceTriplet']['R'] # tercer radio del triplete ocular
        d3e = df.loc['convexPlaneLens','eyespaceTriplet']['d'] # espesor de la tercera lente del triplete ocular
        
        #focal equivalente del triplete objetivo segun el color
        fo = 1/(1/(1/((n1O - 1)*(1/r1O - 1/r2O + (n1O - 1)*d1O/(n1O*r1O*r2O)))) + 1/(1/((n2O - 1)*(1/r2O - 1/r3O + (n2O - 1)*d2O/(n2O*r2O*r3O)))) + 1/(1/((n3O - 1)*(1/r3O))))
        
        #focal equivalente del triplete ocular segun el color
        fe = 1/(1/(1/((n1e - 1)*(1/r1e - 1/r2e + (n1e - 1)*d1e/(n1e*r1e*r2e)))) + 1/(1/((n2e - 1)*(1/r2e - 1/r3e + (n2e - 1)*d2e/(n2e*r2e*r3e)))) + 1/(1/((n3e - 1)*(1/r3e))))

        #focal equivalente de la segunda con la tercera lente del triplete objetivo segun el color (para hallar los planos principales del triplete objetivo)
        f2 = 1/(1/(1/((n2O - 1)*(1/r2O - 1/r3O + (n2O - 1)*d2O/(n2O*r2O*r3O)))) + 1/(1/((n3O - 1)*(1/r3O))))

        hv = fo*(d1O+d2O+d3O)/f2 #distancia del segundo plano principal del triplete objetivo
        
        dsep = fo + fe + hv # distancia de separacion entre las lentes ocular y objetivo
        
        A = [] # se crea la variable de la matriz del sistema
        for i in range(3): #se halla la matriz del sistema para cada color
            R1 = np.array([[1, 0] , [0, 1]]) # Matriz de refraccion de la cuarta superficie del triplete ocular
            T12 = np.array([[1, d3e/n3e[i]] , [0, 1]]) # Matriz de transmision de la tercera lente del triplete ocular
            R2 = np.array([[1, 0] , [(n2e[i]-n3e[i])/r3e, 1]]) # Matriz de refraccion de la tercera superficie del triplete ocular
            T23 = np.array([[1, d2e/n2e[i]] , [0, 1]])  # Matriz de transmision de la segunda lente del triplete ocular
            R3 = np.array([[1, 0] , [(n1e[i]-n2e[i])/r2e, 1]]) # Matriz de refraccion de la segunda superficie del triplete ocular
            T34 = np.array([[1, d1e/n1e[i]] , [0, 1]]) # Matriz de transmision de la primera lente del triplete ocular
            R4 = np.array([[1, 0] , [(1-n1e[i])/r1e, 1]]) # Matriz de refraccion de la primera superficie del triplete ocular
            
            T45 = np.array([[1, dsep[i]/1] , [0, 1]]) # Matriz de transmision entre las dos lentes
            
            R5 = np.array([[1, 0] , [0, 1]]) # Matriz de refraccion de la cuarta superficie del triplete objetivo
            T56 = np.array([[1, d3O/n3O[i]] , [0, 1]]) # Matriz de transmision de la tercera lente del triplete objetivo
            R6 = np.array([[1, 0] , [(n2O[i]-n3O[i])/r3O, 1]]) # Matriz de refraccion de la tercera superficie del triplete objetivo
            T67 = np.array([[1, d2O/n2O[i]] , [0, 1]]) # Matriz de transmision de la segunda lente del triplete objetivo
            R7 = np.array([[1, 0] , [(n1O[i]-n2O[i])/r2O, 1]]) # Matriz de refraccion de la segunda superficie del triplete objetivo
            T78 = np.array([[1, d1O/n1O[i]] , [0, 1]]) # Matriz de transmision de la primera lente del triplete objetivo
            R8 = np.array([[1, 0] , [(1-n1O[i])/r1O, 1]]) # Matriz de refraccion de la primera superficie del triplete objetivo
            
            A.append(R1@T12@R2@T23@R3@T34@R4@T45@R5@T56@R6@T67@R7@T78@R8) # Se halla la matriz del sistema para cada color
        
        AR, AG, AB = A[0], A[1], A[2] # Se gurada la matriz del sistema para cada color de manera independiente

        #Se halla la matriz del sistema con tres dimensiones (Rojo, Verde, Azul)
        A = np.array([[[AR[0][0], AG[0][0], AB[0][0]], [AR[0][1], AG[0][1], AB[0][1]]] , [[AR[1][0], AG[1][0], AB[1][0]], [AR[1][1], AG[1][1], AB[1][1]]]])
    
    print(f'\nFocales del objetivo:\n{fo}\n')
    print(f'\nFocales del ocular:\n{fe}\n')    
    print(f'\nMatriz del sistema:\n{A}\n')
    
    return A

#funcion para hacer el trazado de rayos
def ray_tracing(width, height, rayo, so, n1, obj, res, pixels, width_output, height_output, si2, m, l):
    
    #Aberracion cromatica lateral (LCA) segun la magnificacion de cada color
    LCA = 0 # Se inicializa la variable de aberracion cromatica lateral
    LCAmax = 0 # Se inicializa la variable de aberracion cromatica lateral maxima
    LCAarg = 0 # Se inicializa la variable de aberracion cromatica lateral para la posicion del color
    LCAargMax = 0 # Se inicializa la variable de aberracion cromatica lateral maxima para la posicion del color
    LCAcolors =  ['RG', 'RB', 'GB'] # Se define las diferentes combinaciones de la mayor diferencia de magnificacion
    LCApor = 0 #Porcentaje de aberracion cromatica lateral respecto la magnificacion menor
    
    si = si2 #se cambia el nombre de la variable
    
    print(f'\nDistancia objeto:\n{so}\n')
    print(f'\nDistancia imagen:\n{si}\n')

    if(m == '0'): #Se calculan las matrices de transformacion para el sistema con singletes (con aberracion)
        A = compute_lens_matrix_singlet(l) #matriz del sistema para lentes gruesas y delgadas (segun 'l'), para la configuracion de singletes
        P2 = np.array([[[1, 1, 1], [si[0]/n1, si[1]/n1, si[2]/n1]],[[0, 0, 0], [1, 1, 1]]]) # Define la propagacion despues de las lentes
        P1 = np.array([[[1, 1, 1], [so/n1, so/n1, so/n1]],[[0, 0, 0], [1, 1, 1]]]) # Define la propagacion antes de las lentes
        
    elif(m == '1'): #Se calculan las matrices de transformacion para el sistema con tripletes (sin aberracion)
        T = compute_lens_matrix_triplet(l) #matriz del sistema para lentes gruesas y delgadas (segun 'l'), para la configuracion de tripletes
        P2 = np.array([[[1, 1, 1], [si[0]/n1, si[1]/n1, si[2]/n1]],[[0, 0, 0], [1, 1, 1]]]) # Define la propagacion despues de las lentes
        P1 = np.array([[[1, 1, 1], [so/n1, so/n1, so/n1]],[[0, 0, 0], [1, 1, 1]]]) # Define la propagacion antes de las lentes
        
    #Se itera sobre cada pixel de la imagen
    for i in range(width):
        for j in range(height):

            # Get pixel value and calculate its position relative to the center of the image
            pos_x = i #posicion del pixel en x
            pos_y = j #Posicion del pixel en y
            pixel = obj.getpixel((pos_x, pos_y)) #Se obtienen los valores del pixel en RGB 

            x = pos_x - width/2 #se calcula la posicion relativa del pixel en x con respecto al entro de la imagen
            y = pos_y - height/2 #se calcula la posicion relativa del pixel en y con respecto al entro de la imagen

            r = math.sqrt( x*x + y*y ) + 1 # se calcula la distancia del pixel en pixels con respecto al centro de la imagen

            y_objeto = r*res #se halla la altura del pixel en unidades metricas

            if(m == '0'): # se calcula el rayo de salida para la configuracion de singletes
                if rayo == 0: # para rayo jefe
                    alpha_entrada = -math.atan(y_objeto/so) # el rayo incide en el centro de la lente objetivo
                    
                elif rayo == 1: #para el rayo paralelo
                    alpha_entrada = 0 # el rayo entra paralelo al eje optico
                
                #Se define el vector del rayo de entrada [altura imagen, indice de refraccion del medio incidente * angulo de entrada]    
                V_entrada = np.array([[y_objeto, y_objeto, y_objeto], [n1*alpha_entrada, n1*alpha_entrada, n1*alpha_entrada]])
            
                #Se hace la transformacion del vector, en donde las transformaciones son indenpendientes para cada dimension (Rojo, Verde, Azul)
                res1 = np.einsum('ikj,kj->ij', P1, V_entrada) #hace la multiplicacion matricial de manera independiente para cada una de las dimensiones
                res2 = np.einsum('ikj,kj->ij', A, res1) #hace la multiplicacion matricial de manera independiente para cada una de las dimensiones
                V_salida = np.einsum('ikj,kj->ij', P2, res2) #Vector del rayo de salida con las tres dimensiones (Rojo, Verde, Azul)
                
            elif(m == '1'): # se calcula el rayo de salida para la configuracion de tripletes
                if rayo == 0: # para el rayo jefe
                    alpha_entrada = [-math.atan(y_objeto/so), -math.atan(y_objeto/so), -math.atan(y_objeto/so)] # el rayo incide en el centro de la lente objetivo
                
                elif rayo == 1: #para el rayo paralelo
                    alpha_entrada = [0, 0, 0] # el rayo entra paralelo al eje optico
                
                #Se define el vector del rayo de entrada [altura imagen, indice de refraccion del medio incidente * angulo de entrada]
                V_entrada = np.array([[y_objeto, y_objeto, y_objeto], [n1*alpha_entrada[0], n1*alpha_entrada[1], n1*alpha_entrada[2]]])
                
                #Se hace la transformacion del vector, en donde las transformaciones son indenpendientes para cada dimension (Rojo, Verde, Azul)
                res1 = np.einsum('ikj,kj->ij', P1, V_entrada) #hace la multiplicacion matricial de manera independiente para cada una de las dimensiones
                res2 = np.einsum('ikj,kj->ij', T, res1) #hace la multiplicacion matricial de manera independiente para cada una de las dimensiones
                V_salida = np.einsum('ikj,kj->ij', P2, res2) #Vector del rayo de salida con las tres dimensiones (Rojo, Verde, Azul)

            y_imagen = V_salida[0] #altura del rayo de salida

            Mt = y_imagen/y_objeto # Magnificacion transversal del rayo
            
            #Calculo de la aberracion cromatica lateral
            if Mt[0] != Mt[1] or Mt[0] != Mt[2] or Mt[1] != Mt[2]: #si la magnificacion entre colores es diferente
                RG = abs(Mt[0] - Mt[1]) #Diferencia de magnificacion entre el rojo y el verde
                RB = abs(Mt[0] - Mt[2]) #Diferencia de magnificacion entre el rojo y el azul
                GB = abs(Mt[1] - Mt[2]) #Diferencia de magnificacion entre el verde y el azul
                
                LCAmax = np.max([RG, RB, GB]) #aberracion cromatica lateral maxima
                LCAargMax = np.argmax([RG, RB, GB]) #posicion de la aberracion cromatica lateral maxima
                
            if LCA < LCAmax: # Se acutaliza la aberracion cromatica lateral 
                LCA = LCAmax # Se acutaliza la aberracion cromatica lateral
                LCAarg = LCAargMax #Se actualiza la posicion de la aberracion cromatica lateral
                
                #Se se halla el porcentaje de la aberracion cromatica lateral segun la mayor diferencia entre magnificaciones
                if LCAarg == 0:
                    LCAmtR = Mt[0] #Magnificacion del rojo
                    LCAmtG = Mt[1] #Magnificacion del verde
                    
                    LCApor = (abs(LCAmtR - LCAmtG)/LCAmtG)*100 #porcentaje de la aberracion cromatica lateral del rojo con respecto al verde
                    
                elif LCAarg == 1:
                    LCAmtR = Mt[0] #Magnificacion del rojo
                    LCAmtB = Mt[2] #Magnificacion del azul
                    
                    LCApor = (abs(LCAmtR - LCAmtB)/LCAmtB)*100 #porcentaje de la aberracion cromatica lateral del rojo con respecto al azul
                    
                elif LCAarg == 2:
                    LCAmtG = Mt[1] #Magnificacion del verde
                    LCAmtB = Mt[2] #Magnificacion del azul
                    
                    LCApor = (abs(LCAmtG - LCAmtB)/LCAmtB)*100 #porcentaje de la aberracion cromatica lateral del verde con respecto al azul

            #Se convierte de unidades metricas a unidades de pixel donde 126/1.6 es el factor de conversion
            if(m == '0'):
                x_prime = x*(126/1.6)*Mt #Posicion del pixel en x segun el color
                y_prime = y*(126/1.6)*Mt #Posicion del pixel en y segun el color
                
            elif(m == '1'):
                x_prime = x*(126/1.6)*Mt #Posicion del pixel en x segun el color
                y_prime = y*(126/1.6)*Mt #Posicion del pixel en y segun el color
            
            #se cambia el sistema de referencia para la posicion del pixel: posicion matricial de los canales
            pos_x_prime = [int(x_prime[0] + width_output/2), int(x_prime[1] + width_output/2), int(x_prime[2] + width_output/2)] #Posicion del pixel en x segun el color
            pos_y_prime = [int(y_prime[0] + height_output/2), int(y_prime[1] + height_output/2), int(y_prime[2] + height_output/2)] #Posicion del pixel en y segun el color
            
            #Se omiten los pixels que quedan fuera del lienzo de la imagen de salida
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
            
            #Se actualiza el valor del pixel para cada uno de los colores
            if rayo == 0: #para el rayo jefe
                pixels[pos_x_prime[0], pos_y_prime[0]] = (pixel[0], pixels[pos_x_prime[0], pos_y_prime[0]][1], pixels[pos_x_prime[0], pos_y_prime[0]][2]) #valor nuevo del pixel en el canal Rojo
                pixels[pos_x_prime[1], pos_y_prime[1]] = (pixels[pos_x_prime[1], pos_y_prime[1]][0], pixel[1], pixels[pos_x_prime[1], pos_y_prime[1]][2]) #valor nuevo del pixel en el canal Verde
                pixels[pos_x_prime[2], pos_y_prime[2]] = (pixels[pos_x_prime[2], pos_y_prime[2]][0], pixels[pos_x_prime[2], pos_y_prime[2]][1], pixel[2]) #valor nuevo del pixel en el canal Azul
                next
            
            elif rayo == 1: # para el rayo paralelo
                pixels[pos_x_prime[0], pos_y_prime[0]] = (pixel[0], pixels[pos_x_prime[0], pos_y_prime[0]][1], pixels[pos_x_prime[0], pos_y_prime[0]][2]) #valor nuevo del pixel en el canal Rojo
                pixels[pos_x_prime[1], pos_y_prime[1]] = (pixels[pos_x_prime[1], pos_y_prime[1]][0], pixel[1], pixels[pos_x_prime[1], pos_y_prime[1]][2]) #valor nuevo del pixel en el canal Verde
                pixels[pos_x_prime[2], pos_y_prime[2]] = (pixels[pos_x_prime[2], pos_y_prime[2]][0], pixels[pos_x_prime[2], pos_y_prime[2]][1], pixel[2]) #valor nuevo del pixel en el canal Azul
    
    print('LCA maximo: ', LCA) #Se imprime el valor maximo de la aberracion cromatica lateral (diferencia de magnificaciones)
    print('LCA colores: ', LCAcolors[LCAarg]) # Se imprime los colores con mayor diferencia de magnificacion
    print(f'LCA porcentaje: {LCApor} %') # Se imprime el porcentaje de aberracion cromatica lateral
    
    #retorna los valores de los pixels de la imagen de salida
    return pixels 