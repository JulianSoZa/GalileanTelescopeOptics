from modules import main, triplet, interpolation, analysisResults
import pandas as pd

print('Escoja el sistema de procesamiento: \n 1. Sistema Principal \n 2. Sistema Triplete \n 3. Interpolación \n 4. Gráficas')
n = input()

if(n == '1'):
    main.main_system()

elif(n == '2'):
    triplet.triplet_system()
    
elif(n == '3'):
    print("Elija la imagen a interpolar: \n 1. Imagen Aberrada \n 2. Imagen Sin Aberración")
    m = int(input())
    imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
    interpolation.interpolation_system(imgName, m)

elif(n == '4'):
    analysisResults.figures()