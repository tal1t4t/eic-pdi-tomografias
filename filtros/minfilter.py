from PIL import Image, ImageFilter
from utils import in_file, out_file

original_png = Image.open(in_file('novo1.png'))

filtro_minimo = ImageFilter.MinFilter(3)
# o parâmetro do MinFilter representa a ordem da matriz para calcular a mediana

final_png = original_png.filter(filtro_minimo) #aplicando o filtro na imagem

final_png.save(out_file('minimo_novo.png'))

final_png.show()