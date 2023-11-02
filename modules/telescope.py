from PIL import Image #Image file handling
import pandas as pd
import numpy as np
from modules.tracer import *

def telescope_system(m, l, url):
    df = pd.read_json("data/lenses.json") #Se lee el archivo .json para las lentes
    #Se
    if m == '0':
        print('\n---------- Sistema con singletes (aberracion) ----------\n')
        obj = Image.open(url, "r") #se abre la imagen en modo lectura
        
    elif m == '1':
        print('\n---------- Sistema con tripletes (sin aberracion) ----------\n')
        obj = Image.open(url, "r") 
        
    width, height = obj.size  #Se obtiene el ancho y alto de la imagen en pixeles

    n1 = 1 #Indice de refraccion del vacio y aire dado que son practicamente iguales
    
    CHIEF_RAY = 0
    PARALLEL_RAY = 1

    so = df.loc['mars','object']['so'] #Se lee la distancia objeto de marte del dataframe
    do = df.loc['mars','object']['do']
    dio = df.loc['objective','mainSystem']['di'] #Se lee la distancia imagen del sistema
    
    res = dio/height #Se calcula la resolucion
    
    if m == '0':
        #Parametros del singlete
        if l == 'd':
            #Parametrso para lentes delgadas
            f1 = np.array(df.loc['objective','mainSystem']['f']) #Focal del objetivo
            f2 = np.array(df.loc['eyespace','mainSystem']['f']) #Focal del ocular para un singlete
        
        elif l == 'g':
            #Parametroa para lentes gruesas
            nA = np.array(df.loc['objective','mainSystem']['n']) #Indice de refraccon de la lente objetivo(crown)
            rA = np.array(df.loc['objective','mainSystem']['R']) #Radio de curvatura de la lente objetivo(crown)
            dA = np.array(df.loc['objective','mainSystem']['d']) #Espesor de la lente objetivo(crown)
            nB = np.array(df.loc['eyespace','mainSystem']['n']) #Indice de refraccion de la lente ocular (flint) 
            rB = np.array(df.loc['eyespace','mainSystem']['R']) #Radio de curvatura de la lente ocular(flint)
            dB = np.array(df.loc['eyespace','mainSystem']['d']) #Espesor de la lente ocular(flint)
            
            #Calculo de las focales
            f1 = 1/((nA-1)*((1/rA)-(1/(-rA))+(((nA-1)*dA)/(nA*rA*(-rA))))) 
            f2 = 1/((nB-1)*((1/(-rB))-(1/(rB))+(((nB-1)*dB)/(nB*rB*(-rB)))))
        
        #Calculo de las distancias imagen y objeto de cada lente
        si1 = (f1*so)/(so-f1)
        so2 = -(si1-(f1+f2))
        si2 = (f2*so2)/(so2-f2)
        
        si = si2

    elif m == '1':
        #Parametros del triplete
        if l == 'd':
            #Parametros para lentes delgadas
            so = so
            #Focales del triplete del objetivo
            f1 = np.array(df.loc['convergentLens','objetiveTriplet']['f'])
            f2 = np.array(df.loc['divergentMeniscusLens','objetiveTriplet']['f'])
            f3 = np.array(df.loc['concavePlaneLens','objetiveTriplet']['f'])
            
            fo = 1/(1/f1 + 1/f2 + 1/f3) #Focal resultante del objetivo
            
            #Focales del triplete del ocular
            f1 = np.array(df.loc['divergentLens','eyespaceTriplet']['f'])
            f2 = np.array(df.loc['convergentMeniscusLens','eyespaceTriplet']['f'])
            f3 = np.array(df.loc['convexPlaneLens','eyespaceTriplet']['f'])
            
            fe = 1/(1/f1 + 1/f2 + 1/f3) #focal resultante del ocular
            
        elif l == 'g':
            #Parametros para lentes gruesas
            so = so
            #objetivo 
            #Undices de refraccion de cada lente para cada color, radios de curatura y espesor en ese orden
            n1OR =  df.loc['convergentLens','objetiveTriplet']['n'][0]
            n1OG =  df.loc['convergentLens','objetiveTriplet']['n'][1]
            n1OB =  df.loc['convergentLens','objetiveTriplet']['n'][2]
            r1O = df.loc['convergentLens','objetiveTriplet']['R']
            d1O = df.loc['convergentLens','objetiveTriplet']['d']
            
            n2OR =  df.loc['divergentMeniscusLens','objetiveTriplet']['n'][0]
            n2OG =  df.loc['divergentMeniscusLens','objetiveTriplet']['n'][1]
            n2OB =  df.loc['divergentMeniscusLens','objetiveTriplet']['n'][2]
            r2O = df.loc['divergentMeniscusLens','objetiveTriplet']['R']
            d2O = df.loc['divergentMeniscusLens','objetiveTriplet']['d']
            
            n3OR =  df.loc['concavePlaneLens','objetiveTriplet']['n'][0]
            n3OG =  df.loc['concavePlaneLens','objetiveTriplet']['n'][1]
            n3OB =  df.loc['concavePlaneLens','objetiveTriplet']['n'][2]
            r3O = df.loc['concavePlaneLens','objetiveTriplet']['R']
            d3O = df.loc['concavePlaneLens','objetiveTriplet']['d']
            
            #Calculo de las focales de cada color para cada lente del triplete
            f1R = 1/((n1OR - 1)*(1/r1O - 1/r2O + (n1OR - 1)*d1O/(n1OR*r1O*r2O)))

            f1G = 1/((n1OG - 1)*(1/r1O - 1/r2O + (n1OG - 1)*d1O/(n1OG*r1O*r2O)))

            f1B = 1/((n1OB - 1)*(1/r1O - 1/r2O + (n1OB - 1)*d1O/(n1OB*r1O*r2O)))

            f2R = 1/((n2OR - 1)*(1/r2O - 1/r3O + (n2OR - 1)*d2O/(n2OR*r2O*r3O)))

            f2G = 1/((n2OG - 1)*(1/r2O - 1/r3O + (n2OG - 1)*d2O/(n2OG*r2O*r3O)))

            f2B = 1/((n2OB - 1)*(1/r2O - 1/r3O + (n2OB - 1)*d2O/(n2OB*r2O*r3O)))

            f3R = 1/((n3OR - 1)*(1/r3O))

            f3G = 1/((n3OG - 1)*(1/r3O))

            f3B = 1/((n3OB - 1)*(1/r3O))

            #focal resultante de cada color para cada lente del triplete
            
            fR = 1/(1/f1R + 1/f2R + 1/f3R)
            fG = 1/(1/f1G + 1/f2G + 1/f3G)
            fB = 1/(1/f1B + 1/f2B + 1/f3B)
            
            fo = np.array([fR, fG, fB])
            
            #ocular
            
            #Indice de refraccion para cada corlor, radio de curvatura y espesor para cada lente del triplete del ocular
            n1eR =  df.loc['divergentLens','eyespaceTriplet']['n'][0]
            n1eG =  df.loc['divergentLens','eyespaceTriplet']['n'][1]
            n1eB =  df.loc['divergentLens','eyespaceTriplet']['n'][2]
            r1e = df.loc['divergentLens','eyespaceTriplet']['R']
            d1e = df.loc['divergentLens','eyespaceTriplet']['d']
            
            n2eR =  df.loc['convergentMeniscusLens','eyespaceTriplet']['n'][0]
            n2eG =  df.loc['convergentMeniscusLens','eyespaceTriplet']['n'][1]
            n2eB =  df.loc['convergentMeniscusLens','eyespaceTriplet']['n'][2]
            r2e = df.loc['convergentMeniscusLens','eyespaceTriplet']['R']
            d2e = df.loc['convergentMeniscusLens','eyespaceTriplet']['d']
            
            n3eR =  df.loc['convexPlaneLens','eyespaceTriplet']['n'][0]
            n3eG =  df.loc['convexPlaneLens','eyespaceTriplet']['n'][1]
            n3eB =  df.loc['convexPlaneLens','eyespaceTriplet']['n'][2]
            r3e = df.loc['convexPlaneLens','eyespaceTriplet']['R']
            d3e = df.loc['convexPlaneLens','eyespaceTriplet']['d']
            
            #Calculo de la focar de carda color para cada lente dle triplete del ocular
            f1R = 1/((n1eR - 1)*(1/r1e - 1/r2e + (n1eR - 1)*d1e/(n1eR*r1e*r2e)))

            f1G = 1/((n1eG - 1)*(1/r1e - 1/r2e + (n1eG - 1)*d1e/(n1eG*r1e*r2e)))

            f1B = 1/((n1eB - 1)*(1/r1e - 1/r2e + (n1eB - 1)*d1e/(n1eB*r1e*r2e)))

            f2R = 1/((n2eR - 1)*(1/r2e - 1/r3e + (n2eR - 1)*d2e/(n2eR*r2e*r3e)))

            f2G = 1/((n2eG - 1)*(1/r2e - 1/r3e + (n2eG - 1)*d2e/(n2eG*r2e*r3e)))

            f2B = 1/((n2eB - 1)*(1/r2e - 1/r3e + (n2eB - 1)*d2e/(n2eB*r2e*r3e)))

            f3R = 1/((n3eR - 1)*(1/r3e))

            f3G = 1/((n3eG - 1)*(1/r3e))

            f3B = 1/((n3eB - 1)*(1/r3e))

            #focales resultantes para cada color del ocular
            
            fR = 1/(1/f1R + 1/f2R + 1/f3R)
            fG = 1/(1/f1G + 1/f2G + 1/f3G)
            fB = 1/(1/f1B + 1/f2B + 1/f3B)
            
            fe = np.array([fR, fG, fB])
            
        #Calculo de las distancia imagen y las distancias objetos para el objetivo y ocular    
        si1 = (fo*so)/(so-fo)
        so2 = -(si1-(fo+fe))
        si2 = (fe*so2)/(so2-fe)
        
        si = si2
        
    width_output = int(width)+40
    height_output = int(height)+40

    image = Image.new("RGB", (width_output, height_output), "white") #crea la imagen de salida y por defecto es blanca

    pixels = image.load() #sr cargan los pixeles de la imagen
    
    print('\n---------- Trazado de rayos ----------\n')

    #Se hace el trazado de rayos para  los rayos jefe y paralelos dle sistema abeerado y sostema con la aberración corregida
    if m == '0':
        print('\nChief ray:\n')
        pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)
        print('\nParallel ray:\n')
        pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)    
        image.save('img/nuevaImagen.png', format='PNG')
        
    elif m == '1':
        print('\nChief ray:\n')
        pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)
        print('\nParallel ray:\n')
        pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)    
        image.save('img/nuevaImagenAberracionCorregida.png', format='PNG')