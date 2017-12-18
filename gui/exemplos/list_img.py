from tkinter import *
from PIL import Image, ImageTk
type_frame = Tk()

liste_boutton = ['img1_02','img1_03','img1_04','img1_05']

for num,button_name in enumerate(liste_boutton):
    button = Button(type_frame)
    button['bg'] = "grey72" 
    # this example works, if .py and images in same directory
    image = Image.open('.\images\{}.jpg'.format(button_name))
    image = image.resize((150, 100), Image.ANTIALIAS) # resize the image to ratio needed, but there are better ways
    photo = ImageTk.PhotoImage(image) # to support png, etc image files
    button.image = photo # save reference
    button.config(image=photo, width="150", height="100")
    # be sure to check the width and height of the images, so there is no cut off
    button.grid(row=num, column=0, pady=5, padx=8)

mainloop()

