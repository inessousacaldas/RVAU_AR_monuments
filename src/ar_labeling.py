from database import load_database
from feature_points import *



IMAGE_TEST_PATH = '..\database\sample\image.JPG'


def image_test(image_test, database_images):
    img, kp, des = calculate_feature_points(image_test)

    image = [img, kp, des]


    matches = calculate_matches(des, database_images[2])

    for mm in matches:
        print(len(mm))


def main():
    images_cv, feature_points, descriptors = load_database()

    database_images = [images_cv, feature_points, descriptors]
    
    image_test(IMAGE_TEST_PATH, database_images)


  
if __name__== "__main__":
  main()