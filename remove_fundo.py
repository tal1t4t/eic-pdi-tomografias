# fonte: https://medium.com/@julia.jgmf/removendo-fundo-de-imagens-com-python-71eef07e945e

from utils import in_file, out_file
from rembg import remove
# from PIL import Image
import cv2

# def remove_fundo(img):
#     original = Image.open(in_file(img))
#     output = remove(original)
#     output.save(out_file(f"semfundo_{img}"))
    
#     return output

def remove_fundo(nome_img):
    #imread retorna uma narray do numpy
    original = cv2.imread(in_file(nome_img) + '.png')

    semfundo = remove(original)
    cv2.imwrite(out_file(f'semfundo_{nome_img}.png'), semfundo)

    return semfundo


if __name__ == "__main__":
    nome_original = 'img2'
    remove_fundo(nome_original)