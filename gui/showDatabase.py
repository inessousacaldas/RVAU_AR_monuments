import glob
import os
import sys
import time

from PIL import Image, ImageTk

import tkinter as tk
import tkinter.ttk as ttk


def images(path):
    im = []

    for path in sys.path:
        im.extend(images_for(path))

    return sorted(im)


def images_for(path):
    if os.path.isfile(path):
        return [path]
    i = []
    for match in glob.glob("%s/*" % path):
        if match.lower()[-4:] in ('.jpg', '.png', '.gif'):
            i.append(match)
    return i

class showDatabase():
    def __init__(self, master, path, layerPath):
        self.master = master
        self.root = tk.Toplevel(master)
        self.value = None
        self.root.pack_propagate(False)
        self.root.config(bg="black", width=500, height=500)
        self._fullscreen = True
        self._images = images_for(path)
        self._imagesLayer = images_for(layerPath)
        self._image_pos = -1

        self.root.bind("<Return>", self.return_handler)
        self.root.bind("<space>", self.space_handler)
        self.root.bind("<Escape>", self.esc_handler)
        self.root.bind("<Left>", self.show_previous_image)
        self.root.bind("<Right>", self.show_next_image)
        self.root.bind("q", self.esc_handler)
        self.root.bind("f", self.f_handler)
        self.root.after(100, self.show_next_image)

        self.root.rowconfigure(3, minsize=500)
        self.root.columnconfigure(1, minsize=500)
        
        self.label = tk.Label(self.root, image=None)
        self.label.configure(borderwidth=0)
        self.label.grid(row=0, column=0, rowspan=2)
        tk.Button(self.root, text="New layer", command=lambda:self.editLayer()).grid(row=2, column=0, sticky=tk.SE, padx=10)
        tk.Button(self.root, text="Delete", command=lambda:self.deleteImage()).grid(row=2, column=0, sticky=tk.SE, pady=30, padx=10)

        self.set_timer()

    slide_show_time = 4
    last_view_time = 0
    paused = False
    image = None

    def editLayer(self):
        self.value = ('edit', self._images[self._image_pos])
        self.root.quit()
        self.root.destroy()
    
    def deleteImage(self):
        self.value = ('delete', self._images[self._image_pos])
        self.root.quit()
        self.root.destroy()

    def f_handler(self, e):
        self._fullscreen = not self._fullscreen
        if self._fullscreen:
            self.root.attributes('-fullscreen', True)
        else:
            self.root.attributes('-fullscreen', False)
            self.root.attributes("-zoomed", True)

    def esc_handler(self, e):
        self.root.destroy()

    def return_handler(self, e):
        self.show_next_image()

    def space_handler(self, _):
        self.paused = not self.paused

    def set_timer(self):
        self.root.after(300, self.update_clock)

    def update_clock(self):
        if time.time() - self.last_view_time > self.slide_show_time \
           and not self.paused:
            self.show_next_image()
        self.set_timer()
        self.check_image_size()

    def show_next_image(self, e=None):
        fname, fnameLayer = self.next_image()
        if not fname:
            return
        self.show_image(fname, fnameLayer)

    def show_previous_image(self, e=None):
        fname, fnameLayer = self.previous_image()
        if not fname:
            return
        self.show_image(fname, fnameLayer)

    def show_image(self, fname, fnameLayer):
        self.original_image = Image.open(fname)
        self.original_image_layer = Image.open(fnameLayer)
        self.image = None
        self.fit_to_box()
        self.last_view_time = time.time()

    def check_image_size(self):
        if not self.image:
            return
        self.fit_to_box()

    def fit_to_box(self):
        if self.image:
            if self.image.size[0] == self.box_width: return
            if self.image.size[1] == self.box_height: return
            
        width, height = self.original_image.size
        new_size = scaled_size(width, height, self.box_width, self.box_height)
        self.image = self.original_image.resize(new_size, Image.ANTIALIAS)
        
        self.label.place(x=self.box_width/2, y=self.box_height/2, anchor=tk.CENTER)
        
        resized_image = self.original_image_layer.resize(new_size, Image.ANTIALIAS)

        self.image.paste(resized_image, (0,0), resized_image)
        
        tkimage = ImageTk.PhotoImage(self.image)
        self.label.configure(image=tkimage)
        self.label.image = tkimage
       

    @property
    def box_width(self):
        return self.root.winfo_width()

    @property
    def box_height(self):
        return self.root.winfo_height()

    def next_image(self):
        if not self._images: 
            return None
        self._image_pos += 1
        self._image_pos %= len(self._images)
        return self._images[self._image_pos], self._imagesLayer[self._image_pos]

    def previous_image(self):
        if not self._images: 
            return None
        self._image_pos -= 1
        return self._images[self._image_pos], self._imagesLayer[self._image_pos]

def scaled_size(width, height, box_width, box_height):
    source_ratio = width / float(height)
    box_ratio = box_width / float(box_height)
    if source_ratio < box_ratio:
        return int(box_height/float(height) * width), box_height
    else:
        return box_width, int(box_width/float(width) * height)

def test_scaled_size():
    x = scaled_size(width=1871, height=1223, box_width=1920, box_height=1080)
    assert x == (1652, 1080)
    x = scaled_size(width=100, height=100, box_width=1920, box_height=1080)
    assert x ==(1080, 1080)
