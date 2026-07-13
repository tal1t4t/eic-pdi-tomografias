import cv2
import numpy as np
from utils import in_file

arq = 'semfundo_mediana_semfundo_mediana_mediana_img2.png'

img = cv2.imread(in_file(arq), cv2.IMREAD_GRAYSCALE)

h, w = img.shape[:2]

def clicar(event, x, y, flags, param):

    global floodfill

    if event == cv2.EVENT_LBUTTONDOWN:

        mask = np.zeros((h + 2, w + 2), np.uint8)

        minColor = 6
        maxColor = 10

        # A máscara precisa ser recriada a cada floodFill

        floodfill = img.copy()

        cv2.floodFill(
            floodfill,
            mask,
            (x, y),
            255,
            minColor,
            maxColor
        )

        cv2.imshow("FloodFill", floodfill)
        # cv2.imshow("Mask", mask)

cv2.namedWindow("Original")
cv2.setMouseCallback("Original", clicar)

cv2.imshow("Original", img)

cv2.waitKey(0)
cv2.destroyAllWindows()