import cv2
import pandas as pd
import numpy as np

def LCA_num():
    print('\n---------- Analisis de la aberracion de las imganes por pixels ----------\n')
    
    images = pd.read_json("data\images.json")

    for j,i in enumerate(images):
        if i=='nuevaImagenAberradaInterpolada':
            img = cv2.imread(images[i]['url'])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib
            Ra, Ga, Ba =cv2.split(img)
                
        elif i=='nuevaImagenSinAberracionInterpolada':  
            img = cv2.imread(images[i]['url'])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib
            R, G, B =cv2.split(img)    
            
    l, l1=np.shape(R)
    
    for j in range(l):
            u=int((l/2)-1)  # Selecciona una fila específica (fila del medio)

            # Abb: NDArray[float64]=np.zeros(l)
            Yar = Ra[u][j]
            Yab = Ba[u][j]
            Yr = R[u][j]
            Yb = B[u][j]

            if Yar != 127: # Analiza los valores de pixeles en las coordenadas especificas y determina que son valores distintos de 127
                yr=j

            if Yab != 127:
                yb =j    

            if Yr !=127:
                yr2=j

            if Yb != 127:
                yb2 = j     
                
    LCA = yr - yb # Calcula la aberración cromática lateral de la imagen aberrada
    LCA2 = yr2 - yb2  # Calcula la aberración cromática lateral de la imagen con aberracion corregida

    print(f'Aberracion cromatica lateral de la imagen aberrada: {LCA} px \nAberracion cromatica lateral de la imagen corregida: {LCA2} px')


