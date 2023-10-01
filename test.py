import numpy as np
import math

y_objeto = 80
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
print(sol)