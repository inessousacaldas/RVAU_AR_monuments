import cv2
from PIL import Image, ImageTk

class ImageFeed:
    """ The ImageFeed class manages all operations related to loading, saving, and formatting 
        images for presentation. The ImageFeed has a member file manager that determines what
        files it loads. The ImageFeed supplies a TkinterImage to requester objects."""

    def __init__(self, file_feed, rescale_factor):
        self.file_feed = file_feed
        self.rescale_factor = rescale_factor
        self.image = None
        self.cv_img = None
        self.nextImage()


    def returnTKImage(self):
        return self.image


    def nextImage(self):
        """ Calls the file feed's method to advance in the file list and then loads and formats
            the next image file."""
        img = cv2.imread(self.file_feed.next_file())            
        self.cv_img = img
        img_small = cv2.resize(img, (0,0), fx = self.rescale_factor, fy = self.rescale_factor)
        b, g, r = cv2.split(img_small)
        img_small = cv2.merge((r,g,b))
        im = Image.fromarray(img_small)
        self.image = ImageTk.PhotoImage(image=im)       


    def writeImages(self, corners):
        """ Writes the single 'positive' image to the positive directory and the four 'negative' images to the negative directory.
            The 'negative' images are the four rectangles around the positive image that do not contain the positive image. The 
            parameter corners supplies two diagonal points of the rectangle enclosing the 'positive' region of the image."""
        new_img = self.cv_img[corners[0][1]/self.rescale_factor:corners[1][1]/self.rescale_factor, corners[0][0]/self.rescale_factor:corners[1][0]/self.rescale_factor]
        cv2.imwrite("".join(self.file_feed.get_positive_file()), new_img)

        low_x = min(corners[0][0], corners[1][0])/self.rescale_factor
        high_x = max(corners[0][0], corners[1][0])/self.rescale_factor
        low_y = min(corners[0][1], corners[1][1])/self.rescale_factor
        high_y = max(corners[0][1], corners[1][1])/self.rescale_factor
        neg_file_name = self.file_feed.get_negative_file();

        new_img = self.cv_img[ :low_y, :]
        cv2.imwrite("{}{}{}".format(neg_file_name[0], "LY", neg_file_name[1]), new_img)
        new_img = self.cv_img[ high_y: , :]
        cv2.imwrite("{}{}{}".format(neg_file_name[0], "HY", neg_file_name[1]), new_img)

        new_img = self.cv_img[ :, :low_x ]
        cv2.imwrite("{}{}{}".format(neg_file_name[0], "LX", neg_file_name[1]), new_img)
        new_img = self.cv_img[:,  high_x: ]
        cv2.imwrite("{}{}{}".format(neg_file_name[0], "HX", neg_file_name[1]), new_img)