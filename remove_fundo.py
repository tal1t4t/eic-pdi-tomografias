# fonte: https://medium.com/@julia.jgmf/removendo-fundo-de-imagens-com-python-71eef07e945e

from utils import in_file, out_file
from rembg import remove
from PIL import Image
from otsu import threshold_image, find_best_threshold, abre_imagem, salva_imagem_otsu

original = in_file('img2.png')
sem_fundo = 'img2_semfundo.png'

input = Image.open(original)
output = remove(input)

output.save(out_file(sem_fundo))
