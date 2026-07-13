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
img_blur = cv2.GaussianBlur(img_cinza, (5,5), 0)
img_canny = cv2.Canny(img_blur, threshold1=15, threshold2=40, apertureSize=3, L2gradient=False)

cv2.imshow("Original", img_semfundo)
# cv2.imshow("Mediana", img_mediana)
cv2.imshow("Gaussian Blur", img_blur)

cv2.imshow("Canny", img_canny)

# o que falta:

# dilatar bordas/fazer fechamento 
# detectar contornos fechados
# analisar intervalos de cores e segmentar

cv2.waitKey(0)
cv2.destroyAllWindows()