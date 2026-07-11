import cv2
import numpy as np
from utils import *
import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt

def mostra_valores():
    print(f"lower: {t_lower.get()}\nupper: {t_upper.get()}")
    window.destroy()


arquivo = filedialog.askopenfilename() # pega o caminho do arquivo
img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)

# ------------- Criação da janela interativa para inserir thresholds: ---------------
janela = tk.Tk()
janela.title("Inserção dos valroes para threshold")

# Entry e Label para o t_lower:
t_lower = tk.IntVar()
label_t_lower = ttk.Label(janela, text="Lower Threshold:")
label_t_lower.grid(row=0, column=0, padx=10, pady=5, sticky="e")

entry_t_lower = ttk.Entry(janela, textvariable=t_lower)
entry_t_lower.grid(row=0, column=1, padx=10, pady=5)

# Entry e Label para o t_upper:
t_upper = tk.IntVar()
label_t_upper = ttk.Label(janela, text="Upper Threshold:")
label_t_upper.grid(row=1, column=0, padx=10, pady=5, sticky="e")

entry_t_upper = ttk.Entry(janela, textvariable=t_upper)
entry_t_upper.grid(row=1, column=1, padx=10, pady=5)

# Botão para armazenar os valores
botao_get = ttk.Button(janela, text="Enviar", command=mostra_valores)
botao_get.grid(row=2, columnspan=2, padx=10, pady=10)

janela.mainloop()

#-------execução das bordas de canny com base nos valores dados----------

t_lower, t_upper = janela_thresholds()

img_canny = cv2.Canny(img, t_lower.get(), t_upper.get())
#fzr comando pra salvar imagem canny de acordo com os valores dos thresholds!

kernel = np.ones((5,5), np.uint8)

erosion = cv2.erode(img, kernel, iterations=1)

cv2.imshow('original', img)
cv2.imshow('bordas de canny', img_canny)
cv2.imshow('erosão', erosion)

cv2.waitKey(0)
cv2.destroyAllWindows()


# Ainda falta:
# dilatar as bordas
# eliminar bordas 'ruídos' (se der)
# detectar intervalo de cores de cada região fechada
# pintar cada região de acordo com o intervalo de cores