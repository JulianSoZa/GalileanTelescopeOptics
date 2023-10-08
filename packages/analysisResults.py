import cv2
import matplotlib.pyplot as plt

# imagen Objeto --------------------------------------------------------------------------------
imgObj = cv2.imread("img/mars.jpg") # matriz principal

imgObj = cv2.cvtColor(imgObj, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib

R,G,B = cv2.split(imgObj) # se extraen los canales

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
ax4.imshow(imgObj)
ax4.set_title("Imagen Objeto")

plt.tight_layout()

# imagen con aberracion sin interpolar --------------------------------------------------------------------------------
imgAbe = cv2.imread("img/nuevaImagen.png") # matriz principal

imgAbe = cv2.cvtColor(imgAbe, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib

R,G,B = cv2.split(imgAbe) # se extraen los canales

# Se muestran los canales ------------------------
fig2 = plt.figure()

# Canal rojo
ax1 = fig2.add_subplot(2,2,1)
ax1.imshow(R, cmap="Reds")
ax1.set_title("Canal Rojo")

# Canal verde
ax2 = fig2.add_subplot(2,2,2)
ax2.imshow(G, cmap="Greens")
ax2.set_title("Canal Verde")

# Canal azul
ax3 = fig2.add_subplot(2,2,3)
ax3.imshow(B, cmap="Blues")
ax3.set_title("Canal Azul")

# Imagen original
ax4 = fig2.add_subplot(2,2,4)
ax4.imshow(imgAbe)
ax4.set_title("Imagen Aberrada")

plt.tight_layout()

# imagen con aberracion interpolada --------------------------------------------------------------------------------
imgAbeInter = cv2.imread("img/nuevaImagenInterpolada.png") # matriz principal

imgAbeInter = cv2.cvtColor(imgAbeInter, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib

R,G,B = cv2.split(imgAbeInter) # se extraen los canales

# Se muestran los canales ------------------------
fig3 = plt.figure()

# Canal rojo
ax1 = fig3.add_subplot(2,2,1)
ax1.imshow(R, cmap="Reds")
ax1.set_title("Canal Rojo")

# Canal verde
ax2 = fig3.add_subplot(2,2,2)
ax2.imshow(G, cmap="Greens")
ax2.set_title("Canal Verde")

# Canal azul
ax3 = fig3.add_subplot(2,2,3)
ax3.imshow(B, cmap="Blues")
ax3.set_title("Canal Azul")

# Imagen original
ax4 = fig3.add_subplot(2,2,4)
ax4.imshow(imgAbeInter)
ax4.set_title("Imagen Aberrada Interpolada")

plt.tight_layout()

# Todas las imagenes --------------------------------------------------------------------------------
# Se muestran los canales ------------------------
fig4 = plt.figure()

ax1 = fig4.add_subplot(2,2,1)
ax1.imshow(imgObj)
ax1.set_title("Imagen Objeto")

ax2 = fig4.add_subplot(2,2,2)
ax2.imshow(imgAbe)
ax2.set_title("Imagen Aberrada")

ax3 = fig4.add_subplot(2,2,3)
ax3.imshow(imgAbeInter)
ax3.set_title("Imagen Aberrada Interpolada")

plt.tight_layout()
plt.show()