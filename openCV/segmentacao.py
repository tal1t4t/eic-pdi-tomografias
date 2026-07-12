import cv2
import numpy as np
from utils import *
import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt

def fecha_janela():
    janela.destroy()

def atualizar(x):
    inf = cv2.getTrackbarPos('Inferior', 'Controle de Bordas')
    sup = cv2.getTrackbarPos('Superior', 'Controle de Bordas')

    img_canny = cv2.Canny(img, inf, sup)

    #dilatação de bordas
    kernel = np.ones((3,3), np.uint8)
    # dilated = cv2.dilate(img_canny, kernel, iterations=1)

    # operação de abertura
    # opening = cv2.morphologyEx(img_canny, cv2.MORPH_OPEN, kernel)
    
    # operação de fechamento
    # closed = cv2.morphologyEx(img_canny, cv2.MORPH_CLOSE, kernel)

    # legenda para a imagem com as bordas de canny
    leg_inf = f'Inferior: {inf}'
    cv2.putText(img_canny, leg_inf, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6 ,(255, 255, 255), 1)

    leg_sup = f'Superior: {sup}'
    cv2.putText(img_canny, leg_sup, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)


    cv2.imshow('Controle de Bordas', img_canny)
    # cv2.imshow('Bordas dilatadas', dilated)
    # cv2.imshow('Abertura da imagem', opening)
    cv2.imshow('Fechamento da imagem', closed)



arquivo = filedialog.askopenfilename() # pega o caminho do arquivo
img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)

# ------------- Criação da janela interativa para inserir thresholds: ---------------

cv2.namedWindow("Controle de Bordas")

cv2.createTrackbar("Inferior", "Controle de Bordas", 0, 255, atualizar)
cv2.createTrackbar("Superior", "Controle de Bordas", 0, 255, atualizar)

#-------execução das bordas de canny com base nos valores dados----------
atualizar(0)

# kernel = np.ones((3,3), np.uint8)

# dilated = cv2.dilate(img_canny, kernel, iterations=1)

cv2.imshow('original', img)
# cv2.imshow('dilatação', dilated)

cv2.waitKey(0)
cv2.destroyAllWindows()


# Ainda falta:
# dilatar as bordas
# eliminar bordas 'ruídos' (se der)
# detectar intervalo de cores de cada região fechada
# pintar cada região de acordo com o intervalo de cores