import pydicom
import numpy as np
import matplotlib.pyplot as plt
from utils import in_file, out_file

# BLOCO 01
# =========================
# FUNÇÕES DE TRATAMENTO
# =========================

def converter_para_hu(ds):
    pixels = ds.pixel_array.astype(np.float32)
    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))
    hu = pixels * slope + intercept
    return hu


def aplicar_janela(hu, window_center, window_width):
    min_janela = window_center - window_width / 2
    max_janela = window_center + window_width / 2
    hu_window = np.clip(hu, min_janela, max_janela)
    return hu_window


def normalizar_minmax(img):
    img = img.astype(np.float32)
    return (img - img.min()) / (img.max() - img.min() + 1e-8)


def filtro_media(img):
    padded = np.pad(img, 1, mode="edge")
    saida = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            bloco = padded[i:i+3, j:j+3]
            saida[i, j] = np.mean(bloco)

    return saida


def limiarizar(img, limiar=0.35):
    return (img >= limiar).astype(np.uint8)


def filtro_laplaciano_8(img):
    kernel_8 = np.array([[1, 1, 1],
                         [1, -8, 1],
                         [1, 1, 1]], dtype=np.float32)

    padded = np.pad(img, 1, mode="edge")
    saida_8 = np.zeros_like(img, dtype=np.float32)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            bloco = padded[i:i+3, j:j+3]
            saida_8[i, j] = np.sum(bloco * kernel_8)

    return np.abs(saida_8)


# BLOCO 02
# =========================
# LEITURA DO ARQUIVO DICOM
# =========================

caminho = in_file("img2.dcm")

try:
    ds = pydicom.dcmread(caminho)
    print("Arquivo lido com sucesso!")
except Exception as e:
    print("Erro ao ler o DICOM:", e)
    raise


# BLOCO 03
# =========================
# TRATAMENTO DA IMAGEM
# =========================

img_original = ds.pixel_array
hu = converter_para_hu(ds)
janela = aplicar_janela(hu, window_center=-600, window_width=1500)
img_norm = normalizar_minmax(janela)
img_suave = filtro_media(img_norm)
img_binaria = limiarizar(img_suave, limiar=0.35)

img_laplaciano_8 = filtro_laplaciano_8(img_norm)
img_laplaciano_8 = normalizar_minmax(img_laplaciano_8)


# BLOCO 04
# =========================
# VISUALIZAÇÃO DA IMAGEM
# =========================

fig, ax = plt.subplots(1, 5, figsize=(25, 5))

ax[0].imshow(img_original, cmap="gray")
ax[0].set_title("DICOM original")
ax[0].axis("off")

ax[1].imshow(img_norm, cmap="gray")
ax[1].set_title("Janela + normalização")
ax[1].axis("off")

ax[2].imshow(img_suave, cmap="gray")
ax[2].set_title("Filtro de média")
ax[2].axis("off")

ax[3].imshow(img_binaria, cmap="gray")
ax[3].set_title("Limiarização")
ax[3].axis("off")

ax[4].imshow(img_laplaciano_8, cmap="gray")
ax[4].set_title("Laplaciano")
ax[4].axis("off")

plt.tight_layout()
plt.show()