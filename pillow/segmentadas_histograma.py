from utils import in_file, out_file
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
#import pydicom

#DICOM
#img = (pydicom.dcmread(in_file("img2.dcm")))
#img = img.pixel_array

#PNG
img = np.array(Image.open(in_file("img2.png")).convert('L'))

def calcula_frequencias():
    img_1d = img.ravel() #transforma a matriz num array 1D

    #np.unique retorna 2 arrays: um com os valores encontrados, e outro com suas respectivas frequências
    valores, frequencia = np.unique(img_1d, return_counts=True)
    print(np.size(valores), " valores encontrados.")

    for i in range(0, np.size(valores)):
        print(valores[i], ": ", frequencia[i], " vezes")


def exibir_imagem_histograma():
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    ax[0].imshow(img, cmap="gray")
    ax[0].axis("off")
    ax[0].set_title("Imagem em escala de cinza")

    ax[1].hist(img.ravel(), bins=range(256), color="black")
    ax[1].set_title("Frequência de cada cor")

    plt.tight_layout()
    plt.show()


def freq_teste():
    arr = np.array([1,3,6,6,3,5,8,1,1,2])
    valores, frequencia = np.unique(arr, return_counts=True)
    print(np.size(valores), " valores encontrados: ", valores)
    print("Valores e frequência na imagem: \n")

    print(valores, ": ", frequencia, " vezes")