from PIL import Image, ImageFilter
from utils import in_file, out_file
from math import sqrt

filename = "img2.png"
offset = 0
direction = 'a'

original = Image.open(in_file(filename)).convert('L')


#usando filtro laplaciano para realçar os contornos verticais e/ou horizontais

XLAPLACE = ImageFilter.Kernel((3, 3),
    [0, -1, 0,
            -1, 4, -1,
            0, -1, 0],
    1,
        offset)

YLAPLACE = ImageFilter.Kernel((3, 3),
        [-1, -1, -1,
                -1, 8, -1,
                -1, -1, -1],
          1,
                offset)

if direction == 'x': # só é aplicado o contorno horizontal
    filtered = original.filter(XLAPLACE)
elif direction == 'y': # só é aplicado o contorno vertical
    filtered = original.filter(YLAPLACE)
else: # contorno nos dois eixos
    vlaplace = original.filter(XLAPLACE)
    hlaplace = original.filter(YLAPLACE)
    w, h = original.size
    filtered = Image.new('L', (w, h))
    # L = luminância. indica para o código trabalhar em escala de cinza
    for i in range(w):
        for j in range(h):
            #fórmula do módulo do vetor para extrair a força total do contorno no pixel
            value = int(sqrt(vlaplace.getpixel((i, j))**2 + hlaplace.getpixel((i,j))**2))

            #se a o valor extrapolar 255, ele recebe o valor 255

            value = min(value, 255)
            filtered.putpixel((i, j), value)

filtered.save(out_file('{}_{}laplace_{}.png'.format(filename[:filename.index('.')],
                       direction, offset)))