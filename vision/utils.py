import os.path
import glob
from PIL import Image
from os.path import splitext, basename
import cv2
import numpy as np

DATABASE_PATH = '..\database\images\*'
LAYER_AR_PATH = '..\database\layers\\'

#Get the greater image number as index
def get_image_index():
    index = 1
    files = glob.glob(DATABASE_PATH)

    if(len(files) !=0):
        filename = os.path.splitext(files[-1])[0]
        index = basename(filename).replace('img', '')
        index = int(index) + 1
    
    return index

#Get the number of files in database images
def get_number_of_files():

    files = glob.glob(DATABASE_PATH)

    return len(files)
    
# Gets the database image name at index
def get_image_layerAR(index):

    image_list = []
    for filename in glob.glob(DATABASE_PATH):
        image_list.append(filename)

    filename = image_list[index]
    layer_filename, _ = os.path.splitext(filename)

    layer_basename = basename(layer_filename)
    layer_filename = LAYER_AR_PATH + layer_basename + '_layer.png'

    return layer_filename

# makes a mask using the two images
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

# convertes keypoint into a byte stream
def pickle_keypoints(keypoints):
    temp_array = []
    for point in keypoints:
        temp = (point.pt, point.size, point.angle, point.response, point.octave,
        point.class_id)     
        temp_array.append(temp)
    return temp_array

# the byte stream is converted back into an object hierarchy.
def unpickle_keypoints(point):
    temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])
  
    return temp_feature
