import cv2
import numpy as np
from vision.database import create_file_database

def select_region(image_path):
 
    # Read image
    im = cv2.imread(image_path)

    # Select ROI
    r = cv2.selectROI(im)

    # Crop image
    imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

    print('Calculating feature points for image %s' % image_path, flush=True)
    cv2.destroyAllWindows()
    gray = cv2.cvtColor(imCrop, cv2.COLOR_BGR2GRAY)
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(gray,None)

    create_file_database(image_path, kp1,des1)

    
    
    