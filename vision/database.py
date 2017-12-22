from PIL import Image
import glob
from vision.feature_points import calculate_feature_points
import pickle
import os.path
import errno
from os.path import splitext, basename
import numpy as np
import os
from vision.utils import pickle_keypoints, unpickle_keypoints



DATABASE_PATH_IMAGES = '..\\database\\images\\'
DATABASE_PATH_IMAGES_LAYERS = '..\\database\\layers\\'
IMAGES_PATH = '..\database\images_cv'

#SIFT
FILE_PATH_KEYPOINTS_SIFT = '..\\database\\vision\\sift\\keypoints\\'
FILE_PATH_DESCRIPTORS_SIFT = '..\\database\\vision\\sift\\descriptors\\'
FILE_PATH_IMAGE_SIFT = '..\\database\\vision\\sift\\images\\'
FILE_PATH_LOAD_KEYPOINTS_SIFT = "..\\database\\vision\\sift\\keypoints\\*"
FILE_PATH_LOAD_DESCRIPTORS_SIFT = "..\\database\\vision\\sift\\descriptors\\*"
FILE_PATH_IMAGE_LOAD_SIFT = "..\\database\\vision\\sift\\images\\*"

#SURF
FILE_PATH_KEYPOINTS_SURF = '..\\database\\vision\\surf\\keypoints\\'
FILE_PATH_DESCRIPTORS_SURF = '..\\database\\vision\\surf\\descriptors\\'
FILE_PATH_IMAGE_SURF = '..\\database\\vision\\surf\\images\\'
FILE_PATH_LOAD_KEYPOINTS_SURF = "..\\database\\vision\\surf\\keypoints\\*"
FILE_PATH_LOAD_DESCRIPTORS_SURF = "..\\database\\vision\\surf\\descriptors\\*"
FILE_PATH_IMAGE_LOAD_SURF = "..\\database\\vision\\surf\\images\\*"

# calculates the keypoint, descriptors and saves it to the database files
def create_file_database(type_alg, image_path, img, kpt, des):

     #get image name, without complete path
    img_filename, _ = os.path.splitext(image_path)
    file_basename = basename(img_filename)

    if(type_alg == 'sift'):
        file_kp = FILE_PATH_KEYPOINTS_SIFT + file_basename
        file_desc = FILE_PATH_DESCRIPTORS_SIFT + file_basename
        file_img = FILE_PATH_IMAGE_SIFT + file_basename

    elif(type_alg == 'surf'):
        file_kp = FILE_PATH_KEYPOINTS_SURF + file_basename
        file_desc = FILE_PATH_DESCRIPTORS_SURF + file_basename
        file_img = FILE_PATH_IMAGE_SURF + file_basename
    else:
        print("Unknown algorithm when creating database.", flush=True)
        return

    pickle_tmp = pickle_keypoints(kpt)

    with open(file_kp, 'wb') as fp:
        pickle.dump(pickle_tmp, fp)
    
    
    with open(file_desc, 'wb') as fp:
        pickle.dump(des, fp)

    
    with open(file_img, 'wb') as fp:
        pickle.dump(img, fp)

# load the keypoints, descriptors and images in the database
def load_fileImages_database(type_alg):

    print("Loading database...", flush=True)

    file_kp = ""
    file_desc = ""
    file_img = ""

    if(type_alg == 'sift'):
        file_kp = FILE_PATH_LOAD_KEYPOINTS_SIFT
        file_desc = FILE_PATH_LOAD_DESCRIPTORS_SIFT
        file_img = FILE_PATH_IMAGE_LOAD_SIFT

    elif(type_alg == 'surf'):
        file_kp = FILE_PATH_LOAD_KEYPOINTS_SURF
        file_desc = FILE_PATH_LOAD_DESCRIPTORS_SURF
        file_img = FILE_PATH_IMAGE_LOAD_SURF
    else:
        print("Unknown algorithm", flush=True)
        return

    file_list_keypoints = []
    for filename in glob.glob(file_kp):
        file_list_keypoints.append(filename)
    
    file_list_descriptors = []
    for filename in glob.glob(file_desc):
        file_list_descriptors.append(filename)

    file_list_image = []
    for filename in glob.glob(file_img):
        file_list_image.append(filename)
    
    
    #Create database if not exist
    if len(file_list_keypoints) < 1:
        print("no database for feature_points and descriptors", flush=True)
    elif len(file_list_image) < 1:
        print("no database for images cv", flush=True)
    elif(len(file_list_keypoints) != len(file_list_image) 
        | len(file_list_keypoints) != len(file_list_descriptors)  
        | len(file_list_image) != len(file_list_descriptors) ):

        print("database inconsistency", flush=True)
    else:

        all_images_cv = []
        for file in file_list_image:
            with open (file, 'rb') as fp:
                images_cv = pickle.load(fp)
                all_images_cv.append(images_cv)
        
        all_descriptors = []
        
        for file in file_list_descriptors:
            with open (file, 'rb') as fp:
                desc_tmp = pickle.load(fp)
                all_descriptors.append(desc_tmp)
        
        all_feature_points = []
        
        for file in file_list_keypoints:
            with open (file, 'rb') as fp:
                temp_kp = pickle.load(fp)
        
            feature_points = []

            for list_kp in temp_kp:
                temp_feature = unpickle_keypoints(list_kp)
                feature_points.append(temp_feature)
            
            all_feature_points.append(feature_points)
        
        print("LOAD COMPLETO", flush=True)
        return all_images_cv, all_feature_points, all_descriptors

# delete the saved images in the database    
def deleteImageFromDatabase(image, name):

    try:
        #Remove image
        os.remove(DATABASE_PATH_IMAGES + image)

        #Remove layer
        os.remove(DATABASE_PATH_IMAGES_LAYERS + name + '_layer.png')

        #Remove SIFT
        os.remove(FILE_PATH_KEYPOINTS_SIFT + name)
        os.remove(FILE_PATH_DESCRIPTORS_SIFT + name)
        os.remove(FILE_PATH_IMAGE_SIFT + name)
        
        #Remove SURF
        os.remove(FILE_PATH_KEYPOINTS_SURF + name)
        os.remove(FILE_PATH_DESCRIPTORS_SURF + name)
        os.remove(FILE_PATH_IMAGE_SURF + name)
    
    except OSError:
        pass
    
    