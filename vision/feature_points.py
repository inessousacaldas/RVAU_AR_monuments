import numpy as np
import cv2
from time import time
from matplotlib import pyplot as plt
from vision.utils import blend_transparent

# Minimum number of matches 
MIN_MATCH_COUNT = 15

# Computes matches for des1 (test image) to des2 (database) using flann based matcher
def compute_matches(des1, des2):
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    return good

# Computes the mathes between the test image and the database images
def calculate_matches(image_des, database_des):
    print("Calculating matches with the database images", flush=True)
    start_time = time()
    matches = []
    for db_des in database_des:
        mat = compute_matches(db_des, image_des)
        matches.append(mat)

    end_time = time()
    time_taken = end_time - start_time # time_taken is in seconds
    print("Time spent: %.2f seconds" % time_taken)
    return matches

# Computes the homography between the test image and the image with the higher number of best matches
# Shows the findings with the correct homography
def compute_homography(test_image_path, test_image, database_image, layerAR, matches,ransac_value,debug_bool):

    #kp_database_image/test_image = [img, kp, des]
    layerAR_img = cv2.imread(layerAR, 0)
    coloredLayerAr = cv2.imread(layerAR, -1)
    dst_rgb = cv2.imread(test_image_path, 1)

    #Images openCV
    src = database_image[0]
    dst = test_image[0]
    
    #Keypoints
    kp_database_image = database_image[1]
    kp_test_image = test_image[1]

    #Descriptors
    des_database_image = database_image[2]
    des_test_image = test_image[2]
    
    if len(matches) > MIN_MATCH_COUNT:
        src_pts = np.float32([ kp_database_image[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp_test_image[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, ransac_value)
        matchesMask = mask.ravel().tolist()

        h,w = dst.shape

        result = cv2.warpPerspective(coloredLayerAr, M,(w,h))
    
        # show findings
        if debug_bool:
            print(layerAR_img.shape, flush=True)
            print(src.shape, flush=True)
            
        src_gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
        merge = cv2.addWeighted(layerAR_img,0.5,src_gray,0.5,0)
        merge_final = blend_transparent(dst_rgb, result)

        if debug_bool:
            cv2.namedWindow('res', cv2.WINDOW_KEEPRATIO)
            cv2.resizeWindow('res', 300, 300)
            cv2.imshow('res',result)
           
            cv2.namedWindow('ori', cv2.WINDOW_KEEPRATIO)
            cv2.resizeWindow('ori', 300, 300)
            cv2.imshow('ori', dst)
    
            cv2.namedWindow('test', cv2.WINDOW_KEEPRATIO)
            cv2.resizeWindow('test', 300, 300)
            cv2.imshow('test', src)

            cv2.namedWindow('layer', cv2.WINDOW_KEEPRATIO)
            cv2.resizeWindow('layer', 300, 300)
            cv2.imshow('layer',layerAR_img)

        cv2.namedWindow('merge', cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow('merge', 300, 300)
        cv2.imshow('merge',merge_final)

        cv2.namedWindow('merge_ori', cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow('merge_ori', 300, 300)
        cv2.imshow('merge_ori',merge)

        # Draw best matches on the screen
        draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                        singlePointColor = None,
                        matchesMask = matchesMask, # draw only inliers
                        flags = 2)

        img3 = cv2.drawMatches(src,kp_database_image,dst,kp_test_image,matches,None,**draw_params)

        plt.imshow(img3, 'gray'),plt.show()
        cv2.destroyAllWindows()
    
    else:
        print('The minimum of %s matches was not reached. Please try it agin later...' % MIN_MATCH_COUNT, flush=True)

# calculates the keypoints of an image using a certain algorithm
def calculate_feature_points(image_path, algorithm_type, debug_bool): 
    print('Calculating feature points for image %s' % image_path, flush=True)
    
    if algorithm_type == 'sift':
        print('sift algorithm',flush=True)
        
        img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE) # queryImage
        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()
    
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img,None)
        
        if debug_bool:
            print('kp %s desc %s ' % (len(kp1),len(des1)) ,flush=True)
        
        return img, kp1, des1

    elif algorithm_type == 'surf':
        print('surf algorithm',flush=True)
        
        img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE) # queryImage
        # Create SURF object. You can specify params here or later.
        # Here I set Hessian Threshold to 400
        if debug_bool:
            print('Hessian Threshold = 400',flush=True)
        
        surf = cv2.xfeatures2d.SURF_create(400)
        """
        Hessian threshold is related to the number of keypoints and descriptores found
        The higher the Hessian threshold value the lower the number of key points and 
        descriptors calculated. 
        With the chosen value are found around 1700 with the chosen test image
        """
        # Find keypoints and descriptors directly
        kp, des = surf.detectAndCompute(img,None)
        if debug_bool:
            print('kp %s desc %s ' % (len(kp),len(des)) ,flush=True)

        return img, kp, des


#calculate_feature_points('test.jpg', 'sift')