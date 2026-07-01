#código base: https://medium.com/@vignesh.g1609/image-segmentation-using-otsu-threshold-selection-method-856ccdacf22

from utils import out_file, in_file
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

#limiarização
def threshold_image(im, th):
    #cria matriz vazia com o tamanho da imagem
    thresholded_im = np.zeros(im.shape)

    # se o pixel da imagem for maior q o limiar, ele recebe 1
    thresholded_im[im >= th] = 1

    #retorna imagem binária num array numpy
    return thresholded_im

#critério de otsu
def compute_otsu_criteria(im, th):
    thresholded_im = threshold_image(im, th)
    nb_pixels = im.size #coletando o nº total de pixels da imagem

    #conta a qtd de pixels que ficaram com valor 1
    nb_pixels1 = np.count_nonzero(thresholded_im)

    weight1 = nb_pixels1 / nb_pixels

    weight0 = 1 - weight1

    if weight1 == 0 or weight0 == 0:
        return np.inf

    val_pixels1 = im[thresholded_im == 1]
    val_pixels0 = im[thresholded_im == 0]

    var0 = np.var(val_pixels0) if len(val_pixels0) > 0 else 0
    var1 = np.var(val_pixels1) if len(val_pixels1) > 0 else 0

    return weight0 * var0 + weight1 * var1

def find_best_threshold(im):
    threshold_range = range(int(np.max(im)) + 1)
    criterias = [compute_otsu_criteria(im, th) for th in threshold_range]
    best_threshold = threshold_range[np.argmin(criterias)]
    return best_threshold

def exibe_resultado(im, im_otsu):
    fig, ax = plt.subplots(1, 2, figsize=(20,10))

    ax[0].imshow(im, cmap='gray')
    ax[0].set_title("Original")
    ax[0].axis("off")

    ax[1].imshow(im_otsu, cmap='gray')
    ax[1].set_title("Imagem com método de Otsu")
    ax[1].axis("off")

    plt.tight_layout()
    plt.show()

def abre_imagem(img):
    im = np.asarray(Image.open(in_file(img)).convert('L'))
    return im

def salva_imagem_otsu(im_otsu, nome_img):
    x, y = im_otsu.shape
    png_otsu = Image.new('RGBA', (x, y))

    TRANSP = (255, 255, 255, 0)
    WHITE = (255, 255, 255, 255)
    
    for i in range(x):
        for j in range(y):
            png_otsu.putpixel((j, i), WHITE) if im_otsu[i, j] == 1 else png_otsu.putpixel((j, i), TRANSP)

    nome_tratado = nome_img[:-4]
    png_otsu.save(out_file(f'{nome_tratado}_otsu.png'))

if __name__ == "__main__":
    nome_img = 'img2.png'
    im = abre_imagem(nome_img)
    im_otsu = threshold_image(im, find_best_threshold(im))

    exibe_resultado(im, im_otsu)
    salva_imagem_otsu(im_otsu, nome_img)