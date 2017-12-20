from lib import *
from pyv import *
from PIL import ImageTk, Image
import pickle
import tkinter.ttk as ttk
from tkinter import colorchooser
from vision.choose import select_region
from vision.ar_labeling import arAppCompute
from vision.utils import get_number_of_files
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
VERSION = 5.0,1.0
AUTOR = "Ines Caldas and Joel Carneiro"
PROGRAM_TITLE = "MonumentAR"

#Configuration file
CONFIGURATION_FILE = PROGRAM_TITLE+".ini"

#Default configuration
C_DATA = [[1024, 768],"#000000","#FFFFFF","#FFFFFF",[5,5,[1,1],0,"miter"],2,3,"EN"]

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
BACKGROUND_WINDOW = '#37474F'
BUTTONS_COLOR = '#455A64'

LINE, OVAL, RECTANGLE, ARC = list(range(4))
PENCIL, THIN, THICK = list(range(3))

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
            self.sizeDatabase = get_number_of_files()

            #Window Creation
            self.main = Tk()
            style = ttk.Style()
            #style.configure('TButton', background='black')
            #style.configure('TButton', foreground='green')
            #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
            style.theme_use("xpnative")
            print(style.theme_names())
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
            self.main.bind("<Control-s>",self.saveImage)
            self.main.bind("<Control-S>",self.saveImage)
            self.main.bind("<Control-h>",self.help)
            self.main.bind("<Control-H>",self.help)
            self.main.bind("<Control-i>",self.insertFigureMenu)
            self.main.bind("<Control-I>",self.insertFigureMenu)

            #Menu
            menuBar = Menu(self.main)
            self.main.config(menu=menuBar)
            
            #File
            fileMenu = Menu(menuBar,tearoff=0)
            fileMenu.add_command(label="New    [Ctrl-N]",command=self.newImage)
            fileMenu.add_command(label="Save    [Ctrl-S]",command=self.saveImage)
            fileMenu.add_separator()
            fileMenu.add_command(label="Exit    [Ctrl-Q]",command=self.exit)
            menuBar.add_cascade(label="File",menu=fileMenu)

            #Settings
            settingsMenu = Menu(menuBar,tearoff=0)
            colorMenu = Menu(settingsMenu,tearoff=0)
            settingsMenu.add_cascade(label="Change Color",menu=colorMenu)
            colorMenu.add_command(label="Background",command=lambda:self.colorChange("background"))
            colorMenu.add_command(label="Main",command=lambda:self.colorChange("active"))
            settingsMenu.add_command(label="Tool Style",command=self.styleToolChange)
            settingsMenu.add_command(label="Tool Weight",command=self.toolWeightChange)
            menuBar.add_cascade(label="Settings",menu=settingsMenu)

            #Insert
            insertMenu = Menu(menuBar,tearoff=0)
            insertMenu.add_command(label="Arc",command= lambda: self.createFigure("arc"))
            insertMenu.add_command(label="Square",command= lambda: self.createFigure("square"))
            insertMenu.add_command(label="Image",command= lambda: self.createFigure("image"))
            insertMenu.add_command(label="Oval",command= lambda: self.createFigure("oval"))
            insertMenu.add_command(label="Polygn",command= lambda: self.createFigure("polygn"))
            insertMenu.add_command(label="Line",command= lambda: self.createFigure("line"))
            insertMenu.add_command(label="Text",command= lambda: self.createFigure("text"))
            menuBar.add_cascade(label="Insert",menu=insertMenu)

            #Tools
            toolsMenu = Menu(menuBar,tearoff=0)
            tMenu = Menu(toolsMenu,tearoff=0)
            tMenu.add_command(label="Pencil",command=lambda:self.tools("pencil"))
            tMenu.add_command(label="Thin Brush",command=lambda:self.tools("brushthin"))
            tMenu.add_command(label="Thick Brush",command=lambda:self.tools("brushthick"))
            menuBar.add_cascade(label="Tools",menu=tMenu)

            """
            #Help
            Help = Menu(menuBar,tearoff=0)
            Help.add_command(label="Acerca de",command=self.acercade)
            Help.add_command(label="help    [Ctrl-A]",command=self.help)
            Help.add_command(label="Changelog",command=self.changelog)
            Help.add_command(label="Licencia",command=self.licence)
            menuBar.add_cascade(label="help",menu=Help)
            """

            #Draw Frame
            ParentFrame = Frame(self.main, background=BACKGROUND_WINDOW)
            ParentFrame.grid()
            
            #Draw Canvas
            windowFrame = Frame(ParentFrame, background=BACKGROUND_WINDOW)
            windowFrame.grid_rowconfigure(0, weight=1)
            windowFrame.grid_columnconfigure(0, weight=1)
            windowFrame.grid(row=0, column=0, sticky="nsew")
            windowFrame2 = Frame(ParentFrame, background=BACKGROUND_WINDOW)
            windowFrame2.grid_rowconfigure(0, weight=1)
            windowFrame2.grid_columnconfigure(0, weight=1)
            windowFrame2.grid(row=0, column=0, sticky="nsew")

            windowFrame2.lower()
            
            self.screen = Canvas(windowFrame,width=PROGRAM_SIZE[0]*0.8, height=PROGRAM_SIZE[1],bg=DEFAULT_BACKGROUND)
            self.screenSave = Canvas(windowFrame2,width=PROGRAM_SIZE[0]*0.8, height=PROGRAM_SIZE[1],bg=DEFAULT_BACKGROUND, relief="sunken")
            self.screen.grid()
            self.screenSave.grid()

            #Buttons
            Buttonframe = Frame(ParentFrame,border=5, background=BACKGROUND_WINDOW)
            Buttonframe.grid(row=0, column=1, sticky="NW")
            Label(Buttonframe,text="Tools",border=10).pack()
            
            ttk.Button(Buttonframe,text="Insert Icons",width=20,command=self.insertIcons, style="TButton").pack()

            b_undo = ttk.Button(Buttonframe,text="Undo",width=20,command=self.undoElement, style="TButton")
            image_undo = Image.open(DATAICONS + "eraser.png")
            image_undo = image_undo.resize((32,32), Image.ANTIALIAS)
            image_undo = ImageTk.PhotoImage(image_undo)
            b_undo.config(image=image_undo)
            b_undo.pack()

            b_pencil = ttk.Button(Buttonframe,text="Pencil",width=20,command=lambda:self.tools("pencil"), style="TButton")
            image_pencil = Image.open(DATAICONS + "pencil.png")
            image_pencil = image_pencil.resize((32,32), Image.ANTIALIAS)
            image_pencil = ImageTk.PhotoImage(image_pencil)
            b_pencil.config(image=image_pencil)
            b_pencil.pack()

            ttk.Button(Buttonframe,text="Thin Brush",width=20,command=lambda:self.tools("brushthin"), style="TButton").pack()
              
            ttk.Button(Buttonframe,text="Thick Brush",width=20,command=lambda:self.tools("brushthick"), style="TButton").pack()
            
            ttk.Button(Buttonframe,text="Insert Object",width=20,command=self.insertFigureMenu, style="TButton").pack()

            #Insert Figures
            FiguresInsert = Frame(Buttonframe, background=BACKGROUND_WINDOW)
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

            b_arc = ttk.Button(FiguresInsert,text="Insert Arc",width=20,command=lambda:self.createFigure('arc'), style="TButton")
            image_arc = Image.open(DATAICONS + "arc.png")
            image_arc = image_arc.resize((32,32), Image.ANTIALIAS)
            image_arc = ImageTk.PhotoImage(image_arc)
            b_arc.config(image=image_arc)
            b_arc.pack(side=LEFT)
            
            #Tools info
            Label(Buttonframe,text="tools",border=10).pack()
            WeightPencil = Frame(Buttonframe, background=BACKGROUND_WINDOW)
            WeightPencil.pack()
            self.infoWeightPencil = Label(WeightPencil,text=str(self.toolWeight),border=3,font=10,width=2)
            self.infoWeightPencil.pack(side=LEFT)
            Label(WeightPencil,text="  ").pack(side=LEFT)
            ttk.Button(WeightPencil,text="Weight",command=self.toolWeightChange,width=9).pack()
            
            PencilStyle = Frame(Buttonframe, background=BACKGROUND_WINDOW)
            PencilStyle.pack()
            Label(PencilStyle,text=" ",border=3,font=10,width=2).pack(side=LEFT)
            Label(PencilStyle,text="  ").pack(side=LEFT)
            ttk.Button(PencilStyle,text="Style",command=self.styleToolChange,width=9).pack()

            #Color Information
            Label(Buttonframe,text="Colors",border=10).pack()
            activeColor = Frame(Buttonframe, background=BACKGROUND_WINDOW)
            activeColor.pack()
            self.infoactivedcolor = Canvas(activeColor,width=30,height=32,bg=self.activeColor)
            self.infoactivedcolor.pack(side=LEFT)
            
            b_color = ttk.Button(activeColor,text="Color 1",command=lambda:self.colorChange("active"),width=10)
            image_color = Image.open(DATAICONS + "paint.png")
            image_color = image_color.resize((32,32), Image.ANTIALIAS)
            image_color = ImageTk.PhotoImage(image_color)
            b_color.config(image=image_color)
            b_color.pack()

            activeColor = Frame(Buttonframe, background=BACKGROUND_WINDOW)
            activeColor.pack()
            self.infoactivedbackgroundcolor = Canvas(activeColor,width=30,height=32,bg=self.backgroundColor)
            self.infoactivedbackgroundcolor.pack(side=LEFT)
            
            b_colorBucket = ttk.Button(activeColor,text="Color 2",command=lambda:self.colorChange("background"),width=10)
            image_color_bucket = Image.open(DATAICONS + "paint2.png")
            image_color_bucket = image_color_bucket.resize((32,32), Image.ANTIALIAS)
            image_color_bucket = ImageTk.PhotoImage(image_color_bucket)
            b_colorBucket.config(image=image_color_bucket)
            b_colorBucket.pack()
            
            activeColor = Frame(Buttonframe, background=BACKGROUND_WINDOW)
            activeColor.pack()
            
            #Info for user
            Label(Buttonframe,height=1).pack()
            self.messageUser = Label(Buttonframe,text="",relief=GROOVE,width=30,height=5,justify=CENTER,wraplength=125)
            self.messageUser.pack()

            #Vision
            Label(Buttonframe,text="Vision",border=10).pack()
            ttk.Button(Buttonframe,text="Key Points",width=20,command=self.computeKeyPoints).pack()
            ttk.Button(Buttonframe,text="SIFT",width=20,command=lambda:self.arApp('sift')).pack()
            ttk.Button(Buttonframe,text="SURF",width=20,command=lambda:self.arApp('surf')).pack()


            # add bindings for clicking, dragging and releasing over
            # any object with the "icon" tag

            # this data is used to keep track of an 
            # item being dragged
            self._drag_data = {"x": 0, "y": 0, "item": None, "itemSave": None}
            self.screen.tag_bind("icon", "<ButtonPress-3>", self.on_icon_press)
            self.screen.tag_bind("icon", "<ButtonRelease-3>", self.on_icon_release)
            self.screen.tag_bind("icon", "<B3-Motion>", self.on_icon_motion)


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
        
        if self.activeTool==PENCIL or self.activeTool==THIN or self.activeTool==THICK:
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
            if self.activeTool==THIN:
                elementS = self.screenSave.create_rectangle(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,outline = colorpaint)
                element = self.screen.create_rectangle(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,outline = colorpaint)
                
                self.stackElements.append(element)
                self.stackElementsSave.append(elementS)           
            
            elif self.activeTool==THICK:
                element = self.screen.create_oval(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,outline = colorpaint)
                elementS = self.screenSave.create_oval(event.x,event.y,event.x+self.toolStyle[0],event.y+\
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

    #New image
    def newImage(self,i="null"):
        if self.draw:
            resp = pyv("Save",DATAICONS+"alert.ico","save",(250,80))
            resp.root.mainloop(1)
            if resp.value!=0:
                if resp.value: self.saveImage()
        self.messageUser.config(text="")
        self.screen.create_rectangle(0,0,2*PROGRAM_SIZE[0], 2*PROGRAM_SIZE[1],fill=DEFAULT_BACKGROUND)
        self.draw = False

    #Save imagen
    def saveImage(self,i="null"):#TODO
        if self.draw:
            self.screen.update()
            self.screenSave.update()
            txt = pyv("Save",DATAICONS+"save.ico","savefile",(250,110))
            txt.root.mainloop(1)
            print(txt.value, flush=True)
            
            if txt.value!=0:
                filename = DATASAVES+str(txt.value)+DEFAULT_EXTENSION
                print('as', self.screenSave.size, flush=True)
                self.screenSave.postscript(file=filename, colormode='color',  height = 770, pagewidth=819)

                img = Image.open(filename)
                print(img.size, flush=True)
                self.saveLayer(img)
                img.save(DATASAVES+str(txt.value) + '.png', 'png')
                self.draw = False

            else:
                filename = DATASAVES+DEFAULT_TITLE+DEFAULT_EXTENSION
                self.screenSave.postscript(file=filename)
                img = Image.open(filename)
                img.save(DATASAVES+str(txt.value) + '.png', 'png')
                self.draw = False
                self.saveLayer(img)
    
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
                if resp.value: self.saveImage()
        self.main.destroy()

    #Save Color Tools    - active, eraser
    def colorChange(self,tools):
        color = askcolor()
        color = color[1]
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

    #Change tools style
    def styleToolChange(self):
        a = pyv("Tools Style",DATAICONS+\
                "estilo.ico","style",(260,210),[self.toolStyle[0],self.toolStyle[1],\
                                                 self.toolStyle[2],self.toolStyle[3],\
                                                 self.toolStyle[4],[DEFAULT_TOOL_STYLE[0],\
                                                                            DEFAULT_TOOL_STYLE[1],\
                                                                            DEFAULT_TOOL_STYLE[2],\
                                                                            DEFAULT_TOOL_STYLE[3],\
                                                                            DEFAULT_TOOL_STYLE[4]]])
        a.root.mainloop(1)
        self.toolStyle[0] = a.styleValues[0]
        self.toolStyle[1] = a.styleValues[1]
        self.toolStyle[2] = a.styleValues[2]
        self.toolStyle[3] = a.styleValues[3]
        self.toolStyle[4] = a.styleValues[4]

    #Insert Icons
    def insertIcons(self,E=False):
        a = pyvi(self.main, "Insert icons",DATAICONS+"shaperound.ico","icons", (230,460))
        a.root.mainloop(0)  
        self._create_icon(a.value)
    
    #Insert Figures
    def insertFigureMenu(self,E=False):
        a = pyv("Insert Figure",DATAICONS+"shaperound.ico","insertfigure",(260,230))
        print('aqui', a.value, flush=True)
        a.root.mainloop(1)
        print('aqui', a.value, flush=True)
        self.createFigure(a.value)

    #Retornar la posicion del mouse en dos posiciones y crear alguna figurilla
    def callbackPos(self,event):
        if self.pos[0]==[0,0]:
            self.pos[0][0]=event.x
            self.pos[0][1]=event.y
        else:
            self.pos[1][0]=event.x
            self.pos[1][1]=event.y
            if self.activeFigure==1:
                self.screen.create_rectangle(self.pos[0][0],self.pos[0][1],self.pos[1][0],self.pos[1][1],\
                                               fill=self.backgroundColor,outline=self.activeColor)
                
            if self.activeFigure==2:
                self.screen.create_oval(self.pos[0][0],self.pos[0][1],self.pos[1][0],self.pos[1][1],\
                                          fill=self.backgroundColor,outline=self.activeColor)
                
            if self.activeFigure==3:
                self.screen.create_line(self.pos[0][0],self.pos[0][1],self.pos[1][0],self.pos[1][1],\
                                          fill=self.backgroundColor,width=self.toolWeight)
        
            if self.activeFigure==5:
                a = pyv("Crear arco",DATAICONS+"arc.ico","arco",(260,115))
                self.messageUser.config(text="Ingrese los grados de su arco, 0 para cancelar")
                a.root.mainloop(1)
                if a.value>0:
                    self.screen.create_arc(self.pos[0][0],self.pos[0][1],self.pos[1][0],self.pos[1][1],\
                                               fill=self.backgroundColor,outline=self.activeColor, extent=a.value)
            self.draw = True
            self.screen.bind("<ButtonPress-1>",self.breakpoint)
            self.tools(self.activeTool)
            self.pos=[[0,0],[0,0]]
            self.messageUser.config(text="")

    #Crear un poligono
    def crearPoligono(self,event):
        if self.vertices>0:
            self.messageUser.config(text="Haga click en la screen para definir los vertices de su figura, "+str(self.vertices-1)+" restantes")
            self.vertices-=1
            self.pointable.append([event.x,event.y])
        if self.vertices==0:
            self.screen.create_polygon(self.pointable,fill=self.backgroundColor,outline=self.activeColor)
            self.pointable=[]
            self.tools(self.activeTool)
            self.screen.bind("<ButtonPress-1>",self.breakpoint)
            self.messageUser.config(text="")
            self.draw = True

    #Insertar un texto
    def crearTexto(self,event):
        txt = pyv("Ingresar un texto",DATAICONS+"text.ico","insertartexto",(250,110))
        txt.root.mainloop(1)
        self.messageUser.config(text="")
        self.screen.create_text(event.x,event.y,text=txt.value,font="Arial")
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
            self.screen.bind("<ButtonPress-1>",self.crearTexto)
            self.messageUser.config(text="Haga click en el dibujo para poner su texto")
        if figura=="arc":
            self.screen.bind("<ButtonPress-1>",self.update_xy)
            self.screen.bind("<B1-Motion>",self.drawFigure)
            self.activeFigure = ARC
            self.messageUser.config(text="Drag to create arc")   
        
        if figura=="image":
            self.messageUser.config(text="Enter the location of your image.")
            filepath = askopenfilename(title="Open",initialdir="./",defaultextension=".jpg",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            self.messageUser.config(text="")
            if filepath!="": #TODO see if image file
                self.mainArchive=filepath
                
                print('database ', self.sizeDatabase)
                filename, file_extension = os.path.splitext(filepath)
                print(file_extension, flush=True)

                image = Image.open(filepath)                
                image = image.resize((int(PROGRAM_SIZE[0]*0.8), PROGRAM_SIZE[1]), Image.ANTIALIAS)
                name = DATABASE_PATH + 'img' + str(self.sizeDatabase) + file_extension
                image.save(name)
                self.imageBackgroundPath = name
                self.layerName = 'img' + str(self.sizeDatabase)
                image = ImageTk.PhotoImage(image)
               
                self.imageBackground = self.screen.create_image(0, 0, image = image, anchor = NW)
                
                self.main.mainloop(0)

        if figura =="polygn":
            a = pyv("Numero de aristas",DATAICONS+"shaperound.ico","vertices",(260,115))
            self.messageUser.config(text="Ingrese el numero de aristas que tendra su nueva figura, 0 para cancelar")
            a.root.mainloop(1)
            self.activeFigure = 4
            self.vertices = a.value
            if self.vertices>0:
                self.screen.bind("<ButtonPress-1>",self.crearPoligono)
                self.screen.bind("<B1-Motion>",self.breakpoint)
                self.messageUser.config(text="Haga click en la screen para definir los vertices de su figura, "+str(self.vertices)+" restantes")
            else:
                self.messageUser.config(text="")

    #Change tools - eraser, pencil, brushthin, brushthick
    def tools(self,herr):
        if herr=="pencil" or herr==1: self.activeTool=PENCIL
        if herr=="brushthin" or herr==3: self.activeTool=THIN
        if herr=="brushthick" or herr==4: self.activeTool=THICK
        self.screen.bind("<B1-Motion>",self.freeDraw)

    #Load window with help
    def help(self,i="null"):
        a = pyv("help",DATAICONS+"help.ico","help",(600,400),[PROGRAM_TITLE,DATADOCS+"help.TXT"])
        a.root.mainloop(0)

    #Insert image
    def insertImage(self,event):
        imagen = PhotoImage(file=self.mainArchive)
        self.screen.create_image(event.x,event.y,image=imagen)
        self.screen.update()
        imagen.name=None

    #Terminar de poner las imagenes
    def terminarImagen(self,i):
        self.messageUser.config(text="")
        self.screen.bind("<B1-Motion>",self.freeDraw)
        self.screen.bind("<ButtonPress-1>",self.breakpoint)
        self.mainArchive=""
        self.main.bind("<Escape>",self.breakpoint)

    #Cargar el acercade
    def acercade(self,i="null"):
        a = pyv("Acerca de "+PROGRAM_TITLE,DATAICONS+"coloricon.ico","about",(220,120),[AUTOR,VERSION[0],AUTORMAIL])
        a.root.mainloop(0)

    #Posicionar puntero
    def posPointer(self,event):
        self.befpoint=[0,0]

    #Lista de cambios del programa
    def changelog(self):
        a = pyv("Changelog",DATAICONS+"changelog.ico","changelog",(600,400),[PROGRAM_TITLE,DATADOCS+"CHANGELOG.TXT"])
        a.root.mainloop(0)

    #Licencia del programa
    def licence(self):
        a = pyv("Licencia GNU [English]",DATAICONS+"gnu.ico","licence",(600,400),[PROGRAM_TITLE,DATADOCS+"GNU.TXT"])
        a.root.mainloop(0)

    #Funcion para exit
    def breakpoint(self,breakeable):
        return


    #TODO
    def drawFigure(self, event):
        if self.activeFigure is None or self._obj is None:
            return
        x, y = self.lastx, self.lasty
        if self.activeFigure in (LINE, RECTANGLE, OVAL, ARC):
            self.screen.coords(self._obj, (x, y, event.x, event.y))
            self.screenSave.coords(self._objSave, (x, y, event.x, event.y))

    def update_xy(self, event):
        if self.activeFigure is None:
            return
        x, y = event.x, event.y
        
        if self.activeFigure == LINE:
            self._obj = self.screen.create_line((x, y, x, y), fill=self.activeColor,width=self.toolWeight)
            self._objSave = self.screenSave.create_line((x, y, x, y), fill=self.activeColor,width=self.toolWeight)
        
        elif self.activeFigure == RECTANGLE:
            self._obj = self.screen.create_rectangle((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor)
            self._objSave = self.screenSave.create_rectangle((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor)
        
        elif self.activeFigure == OVAL:
            self._obj = self.screen.create_oval((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor)
            self._objSave = self.screenSave.create_oval((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor)
        
        elif self.activeFigure == ARC:
            self._obj = self.screen.create_arc((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor)
            self._objSave = self.screenSave.create_arc((x, y, x, y), fill=self.backgroundColor,outline=self.activeColor)
        
        element = self._obj
        elementS = self._objSave
        self.stackElements.append(element)
        self.stackElementsSave.append(elementS)
        self.draw = True
        self.lastx, self.lasty = x, y


    #Icons Drag

    def _create_icon(self, filepath):
        if(filepath != None):
            print('aqui',filepath, flush=True)
            '''Create a icon at the given coordinate in the given color'''
            # load the .gif image file
            images = Image.open(filepath)
            images = images.resize((64,64), Image.ANTIALIAS)
            images = ImageTk.PhotoImage(images)
            im = self.screen.create_image(PROGRAM_SIZE[0]*0.8/2, PROGRAM_SIZE[1]/2, image=images, anchor=CENTER,tags="icon", state=NORMAL)
            imSave = self.screenSave.create_image(PROGRAM_SIZE[0]*0.8/2, PROGRAM_SIZE[1]/2, image=images, anchor=CENTER,tags="icon", state=NORMAL)
            self.stackElements.append(im)
            self.stackElementsSave.append(imSave)
            #TODO
            self.screen.repack()
            #PROGRAM_SIZE[0]*0.8/2, PROGRAM_SIZE[1]
            

    def on_icon_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.screen.find_closest(event.x, event.y)[0]
        self._drag_data["itemSave"] = self.screenSave.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_icon_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["itemSave"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_icon_motion(self, event):
        if(self._drag_data["item"] != None):
            '''Handle dragging of an object'''
            # compute how much the mouse has moved
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            # move the object the appropriate amount
            self.screen.move(self._drag_data["item"], delta_x, delta_y)
            self.screenSave.move(self._drag_data["item"], delta_x, delta_y)
            # record the new position
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

    ###########################
    #Vision

    def computeKeyPoints(self):
        print("Aqui", flush=True)
        print("imageBackgroundPath", self.imageBackgroundPath)
        if(self.imageBackgroundPath==""):
            #TODO add popup
            print("Select image first.")
        else:
            select_region(self.imageBackgroundPath)

    def arApp(self, algorithm):
        print("ArAPP", flush=True)
        filepath = askopenfilename(title="Open",initialdir=TEST_PATH,defaultextension=".jpg",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.messageUser.config(text="")
        #if filepath!="" and (filepath[len(filepath)-4:len(filepath)]==".jpg" or filepath[len(filepath)-4:len(filepath)]==".gif"):
        if filepath!="":
            print(filepath, flush=True)
            arAppCompute(filepath, algorithm, 0.6)


#Se carga la clase Paint
Paint()