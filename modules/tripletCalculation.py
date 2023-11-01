import numpy as np

# --------- Convergente ----------------------------------

n = [1.49514, 1.49700, 1.50123]

print('Convergente: ')

#se calcula el radio de la linea d (amarillo)
f = 39190/8161
R = (2*n[1]-2)*f

Rc = R

print('Radio convergente: ', R)

print('Focal amarillo convergente: ', f)

fAc = f

#focal convergente para la linea c (rojo)
f = 1/((n[0] - 1)*(1/R - 1/(-R)))

print('Focal rojo convergente: ', f)

fRc = f

#focal convergente para la linea f (azul)
f = 1/((n[2] - 1)*(1/R - 1/(-R)))

print('Focal azul convergente: ', f)

fBc = f

# --------- Divergente ----------------------------------

print('Divergente: ')

n = [1.69222, 1.69892, 1.71536]

#se calcula el radio de la linea d (amarillo)
f = -3919/604
R = (2-2*n[1])*f

R = Rc

x = 1 - R/(2*f)

print('indice nd: ', x)

print('Radio divergente: ', R)

print('Focal amarillo divergente: ', f)

fAd = f

#focal divergente para la linea c (rojo)
f = 1/((n[0] - 1)*(1/(-R) - 1/(R)))

print('Focal rojo divergente: ', f)

fRd = f

#focal convergente para la linea f (azul)
f = 1/((n[2] - 1)*(1/(-R) - 1/(R)))

print('Focal azul divergente: ', f)

fBd = f

fcs = np.array([4.85959, fAc, 4.645])
fds = np.array([fRd, fAd, fBd])

f = 1/(1/fcs + 2/fds)

print('Focal triplete: ',f)


print('Divergente 2:')



"""#calculo de los radios convergente
R = (2*n-2)*f

#calculo de los radios divergente
R = (2-2*n)*f


R = [0, 0, 0]
#focal convergente
f = 1/((n - 1)*(1/R - 1/(-R)))

#focal divergente
f = 1/((n - 1)*(1/(-R) - 1/(R)))


#indice de refracción convergente
x = 1 + R/(2*f)

#indice de refracción divergente
x = 1 - R/(2*f)"""