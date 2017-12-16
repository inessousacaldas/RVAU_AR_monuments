import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 15

def example():

    src = cv2.imread('..\database\images\img1_01.jpg',0)          # queryImage
    dst = cv2.imread('..\database\sample\image.jpg',0) # trainImage
    layerAR_img = cv2.imread('..\database\layers\img1_01_layer.png', 0)

    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(src,None)
    kp2, des2 = sift.detectAndCompute(dst,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    
    print(len(good), flush=True)
    if len(good)>MIN_MATCH_COUNT:
        print('Encontrou', flush=True)
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 0.6)
        matchesMask = mask.ravel().tolist()
        h,w = dst.shape

        result = cv2.warpPerspective(layerAR_img, M,(w,h))

    print(len(src), len(dst), len(layerAR_img), len(result), flush=True)

    merge = cv2.addWeighted(layerAR_img,0.5,src,0.5,0)
    merge_final = cv2.addWeighted(result,0.5,dst,0.5,0)

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

    img3 = cv2.drawMatches(src,kp1,dst,kp2,good,None,**draw_params)

    plt.imshow(img3, 'gray'),plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

"""
Computes matches for des1 (test image) to des2 (database)
"""
def compute_matches(des1, des2):

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    return good

def calculate_matches(image_des, database_des):
    print("Calculating matches with the database images", flush=True)
    matches = []
    for db_des in database_des:
        mat = compute_matches(image_des, db_des)
        matches.append(mat)

    return matches


def compute_homography(test_image, database_image, layerAR, matches):
    #kp_database_image/test_image = [img, kp, des]
    
    layerAR_img = cv2.imread(layerAR)

    database_im = database_image[0]
    
    kp_test_image = test_image[1]
    kp_database_image = database_image[1]

    print(len(kp_test_image), len(kp_database_image), flush=True)

    if len(matches)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp_database_image[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp_test_image[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,0.6)
        matchesMask = mask.ravel().tolist()



def calculate_feature_points(image_path):
    
    print('Calculating feature points for image %s' + image_path, flush=True)
    
    img = cv2.imread(image_path,0) # queryImage
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
   
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img,None)

    return img, kp1, des1

