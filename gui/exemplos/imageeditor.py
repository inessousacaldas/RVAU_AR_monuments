from tkinter import *
from PIL import Image, ImageTk


import imagefeed
import imagefilefeed

IMAGE_DIRECTORY = "./images/"
POSITIVE_DIRECTORY = "./positive/"
NEGATIVE_DIRECTORY = "./negative/"
IMAGE_RESIZE_FACTOR = .2


class ImageEditor(Frame):
    """class ImageEditor provides functionality to page through photos so that users can  select a portion 
   of each photo to be saved separately as a 'positive' image and the rest to be saved separately as
   four 'negative' images"""

    def __init__(self, parent):
        """Initializes the window with access to an imagefeed class that supplies from and saves images to the appropriate locations"""
        Frame.__init__(self, parent)           
        self.parent = parent
        self.corners = []
        self.image_feed = imagefeed.ImageFeed(imagefilefeed.FileFeed(IMAGE_DIRECTORY, POSITIVE_DIRECTORY, NEGATIVE_DIRECTORY), IMAGE_RESIZE_FACTOR)
        self.image = self.image_feed.returnTKImage()
        self.canvas = None
        self.initUI()
        self.resetCanvas()


    def initUI(self):
        """Adds a Tkinter canvas element that tracks mouse clicks to select image region for saving"""
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Tkinter.Canvas(self, width = self.image.width(), height = self.image.height())       
        self.canvas.bind("<Button-1>", self.OnMouseDown)
        self.canvas.pack()

        nextButton = Button(self, text="Next", command=self.next)
        nextButton.place(x=0, y=0)

        resetButton = Button(self, text="Reset", command=self.reset)
        resetButton.place(x=0, y=22)


    def next(self):
        """Saves current edits and advances to the next image"""
        if len(self.corners) == 2:
            self.image_feed.writeImages(self.corners)
        self.image_feed.nextImage()
        self.reset()    


    def resetCanvas(self):
        """Resets all canvas elements without advancing forward"""
        self.image = self.image_feed.returnTKImage()
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        self.canvas.configure(height = self.image.height(), width = self.image.width())
        self.canvas.place(x = 0, y = 0, height = self.image.height(), width = self.image.width())


    def reset(self):
        """Removes all drawings on the canvas so user can start over on same image"""
        self.corners = []
        self.canvas.delete("all")
        self.resetCanvas()


    def OnMouseDown(self, event):
        """Records location of user clicks to establish cropping region"""
        self.corners.append([event.x, event.y])
        if len(self.corners) == 2:
            self.canvas.create_rectangle(self.corners[0][0], self.corners[0][1], self.corners[1][0], self.corners[1][1], outline ='cyan', width = 2)


def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = ImageEditor(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  