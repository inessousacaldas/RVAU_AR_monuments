import cv2
import numpy as np
from vision.database import create_file_database

def applyMask(img, r):
    
    # Create the basic black image 
    mask = np.zeros(img.shape, dtype = "uint8")

    # Draw a white, filled rectangle on the mask image
    x1 = r[0]
    y1 = r[1]
    x2 = x1 + r[2]
    y2 = y1 + r[3]
    mask_color = cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), -1)
    mask_color = cv2.cvtColor(mask_color,cv2.COLOR_BGR2GRAY)
    res = cv2.bitwise_and(img,img,mask = mask_color)

    # Display constructed mask
    cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Mask", 600, 400)
    cv2.imshow("Mask", mask)

    cv2.namedWindow("Res", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Res", 600, 400)
    cv2.imshow("Res", res)

    cv2.waitKey(0)

    return res


def select_region(image_path):
 
    # Read image
    im = cv2.imread(image_path)

    # Select ROI
    cv2.namedWindow('keypoints', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('keypoints', 600,600)
    r = cv2.selectROI('keypoints', im, True)

    res = applyMask(im, r)

    print('Calculating feature points for image %s' % image_path, flush=True)
    cv2.destroyAllWindows()
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(gray,None)

    create_file_database(image_path, im, kp1,des1)
