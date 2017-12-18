from lib import *
from pyv import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle

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

#Program Information
VERSION = 5.0,1.0
AUTOR = "Ines Caldas and Joel Carneiro"
PROGRAM_TITLE = "MonumentAR"

#Configuration file
CONFIGURATION_FILE = PROGRAM_TITLE+".ini"

#Default configuration
C_DATA = [[1024, 768],"#000000","#FFFFFF","#FFFFFF",[5,5,[1,1],0,"miter"],20,3,"EN"]

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
DEFAULT_EXTENSION = ".is"

#Variables Configuration
PROGRAM_SIZE = C_DATA[0]
DEFAULT_COLOR = C_DATA[1]
DEFAULT_ERASER = C_DATA[2]
DEFAULT_BACKGROUND = C_DATA[3]
DEFAULT_TOOL_STYLE = C_DATA[4]
DEFAULT_TOOL_WEIGHT = C_DATA[5]
DEFAULT_TOOL = C_DATA[6]

#Class paint
class Paint:

    #Constructor
    def __init__(self):

        try:
            #Draw variables
            self.pos = [[0,0],[0,0]]
            self.activeFigure = 0
            self.vertices = 0
            self.pointable = []
            self.befpoint = [0,0]
            self.title = DEFAULT_TITLE
            self.activeTool = DEFAULT_TOOL
            self.activeColor = DEFAULT_COLOR
            self.backgroundColor = DEFAULT_COLOR
            self.eraserColor = DEFAULT_ERASER
            self.toolWeight = DEFAULT_TOOL_WEIGHT
            self.toolStyle = [DEFAULT_TOOL_STYLE[0],DEFAULT_TOOL_STYLE[1],DEFAULT_TOOL_STYLE[2],\
                                      DEFAULT_TOOL_STYLE[3],DEFAULT_TOOL_STYLE[4]]
            self.draw = False
            self.mainArchive = ""

            #Window Creation
            self.main = Tk()
            self.main.focus_force()
            print(PROGRAM_SIZE)
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
            colorMenu.add_command(label="Eraser",command=lambda:self.colorChange("eraser"))
            colorMenu.add_command(label="Main",command=lambda:self.colorChange("active"))
            settingsMenu.add_command(label="Tool Style",command=self.styleToolChange)
            settingsMenu.add_command(label="Tool Weight",command=self.toolWeightChange)
            menuBar.add_cascade(label="Settings",menu=settingsMenu)

            #Insert
            insertMenu = Menu(menuBar,tearoff=0)
            insertMenu.add_command(label="Arch",command= lambda: self.createFigure("arch"))
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
            tMenu.add_command(label="Eraser",command=lambda:self.tools("eraser"))
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
            ParentFrame = Frame(self.main)
            ParentFrame.grid()

            #Draw Canvas
            windowFrame = Frame(ParentFrame)
            #windowFrame.pack(side=LEFT)
            windowFrame.grid_rowconfigure(0, weight=1)
            windowFrame.grid_columnconfigure(0, weight=1)
            windowFrame.grid(row=0, column=0, sticky="nsew")
            windowFrame2 = Frame(ParentFrame)
            #windowFrame2.pack()
            windowFrame2.grid_rowconfigure(0, weight=1)
            windowFrame2.grid_columnconfigure(0, weight=1)
            windowFrame2.grid(row=0, column=0, sticky="nsew")

            windowFrame2.lower()
            
            self.screen = Canvas(windowFrame,width=PROGRAM_SIZE[0]*0.8, height=PROGRAM_SIZE[1],bg=DEFAULT_BACKGROUND)
            self.screenSave = Canvas(windowFrame2,width=PROGRAM_SIZE[0]*0.8, height=PROGRAM_SIZE[1],bg=DEFAULT_BACKGROUND, relief="sunken")
            
            self.screen.grid()
            self.screenSave.grid()
            #self.screen.pack(expand = YES, fill = BOTH)
            #self.screenSave.pack(expand = YES, fill = BOTH)
            
            #Buttons
            Buttonframe = Frame(ParentFrame,border=5)
            Buttonframe.grid(row=0, column=1, sticky="NW")
            Label(Buttonframe,text="tools",border=10).pack()
            Button(Buttonframe,text="Eraser",relief=GROOVE,width=20,command=lambda:self.tools("eraser")).pack()
            Button(Buttonframe,text="Pencil",relief=GROOVE,width=20,command=lambda:self.tools("pencil")).pack()
            Button(Buttonframe,text="Thin Brush",relief=GROOVE,width=20,command=lambda:self.tools("brushthin")).pack()
            Button(Buttonframe,text="Thick Brush",relief=GROOVE,width=20,command=lambda:self.tools("brushthick")).pack()
            Button(Buttonframe,text="Insert Object",relief=GROOVE,width=20,command=self.insertFigureMenu).pack()

            #Tools info
            Label(Buttonframe,text="tools",border=10).pack()
            WeightPencil = Frame(Buttonframe)
            WeightPencil.pack()
            self.infoWeightPencil = Label(WeightPencil,text=str(self.toolWeight),border=3,font=10,width=2)
            self.infoWeightPencil.pack(side=LEFT)
            Label(WeightPencil,text="  ").pack(side=LEFT)
            Button(WeightPencil,text="Weight",relief=GROOVE,command=self.toolWeightChange,width=9).pack()
            PencilStyle = Frame(Buttonframe)
            PencilStyle.pack()
            Label(PencilStyle,text=" ",border=3,font=10,width=2).pack(side=LEFT)
            Label(PencilStyle,text="  ").pack(side=LEFT)
            Button(PencilStyle,text="Style",relief=GROOVE,command=self.styleToolChange,width=9).pack()

            #Color Information
            Label(Buttonframe,text="Colors",border=10).pack()
            activeColor = Frame(Buttonframe)
            activeColor.pack()
            self.infoactivedcolor = Canvas(activeColor,width=30,height=20,bg=self.activeColor)
            self.infoactivedcolor.pack(side=LEFT)
            Button(activeColor,text="Tool",relief=FLAT,command=lambda:self.colorChange("active"),width=10).pack()
            activeColor = Frame(Buttonframe)
            activeColor.pack()
            self.infoactivedbackgroundcolor = Canvas(activeColor,width=30,height=20,bg=self.backgroundColor)
            self.infoactivedbackgroundcolor.pack(side=LEFT)
            Button(activeColor,text="Background",relief=FLAT,command=lambda:self.colorChange("background"),width=10).pack()
            activeColor = Frame(Buttonframe)
            activeColor.pack()
            self.infoactivedcoloreraser = Canvas(activeColor,width=30,height=20,bg=self.eraserColor)
            self.infoactivedcoloreraser.pack(side=LEFT)
            Button(activeColor,text="Eraser",relief=FLAT,command=lambda:self.colorChange("eraser"),width=10).pack()

            #Info for user
            Label(Buttonframe,height=1).pack()
            self.messageUser = Label(Buttonframe,text="",relief=GROOVE,width=30,height=10,justify=CENTER,wraplength=125)
            self.messageUser.pack()

            #Init functions indev
            self.tools(self.activeTool)
            self.screen.bind("<ButtonRelease-1>",self.posPointer)

            #Window is created
            self.main.mainloop(0)

        except ValueError:
            print(ValueError)
            #lib("error","kernel",[2])
            #lib("error","kernel",[3])

    #Free draw
    def freeDraw(self,event):
        if self.activeTool==1 or self.activeTool==3 or self.activeTool==4:
            colorpaint = self.activeColor
        if self.activeTool==2:
            colorpaint = self.eraserColor
        if self.toolWeight==1:
            if self.befpoint==[0,0]:
                self.befpoint = [event.x,event.y]
            self.screen.create_line(event.x,event.y,self.befpoint[0]+self.toolStyle[0]-DEFAULT_TOOL_STYLE[0],self.befpoint[1]+\
                                  self.toolStyle[1]-DEFAULT_TOOL_STYLE[1], dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,smooth=self.toolStyle[3])
            self.screenSave.create_line(event.x,event.y,self.befpoint[0]+self.toolStyle[0]-DEFAULT_TOOL_STYLE[0],self.befpoint[1]+\
                                  self.toolStyle[1]-DEFAULT_TOOL_STYLE[1], dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,smooth=self.toolStyle[3])
            self.befpoint = [event.x,event.y]
        else:
            if self.activeTool==3:
                self.screenSave.create_rectangle(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,outline = colorpaint)
                self.screen.create_rectangle(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,outline = colorpaint)
                                 
            elif self.activeTool==4:
                self.screen.create_oval(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,outline = colorpaint)
                self.screenSave.create_oval(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,outline = colorpaint)
            else:
                self.screen.create_line(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,smooth=self.toolStyle[3])
                self.screenSave.create_line(event.x,event.y,event.x+self.toolStyle[0],event.y+\
                                  self.toolStyle[1],dash=self.toolStyle[2],\
                                  width=self.toolWeight,fill=colorpaint,smooth=self.toolStyle[3])
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
    def saveImage(self,i="null"):
        if self.draw:
            self.screen.update()
            self.screenSave.update()
            txt = pyv("Save",DATAICONS+"save.ico","savefile",(250,110))
            txt.root.mainloop(1)
            print(txt.value, flush=True)
            
            if txt.value!=0:
                filename = DATASAVES+str(txt.value)+DEFAULT_EXTENSION
        
                self.screenSave.postscript(file=filename, colormode='color')

                img = Image.open(filename)
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
        img.save("TransparentImage.png", "PNG")#converted Image name

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
        a = pyv("Change color",DATAICONS+"color.ico","changeColor",(280,440))
        a.root.mainloop(1)
        if a.value!=0:
            if tools=="active":
                self.activeColor = a.value
                self.infoactivedcolor.config(bg=self.activeColor)
            if tools=="eraser":
                self.eraserColor = a.value
                self.infoactivedcoloreraser.config(bg=self.eraserColor)
            if tools=="background":
                self.backgroundColor = a.value
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

    #Insert Figures
    def insertFigureMenu(self,E=False):
        a = pyv("Insert Figure",DATAICONS+"shaperound.ico","insertfigure",(260,230))
        a.root.mainloop(1)
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
            self.screen.bind("<ButtonPress-1>",self.callbackPos)
            self.screen.bind("<B1-Motion>",self.breakpoint)
            self.activeFigure = 1
            self.messageUser.config(text="Haga click en dos puntos del dibujo para crear un cuadrado")
        if figura=="oval":
            self.screen.bind("<ButtonPress-1>",self.callbackPos)
            self.screen.bind("<B1-Motion>",self.breakpoint)
            self.activeFigure = 2
            self.messageUser.config(text="Haga click en dos puntos del dibujo para crear un ovalo")
        if figura=="line":
            self.screen.bind("<ButtonPress-1>",self.callbackPos)
            self.screen.bind("<B1-Motion>",self.breakpoint)
            self.messageUser.config(text="Haga click en dos puntos del dibujo para crear una recta")
            self.activeFigure = 3
        if figura=="text":
            self.screen.bind("<ButtonPress-1>",self.crearTexto)
            self.messageUser.config(text="Haga click en el dibujo para poner su texto")
        if figura=="arch":
            self.screen.bind("<ButtonPress-1>",self.callbackPos)
            self.screen.bind("<B1-Motion>",self.breakpoint)
            self.activeFigure = 5
            self.messageUser.config(text="Haga click en dos puntos del dibujo para definir los limites de su arco")
        
        if figura=="image":
            self.messageUser.config(text="Ingrese la ubicacion de su imagen")
            filepath = askopenfilename(title="Open",initialdir="./",defaultextension=".jpg",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            self.messageUser.config(text="")
            #if filepath!="" and (filepath[len(filepath)-4:len(filepath)]==".jpg" or filepath[len(filepath)-4:len(filepath)]==".gif"):
            if filepath!="":
                self.mainArchive=filepath
                print(filepath, flush=True)

                self.imageBackgroundPath = filepath
                image = Image.open(filepath)
                image = image.resize((int(PROGRAM_SIZE[0]*0.8), PROGRAM_SIZE[1]), Image.ANTIALIAS)
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
        if herr=="pencil" or herr==1: self.activeTool=1
        if herr=="eraser" or herr==2: self.activeTool=2
        if herr=="brushthin" or herr==3: self.activeTool=3
        if herr=="brushthick" or herr==4: self.activeTool=4
        self.screen.bind("<B1-Motion>",self.freeDraw)

    #Cargar una ventana con helps
    def help(self,i="null"):
        a = pyv("help",DATAICONS+"help.ico","help",(600,400),[PROGRAM_TITLE,DATADOCS+"help.TXT"])
        a.root.mainloop(0)

    #Insertar una imagen
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

#Se carga la clase Paint
Paint()