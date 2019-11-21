import cv2
import numpy as np
import pytesseract
from PIL import Image
import copy
import time
from picamera import PiCamera
from time import sleep


from reading_data2 import *
from firebase import firebase


# Path of working folder on Disk
src_path = "/home/pi/Desktop/"
d = 0  # Slice image counter

chill_data = read_csv("datos.csv")


# Apply OCR for character recognition
def ocr(img):
    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(img, lang='eng', boxes=False, config='--psm 11 --oem 1' )

    return result


# Function that process images, d is just a counter to name crops
def analyzer(img, e, e2, e3, e4=0):
    img = cv2.imread(img)  # To open an image as a numpy array with OpenCV
    shape = cv2.imread(src_path + "shape.png")  # Here we store our image with the shape we are looking for

    # This softens the images, is in testing
    """kernel = np.ones((8, 8), np.float64) / 64
    img = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(src_path + "beautiful.png", img)"""

    # Copy Original images
    shape_original = copy.deepcopy(shape)
    original = copy.deepcopy(img)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    shape = cv2.cvtColor(shape, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    #img = cv2.erode(img, kernel, iterations=1)
    #img = cv2.dilate(img, kernel, iterations=1)
    #shape = cv2.erode(shape, kernel, iterations=1)
    #shape = cv2.dilate(shape, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite(src_path + "removed_noise.png", img)

    #  TYPES OF THRESHOLDING
    #  Apply threshold to get a binarized image

    # Threshold for shape
    shape_thresh = cv2.adaptiveThreshold(shape, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    """ There are two types of adaptive methods thresholdings that we use: ADAPTIVE_THRESH_MEAN_C and 
    ADAPTIVE_THRESH_GAUSSIAN_C, here we use MEAN_C, because is faster, though GAUSSIAN is more precise"""
    # Threshold for image
    img_thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 77, 30)# 501, 60
    
    

    # Image location, here we store the threshold images for visual understanding
    cv2.imwrite(src_path + "thres_image.png", img_thresh)  # Image thresh
    cv2.imwrite(src_path + "thres_shape.png", shape_thresh)  # Shape thresh

    # Finding Contours
    img, contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # Target Image
    num_of_contours = len(contours)
    print("Contours found:", len(contours))
    shape, contours2, hierarchy = cv2.findContours(shape_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # Shape image

    # Storing contours
    shape_contours = contours2[0]  # We save the contour of the shape guide
    boxes = []  # We declare the array that will store the filter contours
    img_vector = list()  # Declaring array for cropped images

    # Filtering contours
    # Here we compare the contour of the shape with every contour detected in the image, and store the similarity
    position = []  # Position of the text boxes
    for i in range(0, num_of_contours):
        # value
        similarity = cv2.matchShapes(shape_contours, contours[i], 1, 0.0)

        # area Stores the value of the contour area
        area = cv2.contourArea(contours[i])

        # Here we verify if the similarity of the shape with a contour is relatively similar, and if its, area has the
        # size that we are looking for. If the contour is validated we apply a rectangle approximation, this will give
        # us a better delimitation of the section of interest.

        """ Similarity value is given in a recommend range (0-1), but for testing on a poor image this were the needed
        values, not necessarily 100% accurate, a lot of the contours are basically noise, nonetheless, some of the 
        noise contours are pixels, and pixels does have a rectangle shape. For that reason we need to first know how 
        the Raspberry pi module will capture the image and start from there the calibration.
        Area is given in pixels x pixels, 5000 for maximum area and 1500 for minimum are our test values, tho it may
        change depending on the image"""

        
        if (similarity <= 10) and (12000 >= area >= 5000):

            # Calculate position for rectangle approximation
            x, y, w, h = cv2.boundingRect(contours[i])

            # Add sliced images into an array
            # REMINDER: OpenCV read x,y  positions as y,x
            # We do h+x, cause w and h are width and height, so the sum give us the appropriate coordinates to crop on
            img_vector.append(original[y:h+y, x:w+x])

            position.append((y+4, h-5, x+4, w-100))
            
            # Draw rectangle on the positions calculated above
            original = cv2.rectangle(original, (x+4, y+4), (x + w-100, y + h-5), (0, 255, 0), 1)
            boxes.append(contours[i])
    print("Number of matches: ", len(boxes))
    # We save the original picture with the contours as png
    cv2.imwrite(src_path + "/color.png", original)
    print("Initial recognition finish, starting operation")
    veces = 0
    camera.start_preview()
    hola = True
    mean_time = 0
    while (hola):
        #hola = False
        ti = time.time()
        veces += 1
        slices = []
        # Tomar foto
        src = '/home/pi/Desktop/foto2.jpg'
        
        camera.capture(src)
        

        foto = cv2.imread(src)
        for each in position:
            slices.append(foto[each[0]:each[1] + each[0], each[2]:each[3]+each[2]])

        img2 = sub_images_analysis(slices)

        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        img2 = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)
        
        #img2 = cv2.erode(img2, kernel, iterations=1)
        #img2 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 101, -5)
        
        cv2.imwrite('/home/pi/Desktop/combist.jpg', img2)
        
        img2 = cv2.GaussianBlur(img2, (5, 5), 0)
        th3, img2 = cv2.threshold(img2,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        
        #img2 = cv2.erode(img2, kernel, iterations=1)
        
        cv2.imwrite('/home/pi/Desktop/combi.jpg', img2)
        f = open('resultados1.txt', 'w')
        res = ocr(img2)
        print(res)
        f.write((res) + '\n')
        delay = time.time()-ti
        mean_time += delay
        print("Tiempo de reconocimiento promedio: {} segundos".format(mean_time/veces))
        f.close()
        f = open('resultados1.txt', 'r')
        datos, tempi = analyze(f)
        e += tempi
        push_data(datos)
        print("total", len(datos))
        if (len(datos) != 13):
            if len(datos) > 13:
                e3 += 1
            else:
                e2 += 1
        else:
            temporal = [0] * 12
            temporal[0] = datos[4]
            temporal[1] = datos[2]
            temporal[2] = datos[3]
            temporal[3] = datos[7]
            temporal[4] = datos[6]
            temporal[5] = datos[5]
            temporal[6] = datos[10]
            temporal[7] = datos[11]
            temporal[8] = datos[1]
            temporal[9] = datos[0]
            temporal[10] = datos[9]
            temporal[11] = datos[8]
        f.close()
        print("Se reconocio un foto")
        print("errores de reconocimiento:", e)
        print("errores por omision: ", e2)
        print("errores por adicion: ", e3)
        print("total de datos: ", veces)
        
        if check_if_equal(temporal, chill_data):
            print("Todo OK!")
            print("Han ocurrido {} errores".format(e4))
        else:
            e4 += 1
            print("Han ocurrido {} errores".format(e4))
        

def sub_images_analysis(images):

    max_width = 0  # find the max width of all the images
    total_height = 0  # the total height of the images (vertical stacking)
    
    # open all images and find their sizes
    # Shape returns a tuple like this: (1,2,3), where 1 indicates the number of rows
    for each in images:
        if each.shape[1] > max_width:
            max_width = each.shape[1]
    # 2 indicates the number of columns, and 3 the number of values in that position
        total_height += each.shape[0]

    # create a new array with a size large enough to contain all the images
    final_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)

    current_y = 0  # keep track of where your current image was last placed in the y coordinate
    for each in images:
        # add an image to the final array and increment the y coordinate
        final_image[current_y:each.shape[0] + current_y, :each.shape[1], :] = each
        current_y += each.shape[0]
    return final_image

if __name__ == "__main__":
    
    print('--- Start recognize data from image ---')
    start_time = time.time()

    camera = PiCamera()
    camera.start_preview()
    sleep(3)
    camera.capture('/home/pi/Desktop/foto.jpg')
    camera.stop_preview()
    errors = 0
    errors2 = 0
    errors3 = 0
    analyzer('/home/pi/Desktop/foto.jpg', errors, errors2, errors3)
    print("--- {} seconds ---".format(time.time() - start_time))
    print("------ Done -------")
