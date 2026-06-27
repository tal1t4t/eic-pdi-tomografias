from utils import in_file, out_file
from PIL import Image
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

# kernel do filtro gaussiano para suavizar imagem
def gaussian_kernel(size, sigma=1):
    size = int(size) // 2
    x, y = np.mgrid[-size:size+1, -size:size+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    return g


def sobel_filters(img):
    kx = np.array([[-1, 0, 1],
                          [-2, 0, 2],
                          [-1, 0, 1]], np.float32)
    ky = np.array([[1, 2, 1],
                          [0, 0, 0],
                          [-1, -2, -1]], np.float32)

    #passando as máscaras de convolução pela imagem toda, na horizontal e na vertical
    ix = ndimage.filters.convolve(img, kx)
    iy = ndimage.filters.convolve(img, ky)

    # fórmula do módulo do vetor para extrair a força total do contorno no pixel, tipo raiz de a²+b²
    g = np.hypot(ix, iy)
    g = g / g.max() * 255 # deixa os resultados no intervalo [0, 255]
    theta = np.arctan2(iy, ix) # ângulo do gradiente

    return g, theta


def aplicar_filtro(img, kernel):
    k = kernel.shape[0] // 2
    saida = np.zeros_like(img, dtype=np.float32)

    # Adiciona bordas à imagem
    img_padded = np.pad(img, k, mode='reflect')

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            regiao = img_padded[i:i+2*k+1, j:j+2*k+1]
            saida[i, j] = np.sum(regiao * kernel)

    return saida

#afina as bordas
def non_max_suppression(img, D):
    M, N = img.shape
    Z = np.zeros((M, N), dtype=np.int32)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            try:
                q = 255
                r = 255

                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = img[i, j + 1]
                    r = img[i, j - 1]
                # angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    q = img[i + 1, j - 1]
                    r = img[i - 1, j + 1]
                # angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    q = img[i + 1, j]
                    r = img[i - 1, j]
                # angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    q = img[i - 1, j - 1]
                    r = img[i + 1, j + 1]

                if (img[i, j] >= q) and (img[i, j] >= r):
                    Z[i, j] = img[i, j]
                else:
                    Z[i, j] = 0

            except IndexError as e:
                pass

    return Z

#usando limite duplo para separar as bordas em fortes, médias e fracas a partir dos limiares passados nos parâmetros
#se for necessário, calibre o filtro inserindo outros valores nos Ratios
def threshold(img, lowThresholdRatio=0.05, highThresholdRatio=0.05):
    highThreshold = img.max() * highThresholdRatio #detecta o pixel de maior valor e calcula o limiar a partir dele
    lowThreshold = highThreshold * lowThresholdRatio
    #calcula o limiar para pixels fracos a partir do limiar para pixels fortes

    M, N = img.shape
    # cria uma nova matriz com o mesmo tamanho da imagem, mas preenchida com zeros
    res = np.zeros((M, N), dtype=np.int32)

    #armazena as coordenadas de pixels fortes
    strong_i, strong_j = np.where(img >= highThreshold)

    #armazena as coordenadas de pixels fracos
    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

    #armazena as coordenadas de ruídos
    zeros_i, zeros_j = np.where(img < lowThreshold)

    weak = np.int32(150) # valor para realçar bordas fracas
    strong = np.int32(255) # branco total para destacar bordas fortes

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    return res, weak, strong

def hysteresis(img, weak, strong=255):
# analisa os pixels fracos verificando se ao redor deles há pelo menos um pixel forte.
# se houver, este pixel passa a ser forte também
    M, N = img.shape
    for i in range(1, M-1):
        for j in range(1, N-1):
            if img[i,j] == weak:
                try:
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img


def bordas_vermelhas(img_cinza):
    x, y = img_cinza.shape #registrando tamanho da imagem
    RED = (255, 0, 0, 255)
    TRANSP = (255, 255, 255, 0)

    img_contorno_vermelho = Image.new("RGBA", (x, y))


    for i in range(0, x):
        for j in range(0, y):
            # verificando onde há pixels brancos na imagem binária para substituir por pixels vermelhos
            if img_cinza[j, i] == 255:
                img_contorno_vermelho.putpixel((i, j), RED)
            else:
                img_contorno_vermelho.putpixel((i, j), TRANSP)

    img_contorno_vermelho.save(out_file("contorno_vermelho_im2_gauss6_005_005.png"))
    return img_contorno_vermelho


#---------------------------
# lendo a imagem e aplicando os filtros
#---------------------------

if __name__ == '__main__':
    original = np.array(Image.open(in_file("segmentada1.png")).convert('L'))
    original = original.astype(float)

    kernel_g = gaussian_kernel(3)
    kernel_g /= kernel_g.sum()
    gaussiano = aplicar_filtro(original, kernel_g)

    sobel, theta_s = sobel_filters(gaussiano)

    non_max = non_max_suppression(sobel, theta_s)

    limite_duplo, pixel_fraco, pixel_forte = threshold(non_max)

    histerese = hysteresis(limite_duplo, pixel_fraco, pixel_forte)

    vermelha = bordas_vermelhas(histerese)

    resp = int(input("[1] Ver processo completo\n[2] comparar imagem original com contorno sobreposto\nSua resposta: "))
    if resp == 1:
        fig, ax = plt.subplots(4, 2, figsize=(50, 25))

        ax[0, 0].imshow(original, cmap='gray')
        ax[0, 0].set_title("Original")
        ax[0, 0].axis('off')

        ax[0, 1].imshow(gaussiano, cmap='gray')
        ax[0, 1].set_title("Filtro Gaussiano")
        ax[0, 1].axis('off')

        ax[1, 0].imshow(sobel, cmap='gray')
        ax[1, 0].set_title("Filtro Sobel")
        ax[1, 0].axis('off')

        ax[1, 1].imshow(non_max, cmap='gray')
        ax[1, 1].set_title("Supressão de não-máximos \nsobre filtro sobel")
        ax[1, 1].axis('off')

        ax[2, 0].imshow(limite_duplo, cmap='gray')
        ax[2, 0].set_title("Limite duplo sobre \nsupressão de não-máximos")
        ax[2, 0].axis('off')

        ax[2, 1].imshow(histerese, cmap='gray')
        ax[2, 1].set_title("Histerese sobre limite duplo")
        ax[2, 1].axis('off')

        ax[3, 0].imshow(vermelha)
        ax[3, 0].set_title("bordas em vermelho")
        ax[3, 0].axis('off')

        ax[3, 1].imshow(original, cmap='gray')
        ax[3, 1].imshow(vermelha)
        ax[3, 1].axis('off')

        plt.tight_layout()
        plt.show()

    elif resp == 2:
        fig, ax = plt.subplots(1, 2, figsize=(40, 20))

        ax[0].imshow(original, cmap="gray")
        ax[0].set_title("Original")
        ax[0].axis("off")

        ax[1].imshow(original, cmap="gray")
        ax[1].imshow(vermelha)
        ax[1].set_title("Sobreposição do contorno vermelho")
        ax[1].axis("off")

        plt.tight_layout()
        plt.show()
    else:
        print("comando inválido")
