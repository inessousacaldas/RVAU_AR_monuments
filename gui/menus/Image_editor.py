

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
from PIL import ImageFilter,ImageEnhance

import tkinter.messagebox
# rotate , filter , enhance , help

LARGE_FONT= ("Verdana", 12)
image_global = ""
canvas_current = ""
initial_img_load =0
ori_image = ""
class ImageEditor(tk.Tk):  #start the Tkinter root from the class args


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  # Initialize TKinter object

        #tk.Tk.iconbitmap(self,default='imageicon2.ico')
        tk.Tk.wm_title(self, "Image Editor")

        # Defining the Main frame
        container = tk.Frame(self) #This is the main start page
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)




        self.frames = {}     # This empty dictionary will contain all the page indexes


        for F in (StartPage, PageOne, PageTwo):
            # Defining the  frame object
            frame = F(container, self)
            #Putting an entry of  pages in dictionary above
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


    # def on_button(self,param):
    #     print(param)
    #     global  im,orisize
    #     im = Image.open(param)
    #     imgsize = [0,0]
    #     imgsize1=im.size
    #     imgsize.append(imgsize1[0])
    #     imgsize.append(imgsize1[1])
    #     orisize = tuple(imgsize)
    #     #im.show()
    #     return param
'''
    def image_rotate(self,rotate):
        if rotate == 45
            out = img.rotate(45)'''
# A function to be executed oon button press
def qf(param):
    print (param)


class StartPage(tk.Frame):
# The controller arguement given in the fucntion name called via dictionary is tk.Frame so we are passing in the class arguemnts itself
    def __init__(self, parent, controller):
# Here we are passing the controller tk.Frame via the class arguement itself so it will be dropeed in the the next init statement of tk.Frame in arguements
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="This is the start page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Image Editor",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Extra Image Page",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        label=ttk.Label(self,text="Enter File path:")
        label.pack(pady=10,padx=10)

        entry = ttk.Entry(self)
        entry.pack()
        path = entry.get()
        button4 = ttk.Button(self, text="Submit path",
                            command=lambda: self.on_button(entry.get()))
        button4.pack()


        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filtermenu = tk.Menu(menubar, tearoff=0)
        editmenu = tk.Menu(menubar, tearoff=0)
        enhancemenu = tk.Menu(menubar, tearoff=0)
        rotatemenu = tk.Menu(menubar, tearoff=0)
        helpmenu = tk.Menu(menubar, tearoff=0)

        rotatemenu.add_command(label="Rotate 45",command= lambda: self.rotate(image_global,45))
        rotatemenu.add_command(label="Rotate 90",command= lambda: self.rotate(image_global,90))
        rotatemenu.add_command(label="Rotate 180",command= lambda: self.rotate(image_global,180))
        rotatemenu.add_command(label="Rotate 270",command= lambda: self.rotate(image_global,270))
        rotatemenu.add_separator()
        rotatemenu.add_command(label="Flip Horizontal",command= lambda: self.transpose(image_global,"H"))
        rotatemenu.add_command(label="Flip vertical",command= lambda: self.transpose(image_global,"V"))

        filtermenu.add_command(label="Filter 1",command= lambda: self.image_filter(image_global,1))
        filtermenu.add_command(label="Filter 2",command= lambda: self.image_filter(image_global,2))
        filtermenu.add_command(label="To Black and White",command= lambda: self.image_filter(image_global,"L"))
        filtermenu.add_separator()
        filtermenu.add_command(label="Save to CMYK format",command= lambda: self.image_filter(image_global,"CMYK"))
        filtermenu.add_command(label="Save to RGB format",command= lambda: self.image_filter(image_global,"RGB"))

        helpmenu.add_command(label="Help Topics",command= lambda: self.image_enhance(image_global,2))

        editmenu.add_command(label="Resize",command= lambda: self.image_resize(image_global))
        editmenu.add_command(label="Crop",command= lambda: self.image_resize(image_global))

        filemenu.add_command(label="Save", command=lambda: self.image_save(image_global))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)

        enhancemenu.add_command(label="Image Contrast",command= lambda: self.rotate(image_global,45))
        enhancemenu.add_command(label="Image Brightness",command= lambda: self.rotate(image_global,90))
        enhancemenu.add_command(label="Image Sharpness",command= lambda: self.rotate(image_global,45))
        enhancemenu.add_command(label="Image Color",command= lambda: self.rotate(image_global,90))

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Edit", menu=editmenu)
        menubar.add_cascade(label="Rotate", menu=rotatemenu)
        menubar.add_cascade(label="Filter", menu=filtermenu)
        menubar.add_cascade(label="Enhance", menu=enhancemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        tk.Tk.config(controller, menu=menubar)





    def rotate(self,im,rotate_angle):
        global image_global
        print (im)
        im1= Image.open(im)

        if rotate_angle == 45:
            out = im1.rotate(45).save("intermediate2.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = "intermediate2.jpg"
            print (image_global)
        elif rotate_angle == 90:
            out = im1.rotate(90).save("intermediate1.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = "intermediate1.jpg"
            print (image_global)
        elif rotate_angle == 180:
            out = im1.rotate(180).save("intermediate1.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = "intermediate1.jpg"
            print (image_global)
        elif rotate_angle == 270:
            out = im1.rotate(270).save("intermediate1.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = "intermediate1.jpg"
            print (image_global)
        self.image_display(image_global)

    def transpose(self,im,transpose_direction):
        global image_global
        print (im)
        im1= Image.open(im)
        if transpose_direction == "H":
            out= im1.transpose(Image.FLIP_LEFT_RIGHT).save("intermediate1.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = "intermediate1.jpg"
        elif transpose_direction == "V":
            out= im1.transpose(Image.FLIP_TOP_BOTTOM).save("intermediate1.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = "intermediate1.jpg"
        self.image_display(image_global)

    def image_save(self,im):
        print (im)
        import time
        time1= time.strftime("_%m_%d_%Y_%H_%M_%S")
        my_image= ori_image.split(".")
        final= (my_image[0]+ time1)
        print (final)
        im1= Image.open(im).save( str(final)+ ".jpg" ,"JPEG", quality=100, optimize=True, progressive=True)
        tkinter.messagebox.showinfo("Notification","Image File saved as -->>  "+final+ ".jpg")

    def image_filter(self, im, mode):
        global image_global
        im1= Image.open(im)
        print (im1)
        print (im1.mode)
        try:
            r,g,b = im1.split()
        except:ValueError
        print ("The Image has Insufficient Color Bands to apply Filters")

        if mode == 1:
            out = Image.merge("RGB",(r,r,b)).save("intermediate1.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = "intermediate1.jpg"
            print (image_global)
        elif mode == 2:
            out= Image.merge("RGB",(g,r,b)).save("intermediate1.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = "intermediate1.jpg"
        elif mode == "L":
            out= im1.convert("L").save("intermediate1.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = "intermediate1.jpg"
        elif mode == "CMYK":
            print (ori_image)
            my_image= ori_image.split(".")
            out= im1.convert("CMYK").save(my_image[0]+"_CMYK.jpg" ,"JPEG", quality=100, optimize=True, progressive=True)
            image_global = im
        elif mode == "RGB":
            my_image= ori_image.split(".")
            out= im1.convert("RGB").save(my_image[0]+"_RGB.jpg","JPEG", quality=100, optimize=True, progressive=True)
            image_global = im
        self.image_display(image_global)

    def image_resize(self,im):
        global image_global
        im1= Image.open(im)
        print (im1)
        out = im1.resize((500,500), Image.ANTIALIAS).save("intermediate1.jpg","JPEG", quality=100, optimize=True, progressive=True)
        image_global = "intermediate1.jpg"
        self.image_display(image_global)

    def display_canvas(self,im,orisize):
        global canvas_current
        # print ("Inside function")

        if initial_img_load == 1:
            # print ("Inside IF loop")
            #canvas_current.delete("all")
            canvas_current.destroy()

        canvas=tk.Canvas(self,bg='#FFFFFF',width=1000,height=500,scrollregion=orisize)
        canvas_current = canvas

        hbar=tk.Scrollbar(canvas,orient="horizontal")
        hbar.pack(side="bottom",fill="x")
        hbar.config(command=canvas.xview)

        vbar=tk.Scrollbar(canvas,orient="vertical")
        vbar.pack(side="right",fill="y")
        vbar.config(command=canvas.yview)

        # canvas.config(width=800,height=600)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.pack(side="left",expand=True,fill="both")

        # print ("before delete")
        # print (im)
        #canvas.delete("all")
        canvas.pack(side="left",expand=True,fill="both")
        canvas.image = ImageTk.PhotoImage(im)
        #Add the image to the canvas, and set the anchor to the top left / north west corner
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')




    def image_display(self,image):

        if initial_img_load == 0:
            global ori_image
            ori_image = image
            print ("original_image--------->>  ",image)

        image1 = str(image)

        if ".jpg" in image1:
            im = Image.open(image)
        else:
            im = image
        imgsize = [0,0]
        try:
            imgsize1=im.size
            imgsize.append(imgsize1[0])
            imgsize.append(imgsize1[1])
        except:
            print ("Invalid File name or No File name Entered")

        orisize = tuple(imgsize)
        print (orisize)
        self.display_canvas(im,orisize)
        image_global = im
        # except:
        #     print ("Invalid File name or No File name Entered")
        #     import tkinter.messagebox
        #     tkinter.messagebox.showinfo("Alert!!","Invalid File name or No File name Entered")
        return im

    def on_button(self,param,*args):
        print(param)
        global image_global,initial_img_load
        image_global= param
        self.image_display(param)
        initial_img_load = 1





class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #frame=tk.Frame(self,width=1000,height=1000)


        im = Image.open('Img1.jpg')
        # print (im.size)
        imgsize = [0,0]
        imgsize1=im.size
        imgsize.append(imgsize1[0])
        imgsize.append(imgsize1[1])
        orisize = tuple(imgsize)
        #print (orisize)
        #print (im.format)


        #frame.grid(row=0,column=0)

        canvas=tk.Canvas(self,bg='#FFFFFF',width=1000,height=600,scrollregion=orisize)

        hbar=tk.Scrollbar(self,orient="horizontal")
        hbar.pack(side="bottom",fill="x")
        hbar.config(command=canvas.xview)

        vbar=tk.Scrollbar(self,orient="vertical")
        vbar.pack(side="right",fill="y")
        vbar.config(command=canvas.yview)

        # canvas.config(width=800,height=600)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.pack(side="left",expand=True,fill="both")

        canvas.image = ImageTk.PhotoImage(im)
        # Add the image to the canvas, and set the anchor to the top left / north west corner
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')


        # label = ttk.Label(frame, text="Image Page Two!!!", font=LARGE_FONT)
        # label.pack(side="top")
        #
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(side="bottom")
        #
        # button2 = ttk.Button(self, text="Page One",
        #                     command=lambda: controller.show_frame(PageOne))
        # button2.pack()




app = ImageEditor()

app.mainloop()