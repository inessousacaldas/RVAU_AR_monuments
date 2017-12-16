import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

def test_sift():
    img1 = cv2.imread('..\database\img1_01.jpg',0)          # queryImage
    img2 = cv2.imread('..\database\img1_02.jpg',0) # trainImage

    # Initiate SIFT detector
    #sift = cv2.SIFT()
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

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
                    
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        print ("Not enough matches are found - %s/%s "  (len(good),MIN_MATCH_COUNT))
        matchesMask = None 
        
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = matchesMask, # draw only inliers
                    flags = 2)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

    plt.imshow(img3, 'gray'),plt.show()

    return

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
    print("Calculating matches with database", flush=True)
    matches = []
    for db_des in database_des:
        mat = compute_matches(image_des, db_des)
        matches.append(mat)

    return matches


def compute_homography(test_image, database_image, layerAR, matches):
    
    kp_test_image = test_image[1]
    kp_database_image = database_image[1]

    if len(matches)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp_test_image[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp_database_image[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        im_dst = cv2.warpPerspective(im_src, h, size)

def calculate_feature_points(image_path):
    
    print('Calculating feature points for image %s' + image_path, flush=True)
    
    img = cv2.imread(image_path,0) # queryImage
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
   
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img,None)

    return img, kp1, des1
