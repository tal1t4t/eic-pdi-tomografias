import cv2
import numpy as np
from utils import *
import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt

def mostra_valores():
    print(f"lower: {t_lower.get()}\nupper: {t_upper.get()}")
    janela.destroy()

arquivo = filedialog.askopenfilename() # pega o caminho do arquivo
img = cv2.imread(arquivo)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, contours, -1, (0,255,0), 1)

cv2.imshow('threshold', thresh)
cv2.imshow('contours', img)
cv2.waitKey(0)
cv2.destroyAllWindows()