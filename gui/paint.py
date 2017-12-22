from lib import *
from PIL import ImageTk, Image
import pickle
import tkinter.ttk as ttk
from tkinter import colorchooser
import tkinter.font as tkFont

from os.path import basename

from vision.choose import select_region, keypoints_default
from vision.ar_labeling import arAppCompute
from vision.utils import get_number_of_files, get_image_index
import vision.database as vdb
from gui.pyv import *
import gui.palette as palette
from gui.showDatabase import *


#Funciones intrinsecas de Paint
def isNumerable(x):
    if x.strip().isdigit():
        return True
    else:
        return False

#Constantes de carpetas
DATAFOLDER = "Data/"
DATASAVES = DATAFOLDER+"saves/"
DATADOCS = DATAFOLDER+"docs/"
DATALANG = DATAFOLDER+"langs/"
DATAICONS = DATAFOLDER+"icons/"
TEST_PATH = '../database/sample/'
DATABASE_PATH = '../database/images/'
DATABASE_LAYERS = '../database/layers/'

#Program Information
VERSION = 1.0,1.0
AUTOR = "\nInês Caldas\nJoel Carneiro"
PROGRAM_TITLE = "MonumentAR"

#Configuration file
CONFIGURATION_FILE = PROGRAM_TITLE+".ini"

#Default configuration
C_DATA = [[1048, 768],"#000000","#FFFFFF","#FFFFFF",[5,5,[1,1],0,"miter"],2,3,"EN"]

#Load Settings and Update C_DATA
try:
    conf_file = open(CONFIGURATION_FILE,"r")
    for i in conf_file:
        i = i.strip()
        c_command = i.split("=")
        if c_command[0].strip()=="PROGRAM_SIZE":
            c_after_command = str(c_command[1]).split(",")
            if isNumerable(c_after_command[0]): C_DATA[0][0]=int(c_after_command[0])
            if isNumerable(c_after_command[1]): C_DATA[0][1]=int(c_after_command[1])
        if c_command[0].strip()=="DEFAULT_COLOR": C_DATA[1]=str(c_command[1]).upper().strip()
        if c_command[0].strip()=="DEFAULT_ERASER": C_DATA[2]=str(c_command[1]).upper().strip()
        if c_command[0].strip()=="DEFAULT_BACKGROUND": C_DATA[3]=str(c_command[1]).upper().strip()
        if c_command[0].strip()=="DEFAULT_TOOL_STYLE":
            c_after_command = (c_command[1].strip().replace("[","").replace("]","")).split(",")
            if isNumerable(c_after_command[0]): C_DATA[4][0] = int(c_after_command[0])
            if isNumerable(c_after_command[1]): C_DATA[4][1] = int(c_after_command[1])
            if isNumerable(c_after_command[2]): C_DATA[4][2][0] = int(c_after_command[2])
            if isNumerable(c_after_command[3]): C_DATA[4][2][1] = int(c_after_command[3])
            if isNumerable(c_after_command[4]): C_DATA[4][3] = int(c_after_command[4])
            if len(c_after_command[5])>0 and (c_after_command[5]=="miter" or c_after_command[5]=="bevel" or c_after_command[5]=="round"):
                C_DATA[4][4] = c_after_command[5].replace("\"","").lower()
        if c_command[0].strip()=="DEFAULT_TOOL_WEIGHT":
            if isNumerable(c_command[1]): C_DATA[5]=int(c_command[1])
        if c_command[0].strip()=="DEFAULT_TOOL":
            if isNumerable(c_command[1]): C_DATA[6]=int(c_command[1])
        if c_command[0].strip()=="DEFAULT_LANGUAGE":
            C_DATA[7]=str(c_command[1]).strip().upper()
    conf_file.close()
except:
    lib("error","kernel",[1])
    lib("sonido","fatal")
    try:
        lib("conf_file",False,[CONFIGURATION_FILE,C_DATA])
        print ("IO/MESSAGE: New configuration file generated")
    except:
        print ("ERROR - 0,1: Cannot create configuration file")

#Default constants
DEFAULT_TITLE = "MonumentAR"
DEFAULT_EXTENSION = ".eps"

#Variables Configuration
PROGRAM_SIZE = C_DATA[0]
DEFAULT_COLOR = C_DATA[1]
DEFAULT_ERASER = C_DATA[2]
DEFAULT_BACKGROUND = C_DATA[3]
DEFAULT_TOOL_STYLE = C_DATA[4]
DEFAULT_TOOL_WEIGHT = C_DATA[5]
DEFAULT_TOOL = C_DATA[6]


LINE, OVAL, RECTANGLE, TEXT = list(range(4))
PENCIL, BRUSH = list(range(2))

#Class paint
class Paint:

    #Constructor
    def __init__(self):

        try:
            #Draw variables
            self.pos = [[0,0],[0,0]]
            self.activeFigure = None
            self._obj, self._objSave = None, None
            self.lastx, self.lasty = None, None
            self.vertices = 0
            self.pointable = []
            self.befpoint = [0,0]
            self.title = DEFAULT_TITLE
            self.activeTool = DEFAULT_TOOL
            self.activeColor = DEFAULT_COLOR
            self.backgroundColor = DEFAULT_COLOR
            self.toolWeight = DEFAULT_TOOL_WEIGHT
            self.toolStyle = [DEFAULT_TOOL_STYLE[0],DEFAULT_TOOL_STYLE[1],DEFAULT_TOOL_STYLE[2],\
                                      DEFAULT_TOOL_STYLE[3],DEFAULT_TOOL_STYLE[4]]
            self.draw = False
            self.mainArchive = ""
            self.imageBackgroundPath = ""
            self.layerName = ""
            #Elements draw on canvas
            self.stackElements = []
            self.stackElementsSave = []
            #Database images
            self.sizeDatabase = get_image_index()

            self.command = []
            #Window Creation
            self.main = Tk()
            #style = ttk.Style()
            #style.configure('TButton', background='black')
            #style.configure('TButton', foreground='green')
            #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
            #style.theme_use("xpnative")
            #print(style.theme_names())
            self.main.focus_force()
            self.main.geometry('%dx%d+%d+%d' % (PROGRAM_SIZE[0], PROGRAM_SIZE[1], (self.main.winfo_screenwidth() - PROGRAM_SIZE[0])/2,\
                                                 (self.main.winfo_screenheight() - PROGRAM_SIZE[1])/2))
            self.main.title(PROGRAM_TITLE)
            self.main.iconbitmap(DATAICONS+"coloricon.ico")
            self.main.minsize(PROGRAM_SIZE[0], PROGRAM_SIZE[1])
            self.main.resizable(width=False, height=False)

            #Window events
            self.main.bind("<Control-Q>",self.exit)
            self.main.bind("<Control-q>",self.exit)
            self.main.bind("<Control-N>",self.newImage)
            self.main.bind("<Control-n>",self.newImage)
            self.main.bind("<Control-s>",self.saveImageLayer)
            self.main.bind("<Control-S>",self.saveImageLayer)
            self.main.bind("<Control-h>",self.help)
            self.main.bind("<Control-H>",self.help)
            

            #Buttons Style
            """
            s = ttk.Style()
            s.configure("TButton", padding=6, background="blue")
            s.configure('Wild.TButton',
                background='black',
                foreground='white',
                highlightthickness='20',
                font=('Helvetica', 10, 'bold'))
            s.map('Wild.TButton',
                foreground=[('disabled', 'yellow'),
                            ('pressed', 'red'),
                            ('active', 'blue')],
                background=[('disabled', 'magenta'),
                            ('pressed', '!focus', 'cyan'),
                            ('active', 'green')],
                highlightcolor=[('focus', 'green'),
                                ('!focus', 'red')],
                relief=[('pressed', 'groove'),
                        ('!pressed', 'ridge')])
            """
            #Menu
            menuBar = Menu(self.main)
            self.main.config(menu=menuBar)
            
            #File
            fileMenu = Menu(menuBar,tearoff=0)
            fileMenu.add_command(label="New    [Ctrl-N]",command=self.newImage)
            fileMenu.add_command(label="Save    [Ctrl-S]",command=self.saveImageLayer)
            fileMenu.add_separator()
            fileMenu.add_command(label="Exit    [Ctrl-Q]",command=self.exit)
            menuBar.add_cascade(label="File",menu=fileMenu)

            #Settings
            settingsMenu = Menu(menuBar,tearoff=0)
            colorMenu = Menu(settingsMenu,tearoff=0)
            settingsMenu.add_cascade(label="Change Color",menu=colorMenu)
            colorMenu.add_command(label="Color 1",command=lambda:self.colorChange("active"))
            colorMenu.add_command(label="Color 2",command=lambda:self.colorChange("background"))
            settingsMenu.add_command(label="Tool Weight",command=self.toolWeightChange)
            menuBar.add_cascade(label="Settings",menu=settingsMenu)

            #Insert
            insertMenu = Menu(menuBar,tearoff=0)
            #TODO: insertMenu.add_command(label="Arc",command= lambda: self.createFigure("arc"))
            insertMenu.add_command(label="Square",command= lambda: self.createFigure("square"))
            insertMenu.add_command(label="Oval",command= lambda: self.createFigure("oval"))
            insertMenu.add_command(label="Line",command= lambda: self.createFigure("line"))
            insertMenu.add_command(label="Text",command= lambda: self.createFigure("text"))
            insertMenu.add_command(label="Icon",command=lambda: self.insertIcons())
            
            menuBar.add_cascade(label="Insert",menu=insertMenu)

            #Tools
            toolsMenu = Menu(menuBar,tearoff=0)
            tMenu = Menu(toolsMenu,tearoff=0)
            tMenu.add_command(label="Pencil",command=lambda:self.tools("pencil"))
            tMenu.add_command(label="Brush",command=lambda:self.tools("brush"))
            menuBar.add_cascade(label="Tools",menu=tMenu)


            #Help
            Help = Menu(menuBar,tearoff=0)
            Help.add_command(label="About",command=self.about)
            Help.add_command(label="Help    [Ctrl-h]",command=self.help)
            Help.add_command(label="Changelog",command=self.changelog)
            Help.add_command(label="License",command=self.license)
            menuBar.add_cascade(label="Help",menu=Help)

            #Draw Frame
            ParentFrame = Frame(self.main, background=palette.BACKGROUND_WINDOW)
            ParentFrame.grid()
            
            #Draw Canvas
            windowFrame = Frame(ParentFrame, background=palette.BACKGROUND_WINDOW)
            windowFrame.grid_rowconfigure(0, weight=1)
            windowFrame.grid_columnconfigure(0, weight=1)
            windowFrame.grid(row=0, column=0, sticky="nsew")
            windowFrame2 = Frame(ParentFrame, background=palette.BACKGROUND_WINDOW)
            windowFrame2.grid_rowconfigure(0, weight=1)
            windowFrame2.grid_columnconfigure(0, weight=1)
            windowFrame2.grid(row=0, column=0, sticky="nsew")

            windowFrame2.lower()
            
            self.screen = Canvas(windowFrame,width=PROGRAM_SIZE[0]*0.7815, height=PROGRAM_SIZE[1],bg=palette.CANVAS_COLOR)
            self.screenSave = Canvas(windowFrame2,width=PROGRAM_SIZE[0]*0.7815, height=PROGRAM_SIZE[1],bg=DEFAULT_BACKGROUND, relief="sunken")
            self.screen.grid()
            self.screenSave.grid()

            #Buttons
            Buttonframe = Frame(ParentFrame,border=5, background=palette.BACKGROUND_WINDOW)
            Buttonframe.grid(row=0, column=1, sticky="NW")
            label = Label(Buttonframe,text="Tools",border=10, background=palette.BACKGROUND_WINDOW, fg=palette.LIGHT_GRAY)
            label.config(font=("Courier", 18, 'bold'))
            label.pack()

            #Tools

            ToolsFrame = Frame(Buttonframe)
            ToolsFrame.pack()

            b_undo = ttk.Button(ToolsFrame,text="Undo",width=20,command=self.undoElement, style="TButton")
            image_undo = Image.open(DATAICONS + "eraser.png")
            image_undo = image_undo.resize((32,32), Image.ANTIALIAS)
            image_undo = ImageTk.PhotoImage(image_undo)
            b_undo.config(image=image_undo)
            b_undo.pack(side=LEFT)

            b_pencil = ttk.Button(ToolsFrame,text="Pencil",width=20,command=lambda:self.tools("pencil"), style="TButton")
            image_pencil = Image.open(DATAICONS + "pencil.png")
            image_pencil = image_pencil.resize((32,32), Image.ANTIALIAS)
            image_pencil = ImageTk.PhotoImage(image_pencil)
            b_pencil.config(image=image_pencil)
            b_pencil.pack(side=LEFT)

            b_brush = ttk.Button(ToolsFrame,text="Brush",width=20,command=lambda:self.tools("brush"), style="TButton")
            image_brush = Image.open(DATAICONS + "brush.png")
            image_brush = image_brush.resize((32,32), Image.ANTIALIAS)
            image_brush = ImageTk.PhotoImage(image_brush)
            b_brush.config(image=image_brush)
            b_brush.pack(side=LEFT)

            b_text = ttk.Button(ToolsFrame,text="Text",width=20,command= lambda: self.createFigure("text"), style="TButton")
            image_text = Image.open(DATAICONS + "text.png")
            image_text = image_text.resize((32,32), Image.ANTIALIAS)
            image_text = ImageTk.PhotoImage(image_text)
            b_text.config(image=image_text)
            b_text.pack(side=LEFT)
                          
            #Insert Figures
            FiguresInsert = Frame(Buttonframe, background=palette.BACKGROUND_WINDOW)
            FiguresInsert.pack()

            b_line = ttk.Button(FiguresInsert,text="Insert Line",width=20,command=lambda:self.createFigure('line'), style="TButton")
            image_line = Image.open(DATAICONS + "line.png")
            image_line = image_line.resize((32,32), Image.ANTIALIAS)
            image_line = ImageTk.PhotoImage(image_line)
            b_line.config(image=image_line)
            b_line.pack(side=LEFT)

            b_square = ttk.Button(FiguresInsert,text="Insert Square",width=20,command=lambda:self.createFigure('square'), style="TButton")
            image_square = Image.open(DATAICONS + "square.png")
            image_square = image_square.resize((32,32), Image.ANTIALIAS)
            image_square = ImageTk.PhotoImage(image_square)
            b_square.config(image=image_square)
            b_square.pack(side=LEFT)
            
            b_oval = ttk.Button(FiguresInsert,text="Insert Oval",width=20,command=lambda:self.createFigure('oval'), style="TButton")
            image_oval = Image.open(DATAICONS + "circle.png")
            image_oval = image_oval.resize((32,32), Image.ANTIALIAS)
            image_oval = ImageTk.PhotoImage(image_oval)
            b_oval.config(image=image_oval)
            b_oval.pack(side=LEFT)

            b_icon = ttk.Button(FiguresInsert,text="Insert Icons",width=20,command=self.insertIcons, style="Wild.TButton")
            image_icon = Image.open(DATAICONS + "icon.png")
            image_icon = image_icon.resize((32,32), Image.ANTIALIAS)
            image_icon = ImageTk.PhotoImage(image_icon)
            b_icon.config(image=image_icon)
            b_icon.pack(side=LEFT)
            
            #Tools info
            label = Label(Buttonframe,text="Settings",border=10, background=palette.BACKGROUND_WINDOW, fg=palette.LIGHT_GRAY)
            label.config(font=("Courier", 18, 'bold'))
            label.pack()
            WeightPencil = Frame(Buttonframe, background=palette.BACKGROUND_WINDOW, width=32, height=32)
            WeightPencil.pack()
            self.infoWeightPencil = Label(WeightPencil,relief='groove' ,text=str(self.toolWeight),border=3,font=10,width=3, background=palette.CANVAS_COLOR, fg=palette.LIGHT_GRAY)
            self.infoWeightPencil.config(height=2, width=3)
            self.infoWeightPencil.pack(side=LEFT)
            
            
            b_weight = ttk.Button(WeightPencil,text="Weight",command=self.toolWeightChange,width=2)
            image_weight = Image.open(DATAICONS + "weight.png")
            image_weight = image_weight.resize((32,32), Image.ANTIALIAS)
            image_weight = ImageTk.PhotoImage(image_weight)
            b_weight.config(image=image_weight)
            b_weight.pack()
            
            
            #Color Information
            activeColor = Frame(Buttonframe, background=palette.BACKGROUND_WINDOW)
            activeColor.pack()
            self.infoactivedcolor = Canvas(activeColor,width=32,height=32,bg=self.activeColor)
            self.infoactivedcolor.pack(side=LEFT)
            
            b_color = ttk.Button(activeColor,text="Color 1",command=lambda:self.colorChange("active"),width=32)
            image_color = Image.open(DATAICONS + "paint.png")
            image_color = image_color.resize((32,32), Image.ANTIALIAS)
            image_color = ImageTk.PhotoImage(image_color)
            b_color.config(image=image_color)
            b_color.pack()

            activeColor = Frame(Buttonframe, background=palette.BACKGROUND_WINDOW)
            activeColor.pack()
            self.infoactivedbackgroundcolor = Canvas(activeColor,width=32,height=32,bg=self.backgroundColor)
            self.infoactivedbackgroundcolor.pack(side=LEFT)
            
            b_colorBucket = ttk.Button(activeColor,text="Color 2",command=lambda:self.colorChange("background"),width=10)
            image_color_bucket = Image.open(DATAICONS + "paint2.png")
            image_color_bucket = image_color_bucket.resize((32,32), Image.ANTIALIAS)
            image_color_bucket = ImageTk.PhotoImage(image_color_bucket)
            b_colorBucket.config(image=image_color_bucket)
            b_colorBucket.pack()
            
            activeColor = Frame(Buttonframe, background=palette.BACKGROUND_WINDOW)
            activeColor.pack()
            
            

            #Vision Buttons
            label = Label(Buttonframe,text="Vision",border=10, bg = palette.BACKGROUND_WINDOW, fg=palette.LIGHT_GRAY)
            label.config(font=("Courier", 18, 'bold'))
            label.pack()
            ttk.Button(Buttonframe,text="Add image",width=20,command=self.addImageDatabase, style="TButton").pack()
            ttk.Button(Buttonframe,text="Key Points",width=20,command=self.computeKeyPoints).pack()
            ttk.Button(Buttonframe,text="SIFT",width=20,command=lambda:self.arApp('sift')).pack()
            ttk.Button(Buttonframe,text="SURF",width=20,command=lambda:self.arApp('surf')).pack()
            ttk.Button(Buttonframe,text="Database",width=20,command=self.seeDatabase).pack()

            label = Label(Buttonframe,text="",border=10, bg = palette.BACKGROUND_WINDOW, fg=palette.LIGHT_GRAY)
            label.config(font=("Courier", 5, 'bold'))
            label.pack()

            self.ransac_value = Scale(Buttonframe, from_=0, to=50, label='Ransac Threshold', width=20, resolution=0.1, orient=HORIZONTAL, bg=palette.BACKGROUND_WINDOW, fg=palette.LIGHT_GRAY)
            self.ransac_value.pack(fill=BOTH)
            self.ransac_value.set(0.6)

            #Info for user
            Label(Buttonframe,height=1, background=palette.CANVAS_COLOR).pack()
            self.messageUser = Label(Buttonframe,text="",relief=GROOVE,width=30,height=5,justify=CENTER,wraplength=125, background=palette.CANVAS_COLOR)
            self.messageUser.config(fg=palette.LIGHT_GRAY)
            self.messageUser.pack()

            #Debug
            self.debug = BooleanVar()
            c = Checkbutton(Buttonframe, text="Debug", selectcolor=palette.CANVAS_COLOR, variable=self.debug, bg = palette.BACKGROUND_WINDOW, fg=palette.LIGHT_GRAY, command=self.changeDebugMode)
            c.pack(side=RIGHT)
            c.var = self.debug

            # add bindings for clicking, dragging and releasing over
            # any object with the "token" tag

            # this data is used to keep track of an 
            # item being dragged
            self._drag_data = {"x": 0, "y": 0, "item": None, "itemSave": None}
            self.screen.tag_bind("token", "<ButtonPress-3>", self.on_token_press)
            self.screen.tag_bind("token", "<ButtonRelease-3>", self.on_token_release)
            self.screen.tag_bind("token", "<B3-Motion>", self.on_token_motion)


            #Init functions indev
            self.tools(self.activeTool)
            self.screen.bind("<ButtonRelease-1>",self.posPointer)

            #Window is created
            self.main.mainloop(0)

        except ValueError:
            print(ValueError)
            #lib("error","kernel",[2])
            #lib("error","kernel",[3])

    #Undo Elements
    def undoElement(self):
        if(len(self.stackElements) > 0):
            element = self.stackElements.pop()
            self.screen.delete(element)
            self.draw = True
        if(len(self.stackElementsSave) > 0):
            element = self.stackElementsSave.pop()
            self.screenSave.delete(element)
            self.draw = True

    #Free draw
    def freeDraw(self,event):
        
        if self.activeTool==PENCIL or self.activeTool==BRUSH:
            colorpaint = self.activeColor
        
        if self.toolWeight==1:
            if self.befpoint==[0,0]:
                self.befpoint = [event.x,event.y]
            
            element = self.screen.create_line(event.x,event.y,self.befpoint[0]+self.toolStyle[0]-DEFAULT_TOOL_STYLE[0],self.befpoint[1]+\
                                  self.toolStyle[1]-DEFAULT_TOOL_STYLE[1], dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,smooth=self.toolStyle[3])
            elementS = self.screenSave.create_line(event.x,event.y,self.befpoint[0]+self.toolStyle[0]-DEFAULT_TOOL_STYLE[0],self.befpoint[1]+\
                                  self.toolStyle[1]-DEFAULT_TOOL_STYLE[1], dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,smooth=self.toolStyle[3])
            
            self.stackElements.append(element)
            self.stackElementsSave.append(elementS)

            self.befpoint = [event.x,event.y]
        
        else:
            if self.activeTool==BRUSH:
                elementS = self.screenSave.create_rectangle(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,outline = colorpaint)
                element = self.screen.create_rectangle(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,outline = colorpaint)
                
                self.stackElements.append(element)
                self.stackElementsSave.append(elementS)           
            
            else:
                element = self.screen.create_line(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,smooth=self.toolStyle[3])
                elementS = self.screenSave.create_line(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,smooth=self.toolStyle[3])
                
                self.stackElements.append(element)
                self.stackElementsSave.append(elementS)
        
        self.draw = True

    #New image database menu bar
    def newImage(self,i="null"):
        if self.draw:
            resp = pyv("Save",DATAICONS+"alert.ico","save",(250,80))
            resp.root.mainloop(1)
            if resp.value!=0:
                if resp.value: self.saveImageLayer()
        self.messageUser.config(text="")
        self.addImageDatabase()
        self.draw = False

    #Save imagen
    def saveImageLayer(self,i="null"):#TODO
        if self.draw:
            self.screen.update()
            self.screenSave.update()
            txt = pyv("Save",DATAICONS+"save.ico","save",(250,110))
            txt.root.mainloop(1)
            print(txt.value, flush=True)
            
            if txt.value:
                filename = DATASAVES+'tmp'+DEFAULT_EXTENSION
                print('as', self.screenSave.size, flush=True)
                self.screenSave.postscript(file=filename, colormode='color',  height = 770, pagewidth=819)

                img = Image.open(filename)
                print('size ', img.size, flush=True)
                self.saveLayer(img)
                img.save(DATASAVES+'tmp.png', 'png')
                self.draw = False

    #Save layer AR
    def saveLayer(self, img):
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        layerPath = DATABASE_LAYERS + self.layerName + '_layer.png'
        print('n', layerPath, flush=True)
        img.save(layerPath, "PNG")#converted Image name

    #exit the program
    def exit(self,i="null"):
        if self.draw:
            resp = pyv("Save",DATAICONS+"alert.ico","saveIt",(250,80))
            resp.root.mainloop(1)
            if resp.value!=0:
                if resp.value: self.saveImageLayer()
        self.main.destroy()

    #Save Color Tools    - active, eraser
    def colorChange(self,tools):
        color = askcolor()
        color = color[1]
        if((color == '#ffffff' ) | (color == '#FFFFFF')):
            color = '#fefefe'
            
        if color!=0:
            if tools=="active":
                self.activeColor = color
                self.infoactivedcolor.config(bg=self.activeColor)
            if tools=="eraser":
                self.eraserColor = color
                self.infoactivedcoloreraser.config(bg=self.eraserColor)
            if tools=="background":
                self.backgroundColor = color
                self.infoactivedbackgroundcolor.config(bg=self.backgroundColor)

    #Change weight of tools
    def toolWeightChange(self):
        a = pyv("Tools Weight",DATAICONS+"grosor.ico","weight",(260,450))
        a.root.mainloop(1)
        if a.value!=0:
            self.toolWeight = a.value
            self.infoWeightPencil.config(text=str(a.value))
    

    #Insert Icons
    def insertIcons(self,E=False):
        a = pyvi(self.main, "Insert icons",DATAICONS+"shaperound.ico","icons", (230,460))
        a.root.mainloop(0)  
        self._create_icon(a.value)
    
    #Create Text
    def createText(self,event):
        txt = pyv("Write text",DATAICONS+"text.ico","inserttext",(250,110))
        txt.root.mainloop(1)
        self.messageUser.config(text="")
        print('wie', self.toolWeight, flush=True)
        _font = tkFont.Font(font="Helvetica", size = 40, weight='bold')
        _obj = self.screen.create_text(event.x,event.y, text=txt.value,font = _font, fill=self.activeColor,activefill='red', justify=tk.CENTER, tags='token')
        _objSave = self.screenSave.create_text(event.x,event.y, text=txt.value,font = _font, fill=self.activeColor,activefill='red', justify=tk.CENTER, tags='token')
        
        self.stackElements.append(_obj)
        self.stackElementsSave.append(_objSave)

        self.screen.bind("<ButtonPress-1>",self.breakpoint)
        self.draw = True

    #Create figures
    def createFigure(self,figura):
        if figura=="square":
            self.screen.bind("<ButtonPress-1>", self.update_xy)
            self.screen.bind("<B1-Motion>", self.drawFigure)
            self.activeFigure = RECTANGLE
            self.messageUser.config(text="Drag to create rectangle")
        if figura=="oval":
            self.screen.bind("<ButtonPress-1>",self.update_xy)
            self.screen.bind("<B1-Motion>",self.drawFigure)
            self.activeFigure = OVAL
            self.messageUser.config(text="Drag to create oval")
        if figura=="line":
            self.screen.bind("<ButtonPress-1>", self.update_xy)
            self.screen.bind("<B1-Motion>", self.drawFigure)
            self.messageUser.config(text="Drag to create line")
            self.activeFigure = LINE
        if figura=="text":
            self.activeFigure = TEXT
            self.screen.bind("<ButtonPress-1>",self.createText)
            self.messageUser.config(text="Click where to put text")

    #Change tools - eraser, pencil, brush
    def tools(self,herr):
        if herr=="pencil" or herr==1: self.activeTool=PENCIL
        if herr=="brush" or herr==3: self.activeTool=BRUSH
        self.screen.bind("<B1-Motion>",self.freeDraw)

    #Load window with help
    def help(self,i="null"):
        a = pyv("help",DATAICONS+"help.ico","help",(600,400),[PROGRAM_TITLE,DATADOCS+"HELP.TXT"])
        a.root.mainloop(0)

    #Load About
    def about(self,i="null"):
        a = pyv("About "+PROGRAM_TITLE,DATAICONS+"coloricon.ico","about",(220,120),[AUTOR,VERSION[0]])
        a.root.mainloop(0)

    #Posicionar puntero
    def posPointer(self,event):
        self.befpoint=[0,0]

    #Lista de cambios del programa
    def changelog(self):
        a = pyv("Changelog",DATAICONS+"changelog.ico","changelog",(600,400),[PROGRAM_TITLE,DATADOCS+"CHANGELOG.TXT"])
        a.root.mainloop(0)

    #License of the program
    def license(self):
        a = pyv("Licencia GNU [English]",DATAICONS+"gnu.ico","license",(600,400),[PROGRAM_TITLE,DATADOCS+"GNU.TXT"])
        a.root.mainloop(0)

    #Exit function
    def breakpoint(self,breakeable):
        return


    #TODO
    def drawFigure(self, event):
        if self.activeFigure is None or self._obj is None:
            return
        x, y = self.lastx, self.lasty
        if self.activeFigure in (LINE, RECTANGLE, OVAL):
            self.screen.coords(self._obj, (x, y, event.x, event.y))
            self.screenSave.coords(self._objSave, (x, y, event.x, event.y))

    def update_xy(self, event):
        if self.activeFigure is None:
            return
        x, y = event.x, event.y
        
        if self.activeFigure == LINE:
            self._obj = self.screen.create_line((x, y, x, y), fill=self.activeColor,width=self.toolWeight, tags='token')
            self._objSave = self.screenSave.create_line((x, y, x, y), fill=self.activeColor,width=self.toolWeight, tags='token')
        
        elif self.activeFigure == RECTANGLE:
            self._obj = self.screen.create_rectangle((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor, tags='token')
            self._objSave = self.screenSave.create_rectangle((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor, tags='token')
        
        elif self.activeFigure == OVAL:
            self._obj = self.screen.create_oval((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor, tags='token')
            self._objSave = self.screenSave.create_oval((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor, tags='token')
        
        elif self.activeFigure == TEXT:
            self._obj = self.screen.create_text(x, y,text='a',font="Arial", tags='token')
            self._objSave = self.screen.create_text(x, y,text='a',font="Arial", tags='token')

        element = self._obj
        elementS = self._objSave
        self.stackElements.append(element)
        self.stackElementsSave.append(elementS)
        self.draw = True
        self.lastx, self.lasty = x, y

    #Token Drag
    def _create_icon(self, filepath):
        if(filepath != None):
            print('aqui',filepath, flush=True)
            '''Create a icon at the given coordinate in the given color'''
            # load the .gif image file
            images = Image.open(filepath)
            images = images.resize((64,64), Image.ANTIALIAS)
            images = ImageTk.PhotoImage(images)
            im = self.screen.create_image(PROGRAM_SIZE[0]*0.7815/2, PROGRAM_SIZE[1]/2, image=images, anchor=CENTER,tags="token", state=NORMAL)
            imSave = self.screenSave.create_image(PROGRAM_SIZE[0]*0.7815/2, PROGRAM_SIZE[1]/2, image=images, anchor=CENTER,tags="token", state=NORMAL)
            self.stackElements.append(im)
            self.stackElementsSave.append(imSave)
            mainloop()
            self.draw = True
            
    def on_token_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.screen.find_closest(event.x, event.y)[0]
        self._drag_data["itemSave"] = self.screenSave.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["itemSave"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_token_motion(self, event):
        if(self._drag_data["item"] != None):
            '''Handle dragging of an object'''
            # compute how much the mouse has moved
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            # move the object the appropriate amount
            self.screen.move(self._drag_data["item"], delta_x, delta_y)
            self.screenSave.move(self._drag_data["itemSave"], delta_x, delta_y)
            # record the new position
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
            self.draw = True

    ###########################
    #Vision

    def addImageDatabase(self):
        self.messageUser.config(text="Enter the location of your image.")
        filepath = askopenfilename(title="Open",initialdir="./",defaultextension=".jpg",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.messageUser.config(text="")
        
        if filepath!="": #TODO see if image file
            self.mainArchive=filepath
            
            filename, file_extension = os.path.splitext(filepath)

            image = Image.open(filepath)                
            image = image.resize((int(PROGRAM_SIZE[0]*0.7815), PROGRAM_SIZE[1]), Image.ANTIALIAS)

            namefile = ""
            if(self.sizeDatabase<10):
                namefile = 'img0' + str(self.sizeDatabase)
            else:
                namefile = 'img' + str(self.sizeDatabase)

            name = DATABASE_PATH + namefile + file_extension
            image.save(name)
            self.imageBackgroundPath = name
            self.layerName = namefile
            image = ImageTk.PhotoImage(image)
            
            self.imageBackground = self.screen.create_image(0, 0, image = image, anchor = NW, tags='image')
            self.screenSave.delete(ALL)
            self.sizeDatabase = get_image_index()
            
            #Create empty layer
            self.screen.update()
            self.screenSave.update()
            
            filename = DATASAVES+'temp'+DEFAULT_EXTENSION
            print('as', self.screenSave.size, flush=True)
            self.screenSave.postscript(file=filename, colormode='color',  height = 770, pagewidth=819)

            img = Image.open(filename)
            print(img.size, flush=True)
            self.saveLayer(img)
            img.save(DATASAVES+'temp' + '.png', 'png')

            #Calculates default keypoints and descriptors
            keypoints_default(self.imageBackgroundPath, self.debug.get())

            self.main.mainloop()

    def seeDatabase(self):
        num_files = get_number_of_files()
        
        if(num_files == 0):
            self.messageUser.config(text="Database empty.")
        
        else:
            database = showDatabase(self.main, DATABASE_PATH, DATABASE_LAYERS)
            database.root.mainloop(0)  
            if(database.value != None):
                if(database.value[0] == 'edit'):
                    self.editLayer(database.value[1])
                elif(database.value[0] == 'delete'):
                    self.deleteImageDatabase(database.value[1])

    def editLayer(self, filepath):
        filename, file_extension = os.path.splitext(filepath)
        index = basename(filename).replace('img', '')
       
        image = Image.open(filepath)                
        image = image.resize((int(PROGRAM_SIZE[0]*0.7815), PROGRAM_SIZE[1]), Image.ANTIALIAS)
        self.imageBackgroundPath = filepath
        self.layerName = 'img' + str(index)
        image = ImageTk.PhotoImage(image)
        
        self.screen.delete(ALL)
        self.screenSave.delete(ALL)
        self.stackElements = []
        self.stackElementsSave = []
        
        self.imageBackground = self.screen.create_image(0, 0, image = image, anchor = NW, tags='image')
        
        self.sizeDatabase = get_image_index()
        
        #Create empty layer
        self.screen.update()
        self.screenSave.update()

        self.main.mainloop(0)

    def deleteImageDatabase(self, filepath):
        filename, file_extension = os.path.splitext(filepath)
        index = basename(filename).replace('img', '')
        filepath = filepath.replace('\\','/')
        base_file = basename(filepath)
        print('delete a', filepath, self.imageBackgroundPath, flush=True)
        name = 'img' + str(index)

        if(filepath == self.imageBackgroundPath):
            print('delete curr', index, flush=True)
            self.cleanCanvas()

        vdb.deleteImageFromDatabase(base_file, name)
  
    def cleanCanvas(self):
        self.imageBackground = None
        self.imageBackgroundPath = ""
        self.layerName = ""
        self.sizeDatabase = get_image_index()

        self.screen.delete(ALL)
        self.screenSave.delete(ALL)
        self.stackElements = []
        self.stackElementsSave = []

        #Create empty layer
        self.screen.update()
        self.screenSave.update()

        self.main.mainloop(0)

    def computeKeyPoints(self):
        print("Aqui", flush=True)
        print("imageBackgroundPath", self.imageBackgroundPath)
        if(self.imageBackgroundPath==""):
            self.messageUser.config(text="Select image first.")
            print("Select image first.")
        else:
            select_region(self.imageBackgroundPath, self.debug.get())

    def arApp(self, algorithm):
        num_files = get_number_of_files()
        
        if(num_files == 0):
            self.messageUser.config(text="Database empty.")
        
        else:
            filepath = askopenfilename(title="Open",initialdir=TEST_PATH,defaultextension=".jpg",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            self.messageUser.config(text="")
            #if filepath!="" and (filepath[len(filepath)-4:len(filepath)]==".jpg" or filepath[len(filepath)-4:len(filepath)]==".gif"):
            if filepath!="":
                print(filepath, flush=True)
                arAppCompute(filepath, algorithm, self.ransac_value.get(), self.debug.get())

    def changeDebugMode(self):
        if(self.debug.get()):
            print('Debug mode activated.', flush=True)
        else:
            print('Debug mode deactivated.', flush=True)
        

#Run class Paint
Paint()