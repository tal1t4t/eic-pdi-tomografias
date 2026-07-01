# fonte: https://medium.com/@julia.jgmf/removendo-fundo-de-imagens-com-python-71eef07e945e

from utils import in_file, out_file
from rembg import remove
from PIL import Image
# from otsu import threshold_image, find_best_threshold, abre_imagem, salva_imagem_otsu


def remove_fundo(img):
    original = Image.open(in_file(img))
    output = remove(original)
    output.save(out_file(f"semfundo_{img}"))


if __name__ == "__main__":
    original = 'img2.png'
    remove_fundo(original)