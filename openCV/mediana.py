import cv2
from utils import in_file, out_file

nome_img = 'semfundo_mediana_mediana_img2'
img = cv2.imread(in_file(nome_img) + '.png')
kernel_size = 3
img_mediana = cv2.medianBlur(img, kernel_size)

cv2.imwrite(out_file(f'mediana_{nome_img}.png'), img_mediana)