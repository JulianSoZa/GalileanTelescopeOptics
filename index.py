from modules import telescope, interpolation, analysisResults, analysisAberration
import pandas as pd


"""Aqui el usuario puede seleccionar distintas opciones para el funcionamiento del telescopio, como el objeto a observar, el tipo de lente 
y los distintos resultados que puede obtener."""


d = True #variable para el primer bucle

while d == True: # Bucle para que el usuario elija un objeto astronómico (Marte o Luna).
    print('Escoja el objeto con el que va a trabajar: \n 1. Mars \n 2. Moon')
    ob = input()
    if ob == "1":  #Si el usuario indica 1 se establece la URL de la imagen de Marte.
        url = 'img/mars.jpg'
        d = False
        
    elif ob == "2": #Si el usuario indica 2 se establece la URL de la imagen de la Luna.
        url = 'img/moon.png'
        d = False
        
    else:
        print('Por favor ingrese un valor valido') #Si el usuario indica otro valor este le dice que agregue uno valido.
        d = True
        
d = True #variable para el segundo bucle

while d == True: # Bucle para que el usuario elija el tipo de lente (delgada o gruesa).
    print('Escoja el tipo de lente con el que va a trabajar: \n 1. Lente delgada \n 2. Lente gruesa')
    lens = input()
    if lens == "1":
        l = 'd' #Si el usuario indica 1 el codigo funciona para lente delgada.
        d = False
        
    elif lens == "2":
        l = 'g' #Si el usuario indica 2 el codigo funciona para lente gruesa.
        d = False
        
    else:
        print('Por favor ingrese un valor valido')  #Si el usuario indica otro valor este le dice que agregue uno valido.
        d = True
        
d = True
t = True #Variables del bucle

while d == True: # Bucle para que el usuario elija una operacion a realizar.
    
    print('Escoja el sistema de procesamiento: \n 1. Sistema con singletes \n 2. Sistema con tripletes \n 3. Interpolación \n 4. Gráficas (asegurese de tener las imagenes que requiere) \n 5. Sistema aberrado e interpolado \n 6. Sistema sin aberración e interpolado \n 7. Analisis de resultados')
    n = input()
    if(n == '1'):
        telescope.telescope_system('0', l, url) # Si el usuario indica 1 llama a la funcion para el sistema con singletes.

    elif(n == '2'):
        telescope.telescope_system('1', l, url) # Si el usuario indica 2 llama a la funcion para el sistema con tripletes.

        
    elif(n == '3'):
        print("Elija la imagen a interpolar: \n 1. Imagen Aberrada \n 2. Imagen Sin Aberración") 
        m = int(input())
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada'] #lista de las imagenes creadas.
        interpolation.interpolation_system(imgName, m) # Llama a la función para la interpolacion de imagenes.

    elif(n == '4'):
        analysisResults.figures(url)  # Llama a la función para mostrar los graficos.
        
    elif(n == '5'):
        telescope.telescope_system('0', l, url)
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 1) # # Sistema aberrado e interpolado.
        
    elif(n == '6'):
        telescope.telescope_system('1', l, url)
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 2) # # Sistema sin aberracion e interpolado
        
    elif(n == '7'):
        telescope.telescope_system('0', l, url) #Llama a la función telescope.telescope_system usando singlete.
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada'] #lista con los nombres de las imagenes a aprocesar.
        interpolation.interpolation_system(imgName, 1) # 1 indica que se realizara la interpolación en una imagen aberrada.
        telescope.telescope_system('1', l, url) ##Llamar a la función telescope.telescope_system usando triplete.
        imgName = ['nuevaImagen', 'nuevaImagenAberracionCorregida', 'nuevaImagenAberradaInterpolada', 'nuevaImagenSinAberracionInterpolada']
        interpolation.interpolation_system(imgName, 2) # 1 indica que se realizara la interpolación en una imagen sin aberración.
        analysisAberration.LCA_num() #llama a la funcion de LCA.
        analysisResults.figures(url) #muestra las graficas de los resultados.

    else:
        print('Por favor ingrese un valor valido') #Si el usuario indica otro valor este le dice que agregue uno valido.
        t=False
        pass
    
    while t==True: #si el usuario no ingreso un valor valido le pregunta si desea continuar o salir
        print('¿Desea continuar? \n y.  n.')
        q=input()
        if q=='n': # Si el usuario ingresa n, se establece d en False para salir del bucle principal.
            d=False
        break
