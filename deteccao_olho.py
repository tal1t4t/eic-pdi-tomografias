import pydicom
import numpy as np
from rembg import remove
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cv2

# ---------- parâmetros gerais ----------
caminho_dicom = "/home/talita/pdi-tomografias/pillow/input/img2.dcm"
window_center = -600
window_width = 1500

# ---------- parâmetros da detecção automática dos olhos ----------
# ajuste estes valores se os olhos não forem encontrados / candidatos errados aparecerem
AREA_MIN_FRAC = 0.0008     # área mínima do contorno, como fração da área do rosto
AREA_MAX_FRAC = 0.02       # área máxima do contorno, como fração da área do rosto
CIRCULARIDADE_MIN = 0.45   # 1.0 = círculo perfeito; olhos raramente são perfeitos, então fica flexível
ASPECT_MIN = 0.5           # proporção largura/altura mínima do contorno
ASPECT_MAX = 1.9           # proporção largura/altura máxima do contorno
N_CANDIDATOS_ESCUROS = 10  # quantos contornos mais escuros considerar antes de procurar o par
MOSTRAR_CANDIDATOS = True  # mostra um painel extra com todos os candidatos, útil para calibrar os parâmetros acima


# ---------- funções auxiliares ----------
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


def to_pil_rgba_from_gray(arr8):
    return Image.fromarray(arr8, mode="L").convert("RGBA")


# ---------- pipeline original (HU -> janela -> remoção de fundo -> Canny) ----------
ds = pydicom.dcmread(caminho_dicom)
img_original = ds.pixel_array
hu = converter_para_hu(ds)
hu_windowed = aplicar_janela(hu, window_center, window_width)
img_window_uint8 = normalizar_para_uint8(hu_windowed)
pil_window_rgba = to_pil_rgba_from_gray(img_window_uint8)

pil_window_sem_fundo = remove(pil_window_rgba).convert("RGBA")
semf_arr = np.asarray(pil_window_sem_fundo)

rgb = semf_arr[:, :, :3]
alpha = semf_arr[:, :, 3]

gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
gray[alpha == 0] = 0

gray_blur = cv2.GaussianBlur(gray, (3, 3), 0)
bordas_canny = cv2.Canny(gray_blur, threshold1=15, threshold2=40, apertureSize=3, L2gradient=False)


# ---------- detecção automática da região ocular a partir do Canny ----------
def detectar_olhos(gray, alpha, bordas_canny):
    mask_rosto = alpha > 0
    area_rosto = mask_rosto.sum()
    if area_rosto == 0:
        raise RuntimeError("Máscara do rosto vazia - verifique a remoção de fundo (rembg).")

    ys, xs = np.where(mask_rosto)
    largura_rosto = xs.max() - xs.min()

    # fecha pequenas quebras nas bordas do Canny para formar contornos fechados
    kernel = np.ones((3, 3), np.uint8)
    bordas_dilatadas = cv2.dilate(bordas_canny, kernel, iterations=1)

    contornos, _ = cv2.findContours(bordas_dilatadas, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    candidatos = []
    for c in contornos:
        area = cv2.contourArea(c)
        if area <= 0:
            continue
        frac = area / area_rosto
        if frac < AREA_MIN_FRAC or frac > AREA_MAX_FRAC:
            continue

        perimetro = cv2.arcLength(c, True)
        if perimetro == 0:
            continue
        circularidade = 4 * np.pi * area / (perimetro ** 2)
        if circularidade < CIRCULARIDADE_MIN:
            continue

        x, y, w, h = cv2.boundingRect(c)
        if h == 0:
            continue
        aspecto = w / h
        if aspecto < ASPECT_MIN or aspecto > ASPECT_MAX:
            continue

        cx, cy = x + w / 2.0, y + h / 2.0
        if not mask_rosto[int(cy), int(cx)]:
            continue

        # intensidade média dentro do contorno (usada para achar as regiões mais escuras)
        mask_c = np.zeros(gray.shape, dtype=np.uint8)
        cv2.drawContours(mask_c, [c], -1, 255, -1)
        media_cinza = float(gray[mask_c > 0].mean())

        candidatos.append({
            "contorno": c, "area": area, "circularidade": circularidade,
            "x": x, "y": y, "w": w, "h": h, "cx": cx, "cy": cy,
            "media_cinza": media_cinza,
        })

    if len(candidatos) < 2:
        raise RuntimeError(
            "Não foram encontrados candidatos suficientes para os olhos. "
            "Ajuste AREA_MIN_FRAC / AREA_MAX_FRAC / CIRCULARIDADE_MIN."
        )

    # mantém apenas os contornos mais escuros (olhos tendem a ser as regiões de menor intensidade do rosto)
    candidatos.sort(key=lambda d: d["media_cinza"])
    candidatos_escuros = candidatos[:N_CANDIDATOS_ESCUROS]

    # procura o melhor par simétrico: altura (cy) parecida, separação horizontal plausível
    melhor_par = None
    melhor_score = np.inf

    for i in range(len(candidatos_escuros)):
        for j in range(i + 1, len(candidatos_escuros)):
            a, b = candidatos_escuros[i], candidatos_escuros[j]
            diff_y = abs(a["cy"] - b["cy"])
            dist_x = abs(a["cx"] - b["cx"])

            if diff_y > 0.10 * largura_rosto:
                continue
            if dist_x < 0.08 * largura_rosto or dist_x > 0.65 * largura_rosto:
                continue

            diff_area = abs(a["area"] - b["area"]) / max(a["area"], b["area"])
            diff_escuridao = abs(a["media_cinza"] - b["media_cinza"])
            score = diff_y + diff_area * 20 + diff_escuridao

            if score < melhor_score:
                melhor_score = score
                melhor_par = (a, b)

    if melhor_par is None:
        raise RuntimeError(
            "Não foi encontrado um par simétrico de olhos entre os candidatos mais escuros. "
            "Ajuste os parâmetros de detecção ou aumente N_CANDIDATOS_ESCUROS."
        )

    return melhor_par, candidatos_escuros


(olho_a, olho_b), candidatos_escuros = detectar_olhos(gray, alpha, bordas_canny)

mask_rosto = alpha > 0

# máscara combinada dos dois olhos, usando o contorno real (não apenas o retângulo)
mask_olhos = np.zeros(gray.shape, dtype=bool)
for olho in (olho_a, olho_b):
    m = np.zeros(gray.shape, dtype=np.uint8)
    cv2.drawContours(m, [olho["contorno"]], -1, 255, -1)
    mask_olhos |= (m > 0)

# tom de cinza mais escuro do rosto inteiro (mantido só para referência/print, sem aplicar no olho)
tom_mais_escuro = int(gray[mask_rosto].min())

# olho permanece com o tom original — sem preenchimento
gray_destacado = gray.copy()

# versão colorida do resultado, com a borda do Canny sobreposta
resultado_com_borda = cv2.cvtColor(gray_destacado, cv2.COLOR_GRAY2RGB)
resultado_com_borda[bordas_canny > 0] = (255, 0, 0)


# ---------- visualização ----------
n_paineis = 4 if MOSTRAR_CANDIDATOS else 3
fig, axes = plt.subplots(1, n_paineis, figsize=(5 * n_paineis, 6),
                          gridspec_kw={"width_ratios": [3] * (n_paineis - 1) + [1]})

axes[0].imshow(img_original, cmap="gray")
axes[0].set_title("DICOM original")
axes[0].axis("off")

overlay_canny = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
overlay_canny[bordas_canny > 0] = (255, 0, 0)
axes[1].imshow(overlay_canny)
axes[1].set_title("Canny sobreposto")
axes[1].axis("off")

idx_destaque = 2
axes[idx_destaque].imshow(resultado_com_borda)
for olho, cor in zip((olho_a, olho_b), ("lime", "cyan")):
    rect = mpatches.Rectangle(
        (olho["x"], olho["y"]), olho["w"], olho["h"],
        linewidth=1.5, edgecolor=cor, facecolor="none"
    )
    axes[idx_destaque].add_patch(rect)
axes[idx_destaque].set_title("Olhos detectados (cor original) + Canny sobreposto")
axes[idx_destaque].axis("off")

if MOSTRAR_CANDIDATOS:
    axes[3].imshow(gray, cmap="gray", vmin=0, vmax=255)
    for cand in candidatos_escuros:
        rect = mpatches.Rectangle(
            (cand["x"], cand["y"]), cand["w"], cand["h"],
            linewidth=1, edgecolor="yellow", facecolor="none"
        )
        axes[3].add_patch(rect)
    axes[3].set_title(f"Candidatos escuros (n={len(candidatos_escuros)})")
    axes[3].axis("off")

plt.tight_layout()
plt.show()

print(f"Olho A: centro=({olho_a['cx']:.0f},{olho_a['cy']:.0f}) área={olho_a['area']:.0f} circularidade={olho_a['circularidade']:.2f}")
print(f"Olho B: centro=({olho_b['cx']:.0f},{olho_b['cy']:.0f}) área={olho_b['area']:.0f} circularidade={olho_b['circularidade']:.2f}")