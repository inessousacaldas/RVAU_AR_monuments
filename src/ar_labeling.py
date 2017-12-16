from PIL import Image

from database import load_database
from feature_points import *


IMAGE_TEST_PATH = '..\database\sample\image.JPG'


def image_test(image_test, database_images):
    img, kp, des = calculate_feature_points(image_test)

    image = [img, kp, des]

    matches = calculate_matches(des, database_images[2])

    if(len(matches) == 0):
        print('No corresponde with database image was found.', flush = True)
        return

    max_matches = 0
    index_max = -1
    for i in range(len(matches)):
        if(len(matches[i]) > max_matches):
            max_matches = len(matches[i])
            index_max = i

    print("Found %d matches", max_matches)

    #layerAR = Image.open(filename)

    compute_homography(image, database_images[index_max], layerAR, matches[index_max])

    
        

def main():

    images_cv, feature_points, descriptors = load_database()

    database_images = [images_cv, feature_points, descriptors]
    
    image_test(IMAGE_TEST_PATH, database_images)


if __name__== "__main__":
    main()