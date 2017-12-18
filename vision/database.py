from PIL import Image
import glob
from vision.feature_points import calculate_feature_points
import pickle
import cv2
import os.path
from vision.utils import pickle_keypoints, unpickle_keypoints
from os.path import splitext, basename


DATABASE_PATH = '..\database\images\*.jpg'
IMAGES_PATH = '..\database\images_cv'
FILE_PATH = '..\\database\\vision\\'
FILE_PATH_LOAD = "..\\database\\vision\\*"
DESCRIPTORS_PATH = '..\database\descriptors'
FEATURE_POINTS_PATH = '..\database\Feature_points'

#just one image to database


#image_list = [Image.open(item) for i in [glob.glob('%s*.%s' % (DATABASE_PATH, ext)) for ext in ["jpg","gif","png","tga"]] for item in i]
def create_file_database(image_path):
  
    feature_points = []
    descriptors = []
    
    img, kpt, des = calculate_feature_points(image_path)
        
    feature_points.append(kpt)
    descriptors.append(des)
    
    #get image name, without complete path
    img_filename, _ = os.path.splitext(image_path)
    file_basename = basename(img_filename)
    file = FILE_PATH + file_basename

    temp_kp = []
    i = 0
    for kpts_list in feature_points:
        pickle_tmp = pickle_keypoints(kpts_list, des[i])
        i = i + 1
        temp_kp.append(pickle_tmp)
        
    print('temp_kp: %s' % len(temp_kp),flush=True)

    with open(file, 'wb') as fp:
        pickle.dump(temp_kp, fp)
        
#create_file_database('..\database\images\img1_01.jpg')

def load_fileImages_database():

    print("Loading database...", flush=True)

    file_list = []
    for filename in glob.glob(FILE_PATH_LOAD):
        file_list.append(filename)
       
    
    #Create database if not exist
    if len(file_list) < 1:
        print("no database for feature_points and descriptors", flush=True)
    
    else:
        for file in file_list:
            with open (file, 'rb') as fp:
                temp_kp = pickle.load(fp)  

            feature_points = []
            descriptors = []
           
            for list_kp in temp_kp:
                temp_feature, temp_desc = unpickle_keypoints(list_kp)
                feature_points.append(temp_feature)
                descriptors.append(temp_desc)

        return feature_points, descriptors


#image_list = [Image.open(item) for i in [glob.glob('%s*.%s' % (DATABASE_PATH, ext)) for ext in ["jpg","gif","png","tga"]] for item in i]
def create_database():
    
    image_list = []
    for filename in glob.glob(DATABASE_PATH):
        image_list.append(filename)

    images_cv = []
    feature_points = []
    descriptors = []
    
    for  image in image_list:
        img, kpt, des = calculate_feature_points(image)
        
        images_cv.append(img)
        feature_points.append(kpt)
        descriptors.append(des)

    with open(IMAGES_PATH, 'wb') as fp:
        pickle.dump(images_cv, fp)

    with open(DESCRIPTORS_PATH, 'wb') as fp:
        pickle.dump(descriptors, fp)
    
    temp_kp = []
    for kpts_list in feature_points:
        pickle_tmp = pickle_keypoints(kpts_list)
        temp_kp.append(pickle_tmp)

    with open(FEATURE_POINTS_PATH, 'wb') as fp:
        pickle.dump(temp_kp, fp)

def load_database():

    print("Loading database...", flush=True)

    #Create database if not exist
    if os.path.isfile(IMAGES_PATH) == False | os.path.isfile(DESCRIPTORS_PATH) == False | os.path.isfile(FEATURE_POINTS_PATH) == False:
        create_database()

    with open(IMAGES_PATH, 'rb') as fp:
        images_cv = pickle.load(fp)
    
    with open (DESCRIPTORS_PATH, 'rb') as fp:
        descriptors = pickle.load(fp)

    with open (FEATURE_POINTS_PATH, 'rb') as fp:
        temp_kp = pickle.load(fp)
    
    
    feature_points = []
   
    for list_kp in temp_kp:
        temp_feature = unpickle_keypoints(list_kp)
        feature_points.append(temp_feature)
    
    return images_cv, feature_points, descriptors
    
    
