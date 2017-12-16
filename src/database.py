from PIL import Image
import glob
from feature_points import calculate_feature_points
import pickle
import os.path

DATABASE_PATH = '..\database\images\*.jpg'
IMAGES_PATH = '..\database\images_cv'
DESCRIPTORS_PATH = '..\database\descriptors'
FEATURE_POINTS_PATH = '..\database\Feature_points'

#image_list = [Image.open(item) for i in [glob.glob('%s*.%s' % (DATABASE_PATH, ext)) for ext in ["jpg","gif","png","tga"]] for item in i]
def create_database():
    image_list = []
    for filename in glob.glob(DATABASE_PATH): #assuming png
        im=Image.open(filename)
        image_list.append(filename)

    images_cv = []
    feature_points = []
    descriptors = []
    
    for  image in image_list:
        img, kp, des = calculate_feature_points(image)
        
        images_cv.append(img)
        feature_points.append(kp)
        descriptors.append(des)

    with open(IMAGES_PATH, 'wb') as fp:
        pickle.dump(images_cv, fp)

    with open(DESCRIPTORS_PATH, 'wb') as fp:
        pickle.dump(descriptors, fp)
    
    with open(FEATURE_POINTS_PATH, 'wb') as fp:
        pickle.dump(descriptors, fp)

def load_database():

    #Create database if not exist
    if os.path.isfile(IMAGES_PATH) == False | os.path.isfile(DESCRIPTORS_PATH) == False | os.path.isfile(FEATURE_POINTS_PATH) == False:
        create_database()

    with open(IMAGES_PATH, 'rb') as fp:
        images_cv = pickle.load(fp)
    
    with open (DESCRIPTORS_PATH, 'rb') as fp:
        feature_points = pickle.load(fp)
    
    with open (FEATURE_POINTS_PATH, 'rb') as fp:
        descriptors = pickle.load(fp)

        return images_cv, feature_points, descriptors
    
    
