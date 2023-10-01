import cv2
import numpy as np
import matplotlib.pyplot as plt

# imagen
img = cv2.imread("img/nuevaImagenInterpolada.png") # matriz principal

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib

#print(img)
#print(img[182][250]) # pixel especifico

R,G,B = cv2.split(img) # se extraen los canales

print("Rojo: ",R)

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
ax4.set_title("Imagen completa")
#imgre = cv2.merge((B,G,R)) # para reconstruccion (BGR)
#cv2.imwrite("img/nuevaImagen.png", B) # se guarda la imagen

plt.tight_layout()
plt.show()