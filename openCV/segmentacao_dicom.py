import pydicom
import numpy as np
from rembg import remove
import cv2
from utils import in_file, out_file
import matplotlib.pyplot as plt

def converter_para_hu(ds):
    pixels = ds.pixel_array.astype(np.float32)
    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))
    return pixels * slope + intercept

def aplicar_janela(hu, window_center, window_width):
    min_janela = window_center - window_width / 2
    max_janela = window_center + window_width / 2
    return np.clip(hu, min_janela, max_janela)

def normalizar_para_uint8(img):
    imgf = img.astype(np.float32)
    imgf = (imgf - imgf.min()) / (imgf.max() - imgf.min() + 1e-8)
    return (imgf * 255.0).astype(np.uint8)

def atualizar(x):
    inf = cv2.getTrackbarPos('Inferior', 'Canny')
    sup = cv2.getTrackbarPos('Superior', 'Canny')

    t_kernel = cv2.getTrackbarPos("Tamanho do kernel", "Bordas dilatadas")
    t_kernel_closed = cv2.getTrackbarPos("Tamanho do kernel", "Fechamento")

    iteracoes = cv2.getTrackbarPos("Iterações", "Bordas dilatadas")
    kernel_dilated = np.ones((t_kernel, t_kernel), np.uint8)
    kernel_closed = np.ones((t_kernel_closed, t_kernel_closed), np.uint8)

    img_canny = cv2.Canny(img_blur, inf, sup, apertureSize=3, L2gradient=False)
    dilated = cv2.dilate(img_canny, kernel=kernel_dilated, iterations=iteracoes)
    img_closed = cv2.morphologyEx(img_canny, cv2.MORPH_CLOSE, kernel_closed)

    #detectando contornos mais relevantes para a imagem
    contornos, hierarchy = cv2.findContours(img_closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contornos_fechados = []

    for c in contornos:
        area = cv2.contourArea(c)
        if area > 20:
            contornos_fechados.append(c)

    img_contornada = img_semfundo.copy()
    cv2.drawContours(img_contornada, contornos_fechados, -1, (0, 0, 255), 1)


    # legenda para a imagem com as bordas de canny
    leg_inf = f'Inferior: {inf}'
    cv2.putText(img_canny, leg_inf, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6 ,(255, 255, 255), 1)

    leg_sup = f'Superior: {sup}'
    cv2.putText(img_canny, leg_sup, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

    #legenda para a imagem com as bordas dilatadas
    leg_t_kernel = f'Kernel {t_kernel}x{t_kernel}'
    cv2.putText(dilated, leg_t_kernel, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6 ,(255, 255, 255), 1)

    leg_iteracoes = f'Iterações: {iteracoes}'
    cv2.putText(dilated, leg_iteracoes, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

    #legenda para a imagem com fechamento
    leg_t_kernel_closed = f'Kernel {t_kernel_closed}x{t_kernel_closed}'
    cv2.putText(img_closed, leg_t_kernel_closed, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6 ,(255, 255, 255), 1)

    #exibiçao
    cv2.imshow('Canny', img_canny)
    cv2.imshow("Bordas dilatadas", dilated)
    cv2.imshow("Fechamento", img_closed)
    cv2.imshow("Contornada", img_contornada)

    return img_canny, dilated, img_closed, img_contornada

# ---------- pipeline original (HU -> janela -> remoção de fundo -> Canny) ----------
ds = pydicom.dcmread(in_file('img2.dcm'))

# tirando do arquivo dicom as informações corretas para janelamento 
wc = ds.WindowCenter
ww = ds.WindowWidth

if isinstance(wc, pydicom.multival.MultiValue):
    wc = float(wc[0])

if isinstance(ww, pydicom.multival.MultiValue):
    ww = float(ww[0])

window_center = float(wc)
window_width = float(ww)

img_original = ds.pixel_array
hu = converter_para_hu(ds)
hu_windowed = aplicar_janela(hu, window_center, window_width)
img_window_uint8 = normalizar_para_uint8(hu_windowed)

img_semfundo = remove(img_window_uint8)

img_cinza = cv2.cvtColor(img_semfundo, cv2.COLOR_BGR2GRAY)

# img_mediana = cv2.medianBlur(img_cinza, 3)
img_blur = cv2.GaussianBlur(img_cinza, (3,3), 0)

# Definindo trackbars para as bordas de Canny
cv2.namedWindow("Canny")
cv2.createTrackbar("Inferior", "Canny", 0, 255, atualizar)
cv2.createTrackbar("Superior", "Canny", 0, 255, atualizar)

# Definindo trackbars para a dilatação de bordas
cv2.namedWindow("Bordas dilatadas")
cv2.createTrackbar("Tamanho do kernel", "Bordas dilatadas", 3, 5, atualizar)
cv2.createTrackbar("Iterações", "Bordas dilatadas", 1, 5, atualizar)

# Definindo trackbars para o fechamento
cv2.namedWindow("Fechamento")
cv2.createTrackbar("Tamanho do kernel", "Fechamento", 3, 20, atualizar)


cv2.imshow("Original", img_semfundo)
# cv2.imshow("Mediana", img_mediana)
cv2.imshow("Gaussian Blur", img_blur)

img_canny, img_dilated, img_closed, contornada = atualizar(0)

# o que falta:
# analisar intervalos de cores e segmentar

cv2.waitKey(0)
cv2.destroyAllWindows()
