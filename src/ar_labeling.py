from PIL import Image

from database import load_database
from feature_points import *
from utils import get_image_layerAR
from feature_points import *

IMAGE_TEST_PATH = '..\database\sample\image.jpg'

def image_test(image_test, database_images):
    
    #Calculates feature points for test image
    img, kp, des = calculate_feature_points(image_test)

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

    print('Found %d matches for database image %d' % (max_matches, index_max), flush=True)

    layerAR = get_image_layerAR(index_max)
	
    NOIMREADSAMPLE = image_test
    print('sample %s databas %s' % (NOIMREADSAMPLE, NOIMREADDATABASE), flush=True)
    database_image = [database_images[0][index_max], database_images[1][index_max], database_images[2][index_max]]
    compute_homography(image, database_image, layerAR, matches[index_max])

def main():

    images_cv, feature_points, descriptors = load_database()
    database_images = [images_cv, feature_points, descriptors]
 
    image_test(IMAGE_TEST_PATH, database_images)


if __name__== "__main__":
    main()