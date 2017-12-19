import numpy as np
import cv2
from matplotlib import pyplot as plt
from vision.utils import blend_transparent
MIN_MATCH_COUNT = 15

"""
Computes matches for des1 (test image) to des2 (database)
"""
def compute_matches(des1, des2):
    print(des1, flush=True)
    print(des2, flush=True)
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

def calculate_matches(image_des, database_des):
    print("Calculating matches with the database images", flush=True)
    matches = []
    for db_des in database_des:
        mat = compute_matches(db_des, image_des)
        matches.append(mat)

    return matches

def compute_homography(test_image_path, test_image, database_image, layerAR, matches):

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

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,0.6)
        matchesMask = mask.ravel().tolist()

        h,w = dst.shape

        result = cv2.warpPerspective(coloredLayerAr, M,(w,h))
    
    print('shape', flush=True)
    print(layerAR_img.shape, flush=True)
    print(src.shape, flush=True)
    src_gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    merge = cv2.addWeighted(layerAR_img,0.5,src_gray,0.5,0)
    
    merge_final = blend_transparent(dst_rgb, result)

    cv2.namedWindow('res', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('res', 300, 300)
    cv2.imshow('res',result)

 
    cv2.namedWindow('merge_ori', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('merge_ori', 300, 300)
    cv2.imshow('merge_ori',merge)
 

    cv2.namedWindow('merge', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('merge', 300, 300)
    cv2.imshow('merge',merge_final)

    cv2.namedWindow('ori', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('ori', 300, 300)
    cv2.imshow('ori', dst)

    cv2.namedWindow('test', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('test', 300, 300)
    cv2.imshow('test', src)

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = matchesMask, # draw only inliers
                    flags = 2)

    img3 = cv2.drawMatches(src,kp_database_image,dst,kp_test_image,matches,None,**draw_params)

    plt.imshow(img3, 'gray'),plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def calculate_feature_points(image_path):
    
    print('Calculating feature points for image %s' % image_path, flush=True)
    
    img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE) # queryImage
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
   
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img,None)

    return img, kp1, des1
