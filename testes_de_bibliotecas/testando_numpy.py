import numpy as np
'''
v1 = np.array([3, 5, 7]) #criando variável do tipo array do numpy
v2 = np.array([1, -4, 8])

print("v1 = ", v1)
print("v2 = ", v2, "\n")

print("Soma vetorial: ",v1 + v2)
print("Subtração v1 - v2: ", v1 - v2)
print("Multiplicação de v1 por 4: ", v1 * 4)
print("Prod. Escalar v1 . v2: ", np.dot(v1, v2))
'''
mat1 = np.array([[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]])

mat2 = np.eye(3) # cria uma matriz identidade com a ordem expressa no parâmetro

print(mat1)
print(mat2)
print(mat1 @ mat2) # multiplicação entre as duas matrizes. tambem dá pra usar np.matmul(mat1, mat2)

print("Média dos valores de mat1: ", mat1.mean())
print("Maior valor em mat1: ", mat1.max())