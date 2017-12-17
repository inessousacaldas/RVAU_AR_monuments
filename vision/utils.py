import os.path
import glob
from PIL import Image
from os.path import splitext, basename
import cv2
import numpy as np

DATABASE_PATH = '..\database\images\*.jpg'
LAYER_AR_PATH = '..\database\layers\\'

def get_image_layerAR(index):

    image_list = []
    for filename in glob.glob(DATABASE_PATH):
        image_list.append(filename)

    filename = image_list[index]
    layer_filename, _ = os.path.splitext(filename)

    layer_basename = basename(layer_filename)
    layer_filename = LAYER_AR_PATH + layer_basename + '_layer.png'

    return layer_filename


def pickle_keypoints(keypoints):
    temp_array = []
    for point in keypoints:
        temp = (point.pt, point.size, point.angle, point.response, point.octave,
        point.class_id)
        temp_array.append(temp)
    
    return temp_array

def unpickle_keypoints(array):
    keypoints = []

    for point in array:
        temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])
        keypoints.append(temp_feature)

    return keypoints