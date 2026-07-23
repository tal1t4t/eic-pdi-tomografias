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

def analisar_e_colorir_contornos(contornos, hu, formato_img, usar_colormap=True):
 
    # Para cada contorno, extrai a faixa de valores HU dentro dele e
    # define uma cor com base nessa faixa.
 
    img_colorida = np.zeros((*formato_img, 3), dtype=np.uint8)
    info_contornos = []

    # Faixas de HU aproximadas (ajuste conforme sua necessidade)
    faixas_hu = [
        ("ar", -1000, -500, (0, 0,   0)),   # preto
        ("agua", 0, 10, (245, 167, 66)),   # azul claro
        ("massa_branca", 20, 30, (0, 255, 0)), # verde
        ("massa_cinzenta",   37, 45, (255, 255, 0)),   # ciano
        ("sangue_coagulado",  50,  75, (0,   255, 255)), # amarelo
        ("osso",           200, 3000, (0,   0,   255)),# vermelho
    ]

    def classificar_por_faixa(valor_medio):
        for nome, minimo, maximo, cor in faixas_hu:
            if minimo <= valor_medio < maximo:
                return nome, cor
        return "indefinido", (128, 128, 128)  # cinza

    for i, c in enumerate(contornos):
        # máscara apenas para esse contorno, preenchido
        mask = np.zeros(formato_img, dtype=np.uint8)
        cv2.drawContours(mask, [c], -1, 255, thickness=cv2.FILLED)

        valores = hu[mask == 255]
        if valores.size == 0:
            continue

        v_min, v_max = valores.min(), valores.max()
        v_media = valores.mean()
        v_mediana = np.median(valores)

        if usar_colormap:
            # normaliza a média para 0-255 dentro de uma faixa de interesse
            # (ex: -200 a 400 HU cobre a maior parte de tecidos moles/ósseos)
            norm = np.clip((v_media - (-200)) / (400 - (-200)), 0, 1)
            valor_uint8 = np.uint8(norm * 255)
            # cv2.applyColorMap espera um array; pegamos a cor de 1 pixel
            cor_bgr = cv2.applyColorMap(np.array([[valor_uint8]], dtype=np.uint8),
                                         cv2.COLORMAP_JET)[0, 0].tolist()
            nome = "colormap"
        else:
            nome, cor_bgr = classificar_por_faixa(v_media)

        # pinta a região do contorno com a cor definida
        cv2.drawContours(img_colorida, [c], -1, cor_bgr, thickness=cv2.FILLED)

        info_contornos.append({
            "indice": i,
            "area": cv2.contourArea(c),
            "hu_min": float(v_min),
            "hu_max": float(v_max),
            "hu_media": float(v_media),
            "hu_mediana": float(v_mediana),
            "classificacao": nome,
            "cor_bgr": cor_bgr,
        })

    return img_colorida, info_contornos


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
        if area > 35:
            contornos_fechados.append(c)

#----código do Claude-----------------------------------------------------------------------------------------
    img_segmentada, info = analisar_e_colorir_contornos(contornos_fechados, hu, img_closed.shape, usar_colormap=False)
#-------------------------------------------------------------------------------------------------------------    
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
    # cv2.imshow("Bordas dilatadas", dilated)
    cv2.imshow("Fechamento", img_closed)
    cv2.imshow("Contornada", img_contornada)

    cv2.imshow("Segmentada por HU", img_segmentada)

    return img_canny, dilated, img_closed, img_contornada

# ---------- pipeline original (HU -> janela -> remoção de fundo -> Canny) ----------
ds = pydicom.dcmread(in_file('img4.dcm'))

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
# cv2.imshow("Gaussian Blur", img_blur)

img_canny, img_dilated, img_closed, contornada = atualizar(0)

cv2.waitKey(0)
cv2.destroyAllWindows()


# o que falta:
# analisar intervalos de cores e segmentar