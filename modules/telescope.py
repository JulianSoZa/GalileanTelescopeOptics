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
        width_output = int(width)+40
        height_output = int(height)+40

    elif m == '1':
        so = [so, so, so]
        f1 = np.array(df.loc['convergentLens','objetiveTriplet']['f'])
        f2 = np.array(df.loc['divergentMeniscusLens','objetiveTriplet']['f'])
        f3 = np.array(df.loc['concavePlaneLens','objetiveTriplet']['f'])
        
        fo = 1/(1/f1 + 1/f2 + 1/f3)
        
        f1 = np.array(df.loc['divergentLens','eyespaceTriplet']['f'])
        f2 = np.array(df.loc['convergentMeniscusLens','eyespaceTriplet']['f'])
        f3 = np.array(df.loc['convexPlaneLens','eyespaceTriplet']['f'])
        
        fe = 1/(1/f1 + 1/f2 + 1/f3)
        
        si1 = (fo*so)/(so-fo)
        so2 = -(si1-(fo+fe))
        si2 = (fe*so2)/(so2-fe)
    
        print("si2: ", si2)
        
        si = si2
        
        """d1 = df.loc['convergentLens','triplet']['d']
        d2 = df.loc['divergentLens','triplet']['d']
        d3 = df.loc['planarConvergentLens','triplet']['d']

        so = 18*2 + (d1+d2+d3)/2 - si2
        
        if l == 'd':
            f1 = np.array(df.loc['convergentLens','triplet']['f'])
            f2 = np.array(df.loc['divergentLens','triplet']['f'])
            f3 = np.array(df.loc['planarConvergentLens','triplet']['f'])
            
        elif l == 'g':
            dE = np.array(df.loc['planarConvergentLens','triplet']['d'])
            nE = np.array(df.loc['planarConvergentLens','triplet']['n'])
            rE = np.array(df.loc['planarConvergentLens','triplet']['R'])
            nD = np.array(df.loc['divergentLens','triplet']['n'])
            rD = np.array(df.loc['divergentLens','triplet']['R'])
            dD = np.array(df.loc['divergentLens','triplet']['d'])
            nC = np.array(df.loc['convergentLens','triplet']['n'])
            dC = np.array(df.loc['convergentLens','triplet']['d'])
            rC = np.array(df.loc['convergentLens','triplet']['R'])
            
            f3 = 1/((nE-1)*(1/rE))
            f2 = 1/((nD-1)*((1/(-rD))-(1/(rD))+(((nD-1)*dD)/(nD*rD*(-rD)))))
            f1 = 1/((nC-1)*((1/rC)-(1/(-rC))+(((nC-1)*dC)/(nC*rC*(-rC)))))

        f = 1/((1/f1)+(1/f2)+(1/f3))

        si = (f*so)/(so-f)
        print("so: ", so)
        print("si: ", si)"""
        
        width_output = int(width)
        height_output = int(height)

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