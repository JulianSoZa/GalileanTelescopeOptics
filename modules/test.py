import numpy as np
import math
import pandas as pd
import cv2
import pandas as pd

"""y_objeto = 80
n1 = 1
alpha_entrada = 0.060532
si = -9.93334
so = 1320
P2 = np.array([[[1, 1, 1], [si/n1, si/n1, si/n1]],[[0, 0, 0], [1, 1, 1]]])
P1 = np.array([[[1, 1, 1], [so/n1, so/n1, so/n1]],[[0, 0, 0], [1, 1, 1]]])
V_entrada = np.array([[y_objeto, y_objeto, y_objeto], [n1*alpha_entrada, n1*alpha_entrada, n1*alpha_entrada]])
A = np.array([[[1/70, 0.0144265, 0.0148487], [690, 690, 690]], [[0, 0, 0], [70, 69.3168, 67.3462]]])
#V_salida = P2*(A*(P1*(V_entrada)))
#res = np.einsum('ijk,jk->ij', P1, V_entrada)
res = np.einsum('ikj,kj->ij', P1, V_entrada)
#res = np.einsum('kij,kj->kj', P1, V_entrada)

res2 = np.einsum('ikj,kj->ij', A, res)

res3 = np.einsum('ikj,kj->ij', P2, res2)

sol = np.einsum('ba, ced, fhg, ikj->ij', V_entrada, P1, A, P2)
print(sol)"""
"""so = 1324.817172
f1 = 700
f2 = -10
si1 = (f1*so)/(so-f1)
so2 = si1-(f1+f2)
si2 = (f2*si1)/(si1-f2)

print(si2)"""

"""df = pd.read_json("data/lenses.json")
so = 1320

f1 = df.loc['objective2','mainSystem']['f']
f2 = df.loc['eyespace2','mainSystem']['f']

print(f1, f2)

si1 = [(f1[0]*so)/(so-f1[0]), (f1[1]*so)/(so-f1[1]), (f1[2]*so)/(so-f1[2])]
so2 = [-(si1[0]-(f1[0]+f2[0])), -(si1[1]-(f1[1]+f2[1])), -(si1[2]-(f1[2]+f2[2]))]
si2 = [(f2[0]*so2[0])/(so2[0]-f2[0]), (f2[1]*so2[1])/(so2[1]-f2[1]), (f2[2]*so2[2])/(so2[2]-f2[2])]

print(si2)"""

"""images = pd.read_json("data/images.json")

for j,i in enumerate(images):
    print(i,j)
    img = cv2.imread(images[i]['url'])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # se corrige para poder usar matplotlib
    """

df = pd.read_json("data/lenses.json") 

so = 1320

f1 = np.array(df.loc['objective2','mainSystem']['f'])
f2 = np.array(df.loc['eyespace2','mainSystem']['f'])

si1 = (f1*so)/(so-f1)
so2 = -(si1-(f1+f2))
si2 = (f2*so2)/(so2-f2)

d1 = df.loc['convergentLens','triplet']['d']
d2 = df.loc['divergentLens','triplet']['d']
d3 = df.loc['planarConvergentLens','triplet']['d']

so = 18 + (d1+d2+d3)/2 - si2

f1 = np.array(df.loc['convergentLens','triplet']['f'])
f2 = np.array(df.loc['divergentLens','triplet']['f'])
f3 = np.array(df.loc['planarConvergentLens','triplet']['f'])

f = [1/((1/f1[0])+(1/f2[0])+(1/f3[0])), 1/((1/f1[1])+(1/f2[1])+(1/f3[1])), 1/((1/f1[2])+(1/f2[2])+(1/f3[2]))]

si = [(f[0]*so[0])/(so[0]-f[0]), (f[1]*so[1])/(so[1]-f[1]), (f[2]*so[2])/(so[2]-f[2])]

print(si)

f = 1/((1/f1)+(1/f2)+(1/f3))

si = (f*so)/(so-f)

print(si)

print(int([1.5, 1.2]))