import cv2
from utils import in_file, out_file

nome_img = 'semfundo_img2'
img = cv2.imread(in_file(nome_img) + '.png')
img_mediana = cv2.medianBlur(img, 3)

cv2.imwrite(out_file(f'mediana_{nome_img}.png'), img_mediana)