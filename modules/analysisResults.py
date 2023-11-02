import cv2
import matplotlib.pyplot as plt
import pandas as pd

def figures():
    print('\n---------- Graficas ----------\n')
    
    images = pd.read_json("data/images.json")
    
    fig4 = plt.figure()
    
    for j,i in enumerate(images):
        img = cv2.imread(images[i]['url'])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib

        R,G,B = cv2.split(img) # se extraen los canales

        # Se muestran los canales ------------------------
        fig = plt.figure()

        # Canal rojo
        ax1 = fig.add_subplot(2,2,1)
        ax1.imshow(R, cmap="Reds")
        ax1.set_title("Canal Rojo")

        # Canal verde
        ax2 = fig.add_subplot(2,2,2)
        ax2.imshow(G, cmap="Greens")
        ax2.set_title("Canal Verde")

        # Canal azul
        ax3 = fig.add_subplot(2,2,3)
        ax3.imshow(B, cmap="Blues")
        ax3.set_title("Canal Azul")

        # Imagen original
        ax4 = fig.add_subplot(2,2,4)
        ax4.imshow(img)
        ax4.set_title(images[i]['label'])
        
        plt.tight_layout()
        
        # Todas las imagenes ----------
        ax1 = fig4.add_subplot(2,3,j+1)
        ax1.imshow(img)
        ax1.set_title(images[i]['label'])
    
    fig4.tight_layout()
    plt.show()