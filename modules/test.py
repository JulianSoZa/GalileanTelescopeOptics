import numpy as np
import math
import pandas as pd
from PIL import Image #Image file handling
import cv2

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

"""so = 1320

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

print(int([1.5, 1.2]))"""

"""f1 = np.array(df.loc['objective2','mainSystem']['f'])
f2 = np.array(df.loc['eyespace2','mainSystem']['f'])

d = f1 + f2
A = np.array([[-f2/f1, d], [[0, 0, 0], -f1/f2]])

print(A)"""

"""f1 = np.array(df.loc['convergentLens','triplet']['f'])
f2 = np.array(df.loc['divergentLens','triplet']['f'])
f3 = np.array(df.loc['planarConvergentLens','triplet']['f'])

A = np.array([[[1, 1, 1], [0, 0, 0]], [-(f1*f2 + f1*f3 + f2*f3)/(f1*f2*f3), [1, 1, 1]]])
"""
"""so = df.loc['mars','object']['so']
f1 = np.array(df.loc['objective2','mainSystem']['f'])
f2 = np.array(df.loc['eyespace2','mainSystem']['f'])
print(f2)
f3 = 0
si1 = (f1*so)/(so-f1)
print(si1)
so2 = -(si1-(f1+f2))
print(so2)
si2 = (f2*so2)/(-so2-f2)
si = si2"""
"""dE = np.float64(np.array(df.loc['planarConvergentLens','triplet']['d']))
nE = np.float64(np.array(df.loc['planarConvergentLens','triplet']['n']))
nD = np.float64(np.array(df.loc['divergentLens','triplet']['n']))
rD = np.float64(np.array(df.loc['divergentLens','triplet']['R']))
dD = np.float64(np.array(df.loc['divergentLens','triplet']['d']))
nC = np.float64(np.array(df.loc['convergentLens','triplet']['n']))
dC = np.float64(np.array(df.loc['convergentLens','triplet']['d']))
rC = np.float64(np.array(df.loc['convergentLens','triplet']['R']))"""

"""R1 = np.array([[[1, 1, 1], [0, 0, 0]] , [[0, 0, 0], [1, 1, 1]]])
T12 = np.array([[[1, 1, 1], dE/nE] , [[0, 0, 0], [1, 1, 1]]])
R2 = np.array([[[1, 1, 1], [0, 0, 0]] , [(nD-nE)/rD, [1, 1, 1]]])
T23 = np.array([[[1, 1, 1], dD/nD] , [[0, 0, 0], [1, 1, 1]]])
R3 = np.array([[[1, 1, 1], [0, 0, 0]] , [(nC-nD)/(-rD), [1, 1, 1]]])
T34 = np.array([[[1, 1, 1], dC/nC] , [[0, 0, 0], [1, 1, 1]]])
R4 = np.array([[[1, 1, 1], [0, 0, 0]] , [(1-nC)/(rC), [1, 1, 1]]])"""

#res1 = np.einsum('ikj,ilj->ikjl', T12,R2)
"""res3 = np.einsum('ikj,ilj->ilj', res2, T23)
res4 = np.einsum('ikj,ilj->ilj', res3, R3)
res5 = np.einsum('ikj,ilj->ilj', res4, T34)
A = np.einsum('ikj,ilj->ilj', res5, R4)"""

"""A = []
for i in range(3):
    R1 = np.array([[1, 0] , [0, 1]])
    T12 = np.array([[1, dE/nE[i]] , [0, 1]])
    R2 = np.array([[1, 0] , [(nD[i]-nE[i])/rD, 1]])
    T23 = np.array([[1, dD/nD[i]] , [0, 1]])
    R3 = np.array([[1, 0] , [(nC[i]-nD[i])/(-rD), 1]])
    T34 = np.array([[1, dC/nC[i]] , [0, 1]])
    R4 = np.array([[1, 0] , [(1-nC[i])/(rC), 1]])

    A.append(R1@T12@R2@T23@R3@T34@R4)
    
AR, AG, AB = A[0], A[1], A[2]

A = np.array([[[AR[0][0], AG[0][0], AB[0][0]], [AR[0][1], AG[0][1], AB[0][1]]] , [[AR[1][0], AG[1][0], AB[1][0]], [AR[1][1], AG[1][1], AB[1][1]]]])
"""

"""nA = np.array(df.loc['objective2','mainSystem']['n'])
rA = np.array(df.loc['objective2','mainSystem']['R'])
dA = np.array(df.loc['objective2','mainSystem']['d'])
nB = np.array(df.loc['eyespace2','mainSystem']['n'])
rB = np.array(df.loc['eyespace2','mainSystem']['R'])
dB = np.array(df.loc['eyespace2','mainSystem']['d'])

fA = 1/((nA-1)*((1/rA)-(1/(-rA))+(((nA-1)*dA)/(nA*rA*(-rA)))))
fB = 1/((nB-1)*((1/(-rB))-(1/(rB))+(((nB-1)*dB)/(nB*rB*(-rB)))))
print(fB)

A = []
for i in range(3):
    R5 = np.array([[1, 0] , [(nB[i]-1)/(rB), 1]])
    T56 = np.array([[1, dB/nB[i]] , [0, 1]])
    R6 = np.array([[1, 0] , [(1-nB[i])/(-rB), 1]])
    T67 = np.array([[1, fA[i] + fB[i]] , [0, 1]])
    R7 = np.array([[1, 0] , [(nA[i]-1)/(-rA), 1]])
    T78 = np.array([[1, dA/nA[i]] , [0, 1]])
    R8 = np.array([[1, 0] , [(1-nA[i])/(rA), 1]])
    
    A.append(R5@T56@R6@T67@R7@T78@R8)
    
AR, AG, AB = A[0], A[1], A[2]

A = np.array([[[AR[0][0], AG[0][0], AB[0][0]], [AR[0][1], AG[0][1], AB[0][1]]] , [[AR[1][0], AG[1][0], AB[1][0]], [AR[1][1], AG[1][1], AB[1][1]]]])

print(A)
"""

"""dE = np.array(df.loc['planarConvergentLens','triplet']['d'])
nE = np.array(df.loc['planarConvergentLens','triplet']['n'])
rE = np.array(df.loc['planarConvergentLens','triplet']['R'])
nD = np.array(df.loc['divergentLens','triplet']['n'])
rD = np.array(df.loc['divergentLens','triplet']['R'])
dD = np.array(df.loc['divergentLens','triplet']['d'])
nC = np.array(df.loc['convergentLens','triplet']['n'])
dC = np.array(df.loc['convergentLens','triplet']['d'])
rC = np.array(df.loc['convergentLens','triplet']['R'])

f3 = 1/((nE-1)*(1/rE))
f2 = 1/((nD-1)*((1/(-rD))-(1/(rD))+(((nD-1)*dD)/(nD*rD*(-rD)))))
f1 = 1/((nC-1)*((1/rC)-(1/(-rC))+(((nC-1)*dC)/(nC*rC*(-rC)))))

print(f1, f2, f3)"""

n1O =  np.array(df.loc['convergentLens','objetiveTriplet']['n'])
r1O = df.loc['convergentLens','objetiveTriplet']['R']
d1O = df.loc['convergentLens','objetiveTriplet']['d']

n2O =  np.array(df.loc['divergentMeniscusLens','objetiveTriplet']['n'])
r2O = df.loc['divergentMeniscusLens','objetiveTriplet']['R']
d2O = df.loc['divergentMeniscusLens','objetiveTriplet']['d']

n3O =  np.array(df.loc['concavePlaneLens','objetiveTriplet']['n'])
r3O = df.loc['concavePlaneLens','objetiveTriplet']['R']
d3O = df.loc['concavePlaneLens','objetiveTriplet']['d']

# --- Ocular -----
n1e =  np.array(df.loc['divergentLens','eyespaceTriplet']['n'])
r1e = df.loc['divergentLens','eyespaceTriplet']['R']
d1e = df.loc['divergentLens','eyespaceTriplet']['d']

n2e = np.array(df.loc['convergentMeniscusLens','eyespaceTriplet']['n'])
r2e = df.loc['convergentMeniscusLens','eyespaceTriplet']['R']
d2e = df.loc['convergentMeniscusLens','eyespaceTriplet']['d']

n3e = np.array(df.loc['convexPlaneLens','eyespaceTriplet']['n'])
r3e = df.loc['convexPlaneLens','eyespaceTriplet']['R']
d3e = df.loc['convexPlaneLens','eyespaceTriplet']['d']

fo = 1/(1/((n1O - 1)*(1/r1O - 1/r2O + (n1O - 1)*d1O/(n1O*r1O*r2O))) + 1/((n2O - 1)*(1/r2O - 1/r3O + (n2O - 1)*d2O/(n2O*r2O*r3O))) + 1/((n3O - 1)*(1/r3O)))
fo1 = 1/((n1O - 1)*(1/r1O - 1/r2O + (n1O - 1)*d1O/(n1O*r1O*r2O)))
f02 = 1/((n2O - 1)*(1/r2O - 1/r3O + (n2O - 1)*d2O/(n2O*r2O*r3O)))
f03 = 1/((n3O - 1)*(1/r3O))

fo = (1/fo1 + 2)
fe = 1/(1/((n1e - 1)*(1/r1e - 1/r2e + (n1e - 1)*d1e/(n1e*r1e*r2e))) + 1/((n2e - 1)*(1/r2e - 1/r3e + (n2e - 1)*d2e/(n2e*r2e*r3e))) + 1/((n3e - 1)*(1/r3e)))
print('fo', 1/((n3O - 1)*(1/r3O)))
print('fe', fe)