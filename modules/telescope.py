from PIL import Image #Image file handling
import pandas as pd
import numpy as np
from modules.tracer import *

def telescope_system(m, l, url):
    df = pd.read_json("data/lenses.json") 
    
    if m == '0':
        obj = Image.open(url, "r")
    elif m == '1':
        obj = Image.open("img/mars.jpg", "r")
        
    width, height = obj.size

    n1 = 1
    
    CHIEF_RAY = 0
    PARALLEL_RAY = 1

    so = df.loc['mars','object']['so']
    do = df.loc['mars','object']['do']
    dio = df.loc['objective','mainSystem']['di']
    
    res = dio/height
    
    if m == '0':
        if l == 'd':
            f1 = np.array(df.loc['objective','mainSystem']['f'])
            f2 = np.array(df.loc['eyespace','mainSystem']['f'])
        
        elif l == 'g':
            nA = np.array(df.loc['objective','mainSystem']['n'])
            rA = np.array(df.loc['objective','mainSystem']['R'])
            dA = np.array(df.loc['objective','mainSystem']['d'])
            nB = np.array(df.loc['eyespace','mainSystem']['n'])
            rB = np.array(df.loc['eyespace','mainSystem']['R'])
            dB = np.array(df.loc['eyespace','mainSystem']['d'])
            
            f1 = 1/((nA-1)*((1/rA)-(1/(-rA))+(((nA-1)*dA)/(nA*rA*(-rA)))))
            f2 = 1/((nB-1)*((1/(-rB))-(1/(rB))+(((nB-1)*dB)/(nB*rB*(-rB)))))
        
        si1 = (f1*so)/(so-f1)
        so2 = -(si1-(f1+f2))
        si2 = (f2*so2)/(so2-f2)
    
        print("si2: ", si2)
        
        si = si2

    elif m == '1':
        
        if l == 'd':
            so = so
            f1 = np.array(df.loc['convergentLens','objetiveTriplet']['f'])
            f2 = np.array(df.loc['divergentMeniscusLens','objetiveTriplet']['f'])
            f3 = np.array(df.loc['concavePlaneLens','objetiveTriplet']['f'])
            
            fo = 1/(1/f1 + 1/f2 + 1/f3)
            
            f1 = np.array(df.loc['divergentLens','eyespaceTriplet']['f'])
            f2 = np.array(df.loc['convergentMeniscusLens','eyespaceTriplet']['f'])
            f3 = np.array(df.loc['convexPlaneLens','eyespaceTriplet']['f'])
            
            fe = 1/(1/f1 + 1/f2 + 1/f3)
            
        elif l == 'g':
            so = so
            #objetivo 
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
            
            f1R = 1/((n1OR - 1)*(1/r1O - 1/r2O + (n1OR - 1)*d1O/(n1OR*r1O*r2O)))

            f1G = 1/((n1OG - 1)*(1/r1O - 1/r2O + (n1OG - 1)*d1O/(n1OG*r1O*r2O)))

            f1B = 1/((n1OB - 1)*(1/r1O - 1/r2O + (n1OB - 1)*d1O/(n1OB*r1O*r2O)))

            f2R = 1/((n2OR - 1)*(1/r2O - 1/r3O + (n2OR - 1)*d2O/(n2OR*r2O*r3O)))

            f2G = 1/((n2OG - 1)*(1/r2O - 1/r3O + (n2OG - 1)*d2O/(n2OG*r2O*r3O)))

            f2B = 1/((n2OB - 1)*(1/r2O - 1/r3O + (n2OB - 1)*d2O/(n2OB*r2O*r3O)))

            f3R = 1/((n3OR - 1)*(1/r3O))

            f3G = 1/((n3OG - 1)*(1/r3O))

            f3B = 1/((n3OB - 1)*(1/r3O))
            
            fR = 1/(1/f1R + 1/f2R + 1/f3R)
            fG = 1/(1/f1G + 1/f2G + 1/f3G)
            fB = 1/(1/f1B + 1/f2B + 1/f3B)
            
            fo = np.array([fR, fG, fB])
            
            #ocular
            
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
            
            f1R = 1/((n1eR - 1)*(1/r1e - 1/r2e + (n1eR - 1)*d1e/(n1eR*r1e*r2e)))

            f1G = 1/((n1eG - 1)*(1/r1e - 1/r2e + (n1eG - 1)*d1e/(n1eG*r1e*r2e)))

            f1B = 1/((n1eB - 1)*(1/r1e - 1/r2e + (n1eB - 1)*d1e/(n1eB*r1e*r2e)))

            f2R = 1/((n2eR - 1)*(1/r2e - 1/r3e + (n2eR - 1)*d2e/(n2eR*r2e*r3e)))

            f2G = 1/((n2eG - 1)*(1/r2e - 1/r3e + (n2eG - 1)*d2e/(n2eG*r2e*r3e)))

            f2B = 1/((n2eB - 1)*(1/r2e - 1/r3e + (n2eB - 1)*d2e/(n2eB*r2e*r3e)))

            f3R = 1/((n3eR - 1)*(1/r3e))

            f3G = 1/((n3eG - 1)*(1/r3e))

            f3B = 1/((n3eB - 1)*(1/r3e))
            
            fR = 1/(1/f1R + 1/f2R + 1/f3R)
            fG = 1/(1/f1G + 1/f2G + 1/f3G)
            fB = 1/(1/f1B + 1/f2B + 1/f3B)
            
            fe = np.array([fR, fG, fB])
            
            print('fo t:', fo)
            print('fe t:', fe)
            
        si1 = (fo*so)/(so-fo)
        so2 = -(si1-(fo+fe))
        si2 = (fe*so2)/(so2-fe)
    
        print("si2: ", si2)
        
        si = si2
        
    width_output = int(width)+40
    height_output = int(height)+40

    image = Image.new("RGB", (width_output, height_output), "white")

    pixels = image.load()

    if m == '0':
        #Compute the cummulated image with parallel ray
        pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)
        pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)    
        image.save('img/nuevaImagen.png', format='PNG')
        
    elif m == '1':
        #Compute the cummulated image with parallel ray
        pixels = ray_tracing(width, height, CHIEF_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)
        pixels = ray_tracing(width, height, PARALLEL_RAY, so, n1, obj, res, pixels, width_output, height_output, si, m, l)    
        image.save('img/nuevaImagenAberracionCorregida.png', format='PNG')