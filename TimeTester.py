import copy
from pathlib import Path
import time

import cv2
import numpy as np
import pytesseract
from PIL import Image


# Path of working folder on Disk
home = str(Path.home())
src_path = home + "Desktop/PF/"

# Apply OCR for character recognition
def ocr(img):
    #f = open('resultados1.txt', 'a')
    result = pytesseract.image_to_string(img)
    #f.write('\n' + result)  
    #f.close()

"""MAIN"""
img = []

print('--- Start recognize text from image ---')

start_time = time.time()
img = cv2.imread("prueba.jpg")
print("--- {} seconds ---".format(time.time() - start_time))

start_time = time.time()
ocr(img)
print("--- {} Time in OCR jpg ---".format(time.time() - start_time))
"""start_time = time.time()
img = cv2.imread("holi.png")
print("--- {} time reading ---".format(time.time() - start_time))
ocr(img)
print("--- {} Time in OCR png ---".format(time.time() - start_time))"""
print("------ Done -------")

