from PIL import Image, ImageFilter
from utils import in_file, out_file

original_png = Image.open(in_file('novo1.png'))

filtro_mediana = ImageFilter.MedianFilter(3)
# o parâmetro do MedianFilter representa a ordem da matriz para calcular a mediana

final_png = original_png.filter(filtro_mediana) #aplicando o filtro na imagem

final_png.save(out_file('mediana_img2.png'))

final_png.show()