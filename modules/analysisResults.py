import cv2
import matplotlib.pyplot as plt
import pandas as pd

"""En este modulo se grafican todas las imagenes obtenidas y se separan sus canales, 
graficando cada imagen con su respectivo canal en una ventana individual. 
Ademas, se grafican todas las imagenes completas en una sola ventana"""

def figures(url):
    print('\n---------- Graficas ----------\n')
    
    images = pd.read_json("data/images.json") # Se leen los metadatos de las imagenes
    
    # Se define el objeto de observacion 
    if url == 'img/mars.jpg': # ubicacion de la imagen
        images = images.drop('moon', axis=1) # se omite el otro objeto
    elif url == 'img/moon.png': # ubicacion de la imagen
        images = images.drop('mars', axis=1) # se omite el otro objeto
    
    fig4 = plt.figure() # se define la ventana en donde se encuentran todas las imagenes completas
    
    #se grafican las imagenes y la grafica de cada canal
    for j,i in enumerate(images):
        img = cv2.imread(images[i]['url']) #se lee la ubicacion de la imagen
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib (openCV lee en BGR)

        R,G,B = cv2.split(img) # se extraen los canales

        # Se muestran los canales ------------------------
        fig = plt.figure() # se define la ventana grafica

        # Canal rojo
        ax1 = fig.add_subplot(2,2,1) # crea un subgrafico
        ax1.imshow(R, cmap="Reds") # Se grafica el canal
        ax1.set_title("Canal Rojo") # se coloca el titulo de la imagen

        # Canal verde
        ax2 = fig.add_subplot(2,2,2) # ""
        ax2.imshow(G, cmap="Greens") # ""
        ax2.set_title("Canal Verde") # ""

        # Canal azul
        ax3 = fig.add_subplot(2,2,3) # ""
        ax3.imshow(B, cmap="Blues") # ""
        ax3.set_title("Canal Azul") # ""

        ax4 = fig.add_subplot(2,2,4) # crea un subgrafico para la imagen completa
        ax4.imshow(img) # se grafica la imagen 
        ax4.set_title(images[i]['label']) # se coloca el titulo de la imagen
        
        plt.tight_layout() # se separan de manera uniforme los graficos y etiquetas 
        
        # Todas las imagenes ----------
        ax1 = fig4.add_subplot(2,3,j+1) # Se crea el subgrafico de cada cada imagen completa
        ax1.imshow(img) # se grafica la imagen completa
        ax1.set_title(images[i]['label']) # se coloca el titulo de la imagen
    
    fig4.tight_layout() # se separan de manera uniforme los graficos y etiquetas 
    plt.show() # se muestran las ventanas