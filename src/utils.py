import os.path
import glob
from PIL import Image
from os.path import splitext, basename

DATABASE_PATH = '..\database\images\*.jpg'
LAYER_AR_PATH = '..\database\layers\\'

def get_image_layerAR(index):

    image_list = []
    for filename in glob.glob(DATABASE_PATH):
        im=Image.open(filename)
        image_list.append(filename)

    
    filename = image_list[index]
    layer_filename, file_extension = os.path.splitext(filename)

    layer_basename = basename(layer_filename)
    layer_filename = LAYER_AR_PATH + layer_basename + '_layer.png'

    return layer_filename
