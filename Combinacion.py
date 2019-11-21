from pathlib import Path
import time

import cv2
import numpy as np
import pytesseract

home = str(Path.home)
src_path = home + "/Desktop/image/"

# Recognize text with tesseract for python
def ocr(img):
    # Here we apply the ocr
    result = pytesseract.image_to_string(img)
    # Write results on file
    f = open('resultados1.txt', 'a')
    f.write('\n' + result)
    f.close()
    return result


def combine_images():
    image_names = []
    # Due the nomencalture of the files, this for loop will add all the paths into a list.
    # Please remember to change the range if you are going to change the number of files
    # to combine
    for i in range (0, 14):
        image_names.append(src_path + 'crop_thres{}_0.jpg'.format(i))

    images = []
    max_width = 0  # find the max width of all the images
    total_height = 0  # the total height of the images (vertical stacking)
    for name in image_names:
        # open all images and find their sizes
        img = cv2.imread(name)
        images.append(img)
        # Shape returns a tuple like this: (1,2,3), where 1 indicates the number of rows
        # 2 indicates the number of columns, and 3 the number of values in that position
        if images[-1].shape[1] > max_width:
            max_width = images[-1].shape[1]
        total_height += images[-1].shape[0]

    # create a new array with a size large enough to contain all the images
    final_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)

    current_y = 0  # keep track of where your current image was last placed in the y coordinate
    for image in images:
        # add an image to the final array and increment the y coordinate
        final_image[current_y:image.shape[0] + current_y, :image.shape[1], :] = image
        current_y += image.shape[0]

    return final_image

if __name__ == "__main__":
    start_time = time.time()
    cv2.imwrite(src_path + 'combiandas.png', combine_images())
    print("--- Combination took {} seconds ---".format(time.time() - start_time))
    img = cv2.imread(src_path + 'combiandas.png')
    start_time = time.time()
    # Here we apply the ocr
    ocr(img)
    print("--- Ocr took {} seconds ---".format(time.time() - start_time))
