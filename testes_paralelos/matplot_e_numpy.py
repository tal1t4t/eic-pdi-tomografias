from cProfile import label

import matplotlib.pyplot as plt
import numpy as np
from fontTools.diff import color
from numpy.ma.core import size


def linha():
    plt.plot([1, 2, 3, 4]) # exibe um gráfico em linha

def pontos():
    plt.plot([1, 2, 3, 4], "ro") # exibe só os pontos no gráfico

def subplots():

    x = np.arange(0, 10, 0.1)
    # cria um array que vai de o até 10, crescendo de 0.1 em 0.1

    fig1, f1_axes = plt.subplots(ncols=2, nrows=2, figsize=(15, 10))
    #retorna um ponteiro para a figura 1 e um array para o endereço dos axes
    #figsize determina o tamanho da figura
    fig1.suptitle("Testando matplotlib", size=30)

    f1_axes[0, 0].plot(np.sin(x),
                       label="sen(x)",
                       color="darkcyan") # função sen(x) do numpy com legenda definida no gráfico
    f1_axes[0, 0].set_title("Caixa 1",
                            size=15)
    f1_axes[0, 0].set_xlabel("testando label x")
    f1_axes[0, 0].set_ylabel("testando label y")
    f1_axes[0, 0].plot(np.cos(x),
                       label="cos(x)",
                       color="mediumslateblue") # dá pra sobrepôr gráficos :D
    f1_axes[0, 0].legend() # pega os labels de cada plot e cria a legenda do gráfico

    f1_axes[0, 1].plot(np.cos(x)) # função cos(x) do numpy
    f1_axes[0, 1].plot(np.arccos(x)) # função cos(x) do numpy
    f1_axes[0, 1].set_title("Função cosseno",
                            size=15)

    f1_axes[1, 0].plot(np.tan(x)) # função tan(x) do numpy
    f1_axes[1, 0].set_title("Função tangente",
                            size=15)

subplots()

plt.show()