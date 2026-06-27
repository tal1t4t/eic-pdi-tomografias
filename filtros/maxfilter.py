from PIL import Image, ImageFilter
from utils import in_file, out_file

original_png = Image.open(in_file('novo1.png'))

filtro_maximo = ImageFilter.MinFilter(3)

final_png = original_png.filter(filtro_maximo) #aplicando o filtro na imagem

final_png.save(out_file('maximo.png'))

final_png.show()