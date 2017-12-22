from __future__ import print_function
from PIL import Image
from vision.database import load_fileImages_database
from vision.feature_points import calculate_feature_points, calculate_matches, compute_matches, compute_homography
from vision.utils import get_image_layerAR


IMAGE_TEST_PATH = '..\database\sample\image.jpg'

# Tests the user image with databe and computes the homography, then it shows the results
# Need algorithm type and ransac value
def image_test(image_test, database_images, algorithm_type, ransac_value, debug_bool):
    
    #Calculates feature points for test image
    img, kp, des = calculate_feature_points(image_test, algorithm_type, debug_bool)
 
    image = [img, kp, des]
    
    #Calculates matches of image test with all images from database
    matches = calculate_matches(des, database_images[2])

    #If no good match with any of the database images return
    if(len(matches) == 0):
        print('No corresponde with database image was found.', flush = True)
        return

    #Choose database image with best match
    max_matches = 0
    index_max = -1
    for i in range(len(matches)):
        if(len(matches[i]) > max_matches):
            max_matches = len(matches[i])
            index_max = i

    print('Found %d matches for database image %d' % (max_matches, index_max + 1), flush=True)

    layerAR = get_image_layerAR(index_max)

    database_image = [database_images[0][index_max], database_images[1][index_max], database_images[2][index_max]]
    
    compute_homography(image_test, image, database_image, layerAR, matches[index_max], ransac_value, debug_bool)

# compute the test image and show the findings 
# args : the image path, the algorithm name ('sift' or 'surf'), the ransac value (float) and debug (true or false)
# arAppCompute('..\database\images\img1.jpg', 'surf', 0.6, False) 
def arAppCompute(image_test_path, algorithm_type, ransac_value, debug_bool):
    images_cv, feature_points, descriptors = load_fileImages_database(algorithm_type)
    database_images = [images_cv, feature_points, descriptors]
    
    image_test(image_test_path, database_images, algorithm_type, ransac_value, debug_bool)

"""
def main():

    images_cv, feature_points, descriptors = load_database()
    database_images = [images_cv, feature_points, descriptors]
 
    image_test(IMAGE_TEST_PATH, database_images, 'sift', 0.6)


if __name__== "__main__":
    main()
"""
#arAppCompute('..\database\images\img1.jpg', 'surf', 0.6, False) 