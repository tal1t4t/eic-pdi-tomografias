from PIL import Image
from utils import in_file, out_file
import pydicom
import numpy as np

def convert(img):
    original_dcm = pydicom.dcmread(in_file("img3.dcm"))

    # transforma a array de pixels da imagem em float
    original_dcm = original_dcm.pixel_array.astype(float)

    rescaled_image = (np.maximum(original_dcm,0) / original_dcm.max()) * 255
    # deixa os valores dos pixels num range de 0 a 255 no formato float
    # np.maximum(original,0) -> se houver valores menores que 0 no intervalo, eles serão substituídos por 0

    final = np.uint8(rescaled_image) # tranforma os valores dos pixels em int com tamanho de 8bits
    final = Image.fromarray(final)

    #essa linha deve sair futuramente, quando as pastas de input e output forem alteradas
    final.save(out_file('img3.png'))