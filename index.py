from modules import telescope, interpolation, analysisResults, analysisAberration
import pandas as pd

d = True

while d == True:
    print('Escoja el objeto con el que va a trabajar: \n 1. Mars \n 2. Moon')
    ob = input()
    if ob == "1":
        url = 'img/mars.jpg'
        d = False
        
    elif ob == "2":
        url = 'img/moon.png'
        d = False
        
    else:
        print('Por favor ingrese un valor valido')
        d = True
        
d = True

while d == True:
    print('Escoja el tipo de lente con el que va a trabajar: \n 1. Lente delgada \n 2. Lente gruesa')
    lens = input()
    if lens == "1":
        l = 'd'
        d = False
        
    elif lens == "2":
        l = 'g'
        d = False
        
    else:
        print('Por favor ingrese un valor valido')
        d = True
        
d = True
t = True

while d == True:
    
    print('Escoja el sistema de procesamiento: \n 1. Sistema con singletes \n 2. Sistema con tripletes \n 3. Interpolación \n 4. Gráficas \n 5. Sistema aberrado e interpolado \n 6. Sistema sin aberración e interpolado \n 7. Analisis de resultados')
    n = input()
    if(n == '1'):
        telescope.telescope_system('0', l, url)

    elif(n == '2'):
        telescope.telescope_system('1', l, url)
        
    elif(n == '3'):
        print("Elija la imagen a interpolar: \n 1. Imagen Aberrada \n 2. Imagen Sin Aberración")
        m = int(input())
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, m)

    elif(n == '4'):
        analysisResults.figures()
        
    elif(n == '5'):
        telescope.telescope_system('0', l, url)
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 1)
        
    elif(n == '6'):
        telescope.telescope_system('1', l, url)
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 2)
        
    elif(n == '7'):
        telescope.telescope_system('0', l, url)
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 1)
        telescope.telescope_system('1', l, url)
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 2)
        analysisAberration.LCA_num()
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