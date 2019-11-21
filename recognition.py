import codecs
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Path to the image
src_path = #Path to image's directory

def get_string(img_path):
    # Load color image in grayscale
    img = cv2.imread(img_path, 0)

    # Morphological transformation to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Saving image after the noise has been removed
    cv2.imwrite(src_path + "no_noise.png", img)

    # Applying threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 
                                77, -9)

    # Saving image after threshold
    cv2.imwrite(src_path + "threshold.png", img)

    # Recognize text with tesseract for Python
    result = pytesseract.image_to_string(Image.open(src_path + "threshold.png"))

    return result

print("---Starting recognition---")

# Printing results in a .txt file
file = codecs.open("results.txt", "w", "utf-8")
file.write("\n" + get_string(src_path + image.png))
file.close()

print("---DONE---")
