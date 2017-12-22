import cv2
import numpy as np
from vision.database import create_file_database

descriptors = None

# Computes the mask select by the user
def applyMask(img, r, debug_bool):
    
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

    if debug_bool:
        # Display constructed mask
        cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Mask", 600, 400)
        cv2.imshow("Mask", mask)

        cv2.namedWindow("Res", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Res", 600, 400)
        cv2.imshow("Res", res)

        cv2.waitKey(0)

    return res

# Calculates the Keypoints and the descriptors of the selected mask, and store them into the respective files
def select_region(image_path, debug_bool):
 
    global descriptors

    # Read image
    im = cv2.imread(image_path)

    # Select ROI
    cv2.namedWindow('keypoints', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('keypoints', 600,600)
    r = cv2.selectROI('keypoints', im, True)

    res = applyMask(im, r, debug_bool)

    print('Calculating feature points for image %s' % image_path, flush=True)
    cv2.destroyAllWindows()
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    
    print('sift algorithm',flush=True)
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(gray,None)

    descriptors = des1
    removeKeyPoints(gray, kp1)
    des1 = descriptors
   
    if debug_bool:
        print('kp %s desc %s ' % (len(kp1),len(des1)) ,flush=True)
   
    create_file_database('sift', image_path, im, kp1,des1)
   
    if debug_bool:
        print('Hessian Threshold = 400',flush=True)
   
    surf = cv2.xfeatures2d.SURF_create(400)
    # Find keypoints and descriptors directly
    kp, des = surf.detectAndCompute(gray,None)
    
    descriptors = des
    removeKeyPoints(gray, kp)
    des = descriptors
    
    if debug_bool:
        print('kp %s desc %s ' % (len(kp),len(des)) ,flush=True)
   
    create_file_database('surf', image_path, im, kp,des)

# Calculates the Keypoints and the descriptors for the entire image
def keypoints_default(image_path, debug_bool):
 
    # Read image
    im = cv2.imread(image_path)

    if debug_bool:
        print('Calculating feature points for image %s' % image_path, flush=True)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    
    print('sift algorithm',flush=True)
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(gray,None)
    
    if debug_bool:
        print('kp %s desc %s ' % (len(kp1),len(des1)) ,flush=True)
    
    create_file_database('sift', image_path, im, kp1,des1)
    
    print('surf algorithm',flush=True)

    if debug_bool:
        print('Hessian Threshold = 400',flush=True)
   
    surf = cv2.xfeatures2d.SURF_create(400)
    # Find keypoints and descriptors directly
    kp, des = surf.detectAndCompute(gray,None)
    
    if debug_bool:
        print('kp %s desc %s ' % (len(kp),len(des)) ,flush=True)
    
    create_file_database('surf', image_path, im, kp,des)

#Window to remove keypoints with mouse click
def removeKeyPoints(gray, kp1):
    
    keycode = -1
    closed = 0.0
    _color = (0,0,255)

    while (keycode != 13) & (closed != -1.0): #Enter pressed
        img_kp =cv2.drawKeypoints(gray, kp1, None, color=_color, flags=2)
        cv2.imshow('remove_keypoints',img_kp)
        cv2.setMouseCallback("remove_keypoints", click_and_delete, param=[kp1])
        keycode = cv2.waitKey(100)
        closed = cv2.getWindowProperty('remove_keypoints', 0)
 
    cv2.destroyWindow('remove_keypoints')  

#Checks if coordinates are inside the circle: (center_x, center_y) and radius
def inside_circle(x, y, center_x, center_y, radius):
    if ((((x - center_x)**2) + ((y - center_y)**2)) < radius**2):
        return True
    
    return False

#Check if mouse input over keypoint and deletes it
def click_and_delete(event, x, y, flags, param):
    
    global descriptors
    kp = param[0]

    if event == cv2.EVENT_LBUTTONDOWN:     
        for n in range(len(kp)):
            center_x = kp[n].pt[0]
            center_y = kp[n].pt[1]
            radius = kp[n].size
            if(inside_circle(x, y, center_x, center_y, radius)):
                del(kp[n])
                descriptors = np.delete(descriptors, n, 0)
                break

