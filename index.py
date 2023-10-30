from modules import telescope, interpolation, analysisResults
import pandas as pd

d=True
t=True
while d==True:
    print('Escoja el sistema de procesamiento: \n 1. Sistema Principal \n 2. Sistema Triplete \n 3. Interpolación \n 4. Gráficas \n 5. Sistema aberrado e interpolado \n 6. Sistema sin aberración e interpolado \n 7. Analisis de resultados')
    n=input()
    if(n == '1'):
        telescope.telescope_system('0')

    elif(n == '2'):
        telescope.telescope_system('1')
        
    elif(n == '3'):
        print("Elija la imagen a interpolar: \n 1. Imagen Aberrada \n 2. Imagen Sin Aberración")
        m = int(input())
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, m)

    elif(n == '4'):
        analysisResults.figures()
        
    elif(n == '5'):
        telescope.telescope_system('0')
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 1)
        
    elif(n == '6'):
        telescope.telescope_system('1')
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 2)
        
    elif(n == '7'):
        telescope.telescope_system('0')
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 1)
        telescope.telescope_system('1')
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 2)
        analysisResults.figures()

    else:
        print('Por favor ingrese un valor valido')
        t=False
        pass
    
    while t==True:
        print('¿Desea continuar? \n y.  n.')
        q=input()
        if q=='n':
            d=False
        break