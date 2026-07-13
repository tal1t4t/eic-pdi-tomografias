import cv2
import numpy as np
from utils import *
import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt

def fecha_janela():
    janela.destroy()

def atualizar(x):
    inf = cv2.getTrackbarPos('Inferior', 'Canny')
    sup = cv2.getTrackbarPos('Superior', 'Canny')

    img_blur = cv2.GaussianBlur(img, (3,3), 0)
    img_canny = cv2.Canny(img_blur, inf, sup, apertureSize=3, L2gradient=False)

    #dilatação de bordas
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(img_canny, kernel, iterations=1)

    # legenda para a imagem com as bordas de canny
    leg_inf = f'Inferior: {inf}'
    cv2.putText(img_canny, leg_inf, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6 ,(255, 255, 255), 1)

    leg_sup = f'Superior: {sup}'
    cv2.putText(img_canny, leg_sup, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

    cv2.imshow('Canny', img_canny)
    cv2.imshow('Bordas dilatadas', dilated)


arquivo = filedialog.askopenfilename() # pega o caminho do arquivo
img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)

# ------------- Criação da janela interativa para inserir thresholds: ---------------

cv2.namedWindow("Canny")

cv2.createTrackbar("Inferior", "Canny", 0, 255, atualizar)
cv2.createTrackbar("Superior", "Canny", 0, 255, atualizar)


#-------execução das bordas de canny com base nos valores dados----------
atualizar(0)

cv2.imshow('original', img)

cv2.waitKey(0)
cv2.destroyAllWindows()


# Ainda falta:
# eliminar bordas 'ruídos' (se der)
# detectar intervalo de cores de cada região fechada
# pintar cada região de acordo com o intervalo de cores