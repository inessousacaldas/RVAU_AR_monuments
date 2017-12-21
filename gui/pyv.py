#Archivo creador de ventanas
#Autor: Ines Caldas and Joel Carneiro

from lib import *
from tkinter.colorchooser import *
import glob
from PIL import ImageTk, Image
import tkinter.ttk as ttk
import tkinter

#Important Variables
DEFAULT_FONT_TITLE="Arial",10
DEFAULT_WIDTH_CANVASTREE = 38,30

#Function that returns true if num in [x,y]
def valueBetween(num,x,y):
    if (num>=x) and (num<=y): return True
    else: return False


class pyvi:
    
    
    #Constructor
    def __init__(self,master, title,icon,type_win,size, properties=[0,0,0,0,0]):
        self.master = master
        self.root = tkinter.Toplevel(master)

        self.value = 0
        
        self.root.geometry('%dx%d+%d+%d' % (size[0], size[1], (self.root.winfo_screenwidth() - size[0])/2,\
                                             (self.root.winfo_screenheight() - size[1])/2))
        self.root.iconbitmap(bitmap=icon)
        self.root.title(title)
        self.root.minsize(width=size[0], height=size[1])
        self.root.resizable(width=False, height=False)

        if type_win == 'icons':
            
            F = Frame(self.root)
            F.pack()

            FiguresInsert = Frame(F)
            FiguresInsert.pack()
        
            
            files = glob.glob('Data\icons_gui\*')
            
            i,j = 0,0
            n = 0
            b_lines = [None]*len(files)
            images = [None]*len(files)   
            for icon_file in files:
                b_lines[n] = ttk.Button(FiguresInsert,text="Insert Icon", command=lambda icon_file=icon_file:self.sendIcon(icon_file), width=20, style="TButton")
                images[n] = Image.open(icon_file)
                images[n] = images[n].resize((32,32), Image.ANTIALIAS)
                images[n] = ImageTk.PhotoImage(images[n])
                b_lines[n].config(image=images[n])
                b_lines[n].image = images[n]
                b_lines[n].grid(row=j, column=i)
                
                n = n + 1
                i = i + 1
                if(i > 4):
                    i = 0
                    j = j + 1
            
            b_cancel = ttk.Button(FiguresInsert, text="Cancel",command=lambda:self.sendIcon(None),width=10)
            b_cancel.grid(columnspan = 5, pady = 10)

    def sendIcon(self, filepath):
        
        self.value = filepath
        self.root.quit()
        self.root.destroy()

#Clase create windwos
class pyv:
    
    
    #Constructor
    def __init__(self,title,icon,type_win,size,properties=[0,0,0,0,0]):
        self.root = tkinter.Tk()
        #tkinter.Toplevel(self.root)
        self.value = 0
        
        self.root.geometry('%dx%d+%d+%d' % (size[0], size[1], (self.root.winfo_screenwidth() - size[0])/2,\
                                             (self.root.winfo_screenheight() - size[1])/2))
        self.root.iconbitmap(bitmap=icon)
        self.root.title(title)
        self.root.minsize(width=size[0], height=size[1])
        self.root.resizable(width=False, height=False)
        
        #Weight of Tools
        if type_win=="weight":
            Label(self.root,text="Weight",font=DEFAULT_FONT_TITLE,border=10).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=1)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 1",relief=GROOVE,command=lambda:self.weight(1),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=2)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 2",relief=GROOVE,command=lambda:self.weight(2),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=3)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 3",relief=GROOVE,command=lambda:self.weight(3),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=4)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 4",relief=GROOVE,command=lambda:self.weight(4),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=5)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 5",relief=GROOVE,command=lambda:self.weight(5),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=6)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 6",relief=GROOVE,command=lambda:self.weight(6),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=7)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 7",relief=GROOVE,command=lambda:self.weight(7),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=8)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 8",relief=GROOVE,command=lambda:self.weight(8),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=9)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 9",relief=GROOVE,command=lambda:self.weight(9),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=10)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 10",relief=GROOVE,command=lambda:self.weight(10),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=11)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 11",relief=GROOVE,command=lambda:self.weight(11),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=12)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 12",relief=GROOVE,command=lambda:self.weight(12),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=13)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 13",relief=GROOVE,command=lambda:self.weight(13),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+2,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=14)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 14",relief=GROOVE,command=lambda:self.weight(14),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=15)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 15",relief=GROOVE,command=lambda:self.weight(15),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+2,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=16)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 16",relief=GROOVE,command=lambda:self.weight(16),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=17)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 17",relief=GROOVE,command=lambda:self.weight(17),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+2,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=18)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 18",relief=GROOVE,command=lambda:self.weight(18),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=19)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 19",relief=GROOVE,command=lambda:self.weight(19),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+2,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=20)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 20",relief=GROOVE,command=lambda:self.weight(20),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=21)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 21",relief=GROOVE,command=lambda:self.weight(21),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+2,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=22)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 22",relief=GROOVE,command=lambda:self.weight(22),width=7).pack()
            
            #New thickness line
            F = Frame(self.root)
            F.pack()
            FA = Frame(F)
            FA.pack(side=LEFT)
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+1,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=23)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 23",relief=GROOVE,command=lambda:self.weight(23),width=7).pack(side=LEFT)
            Label(FA,text=" ").pack(side=LEFT)
            FA = Frame(F)
            FA.pack()
            F_C=Canvas(FA,width=DEFAULT_WIDTH_CANVASTREE[0],height=DEFAULT_WIDTH_CANVASTREE[1],bg="white")
            F_C.pack(side=LEFT)
            F_C.create_line(0,DEFAULT_WIDTH_CANVASTREE[1]/2+2,DEFAULT_WIDTH_CANVASTREE[0]+2,DEFAULT_WIDTH_CANVASTREE[1]/2+1,width=24)
            Label(FA,text=" ").pack(side=LEFT)
            Button(FA,text="Weight 24",relief=GROOVE,command=lambda:self.weight(24),width=7).pack()
            
        if type_win=="style":
            self.styleValues = properties
            Label(self.root,text="Tool Style",font=DEFAULT_FONT_TITLE,border=10).pack()
            
            #New line
            F = Frame(self.root,border=4)
            F.pack()
            F1 = Frame(F)
            F1.pack(side=LEFT)       
            Label(F1,text="X - [X>0]",width=9,justify=RIGHT).pack(side=LEFT)
            self.XPLUS = Entry(F1,width=4)
            self.XPLUS.insert(0, properties[0])
            self.XPLUS.pack()
            F2 = Frame(F)
            F2.pack()       
            Label(F2,text="Y - [Y>0]",width=9,justify=RIGHT).pack(side=LEFT)
            self.YPLUS = Entry(F2,width=4)
            self.YPLUS.insert(0, properties[1])
            self.YPLUS.pack()
            F3 = Frame(self.root,border=4)
            F3.pack()       
            Label(F3,text="DASH [N1,N2..]",width=15,justify=RIGHT).pack(side=LEFT)
            self.DASH = Entry(F3,width=7)
            self.DASH.insert(0, str(properties[2]).replace("[","").replace("]", "").replace(" ",""))
            self.DASH.pack()         
            F4 = Frame(self.root,border=4)
            F4.pack()       
            Label(F4,text="SMOOTH [0,1]",width=15,justify=RIGHT).pack(side=LEFT)
            self.SMOOTH = Entry(F4,width=3)
            self.SMOOTH.insert(0, str(properties[3]))
            self.SMOOTH.pack()          
            F5 = Frame(self.root,border=4)
            F5.pack()       
            Label(F5,text="JOINSTYLE (miter, bevel, round)",width=25,justify=RIGHT).pack(side=LEFT)
            self.JOIN = Entry(F5,width=6)
            self.JOIN.insert(0, str(properties[4]))
            self.JOIN.pack()             
            
            #Button
            Label(self.root,text="").pack()
            FB = Frame(self.root)
            FB.pack()
            Button(FB,text="Ok",command=self.enviarEstilo).pack(side=LEFT)
            Label(FB,text=" ").pack(side=LEFT)
            Button(FB,text="Restaurar",command=self.restaurarEstilo).pack(side=LEFT)
            self.defaultProperties=[properties[5][0],properties[5][1],properties[5][2],properties[5][3],properties[5][4]]
        
        #Menu insert figure
        if type_win=="insertfigure":
            Label(self.root,text="Insert figure",font=DEFAULT_FONT_TITLE,border=10).pack()
            Button(self.root, text="Arc",command=lambda:self.sendFigure("arc"),width=10,relief=GROOVE).pack()
            Button(self.root, text="Square",command=lambda:self.sendFigure("square"),width=10,relief=GROOVE).pack()
            Button(self.root, text="Image",command=lambda:self.sendFigure("image"),width=10,relief=GROOVE).pack()
            Button(self.root, text="Oval",command=lambda:self.sendFigure("oval"),width=10,relief=GROOVE).pack()
            Button(self.root, text="Polygn",command=lambda:self.sendFigure("polygon"),width=10,relief=GROOVE).pack()
            Button(self.root, text="Line",command=lambda:self.sendFigure("line"),width=10,relief=GROOVE).pack() 
            Button(self.root, text="Text",command=lambda:self.sendFigure("text"),width=10,relief=GROOVE).pack()
            print('a', flush=True)
            
        #Menu insert figura
        if type_win=="inserttext":
            Label(self.root,text="Insert Text",font=DEFAULT_FONT_TITLE,border=10).pack()
            self.texto = Entry(self.root)
            self.texto.pack()
            Label(self.root,text=" ").pack()
            Button(self.root, text="Write",command=self.enviarTexto,width=10,relief=GROOVE).pack()
            self.texto.focus_force()
            
        #Menu insertar figura
        if type_win=="savefile":
            Label(self.root,text="Choose name",font=DEFAULT_FONT_TITLE,border=10).pack()
            self.texto = Entry(self.root)
            self.texto.pack()
            Label(self.root,text=" ").pack()
            Button(self.root, text="Save",command=self.enviarTexto,width=10,relief=GROOVE).pack()
            self.texto.focus_force()
            
        #Menu numero de vertices
        if type_win=="vertices":
            Label(self.root,text="Numero de vertices",font=DEFAULT_FONT_TITLE,border=10).pack()
            self.numvertices = Entry(self.root)
            self.numvertices.pack()
            Label(self.root,text=" ").pack()
            Button(self.root, text="Continuar",command=self.enviarVertices,width=10,relief=GROOVE).pack()
            self.numvertices.focus_force()
            
        #Menu numero de vertices
        if type_win=="arc":
            Label(self.root,text="Longitud del arco",font=DEFAULT_FONT_TITLE,border=10).pack()
            self.arc = Entry(self.root)
            self.arc.pack()
            Label(self.root,text=" ").pack()
            Button(self.root, text="Continuar",command=self.enviarArco,width=10,relief=GROOVE).pack()
            self.arc.focus_force()
        
        #Menu numero de vertices
        if type_win=="save":
            lib("sonido","alerta")
            Label(self.root,text="Save?",font=DEFAULT_FONT_TITLE,border=10).pack()
            F = Frame(self.root)
            F.pack()
            Button(F, text="Yes",command=lambda:self.response("yes"),width=5,relief=GROOVE).pack(side=LEFT)
            Label(F, text=" ").pack(side=LEFT)
            Button(F, text="No",command=lambda:self.response("no"),width=5,relief=GROOVE).pack()
            
        #About
        if type_win=="about":
            Label(self.root,text="Creador: "+properties[0],font=DEFAULT_FONT_TITLE,border=5).pack()
            Label(self.root,text="Mail: "+properties[2],font=DEFAULT_FONT_TITLE,border=5).pack()
            Label(self.root,text="Version: "+str(properties[1]),font=DEFAULT_FONT_TITLE,border=5).pack()
            Button(self.root, text="Cerrar",command=self.root.destroy).pack()
            
        #Licencia o gnu
        if type_win=="licence" or type_win=="changelog" or type_win=="ayuda":
            archivo = open(properties[1],"r")
            Yscroll = Scrollbar(self.root)
            Yscroll.pack(side=RIGHT, fill=Y)
            texto = Text(self.root,wrap=NONE,
            yscrollcommand=Yscroll.set)
            texto.focus_force()
            for i in archivo: texto.insert(INSERT,i)
            texto.pack()
            texto.configure(state="disabled")
            Yscroll.config(command=texto.yview)
            archivo.close()
        
        if type_win == 'icons':
            
            F = Frame(self.root)
            F.pack()

            FiguresInsert = Frame(F)
            FiguresInsert.pack()
        
            
            files = glob.glob('Data\icons_gui\*')
            
            i,j = 0,0          
            for icon_file in files:
            
                b_line = ttk.Button(FiguresInsert,text="Insert Icon", command=lambda:self.sendIcon(icon_file), width=20, style="TButton")
                images = Image.open(icon_file)
                images = images.resize((32,32), Image.ANTIALIAS)
                images = ImageTk.PhotoImage(file='Data\icons_gui\\test.gif')
                b_line.config(image=images)
                b_line.image = images
                b_line.grid(row=j, column=i)
                
                i = i + 1
                if(i > 4):
                    i = 0
                    j = j + 1
            
            #b_cancel = ttk.Button(FiguresInsert, text="No",command=lambda:self.sendIcon("no"),width=5)
            #b_cancel.grid(columnspan = 5, pady = 10)
            

    #Asignar un numero de vertices para dibujar
    def sendIcon(self, filepath):
        print(filepath, flush=True)
        self.value = filepath
        self.root.destroy()

    #Ingresa colores programados
    def putcolor(self,colorText):
        self.color.config(text=colorText)
        self.value = colorText
        
    #Funcion que envia una respuesta
    def response(self,respuesta):
        if respuesta=="yes": self.value = True
        if respuesta=="no": self.value = False
        self.root.destroy()
        
    #Enviar un texto
    def enviarTexto(self):
        text = self.texto.get()
        if len(text)>0:
            self.value=text
            self.root.destroy()
        
    #Enviar una figura
    def sendFigure(self,figura):
        self.value = figura
        self.root.destroy()
        
    #Enviar estilo
    def enviarEstilo(self):
        x = self.XPLUS.get()
        y = self.YPLUS.get()
        dash = self.DASH.get()
        smooth = self.SMOOTH.get()
        join = self.JOIN.get().lower()
        if x.isdigit() and x!="":
            x= int(x)
            if x>0: self.styleValues[0]=x
        if y.isdigit() and y!="":
            y=int(y)
            if y>0: self.styleValues[1]=y
        if dash.replace(",","").replace(" ","").isdigit():
            dash = dash.split(",")
            k=0
            j=0
            for i in dash:
                if not valueBetween(int(i),1,255): k+=1
                dash[j]=int(dash[j])
                j+=1
            if k==0: self.styleValues[2]=dash
        if smooth.isdigit() and smooth!="":
            smooth=int(smooth)
            if valueBetween(smooth,0,1): self.styleValues[3]=smooth
        if join=="miter" or join=="bevel" or join=="round": self.styleValues[4]=join       
        self.root.destroy()
        
    #Restaurar el estilo
    def restaurarEstilo(self):
        self.styleValues[0]=self.defaultProperties[0]
        self.styleValues[1]=self.defaultProperties[1]
        self.styleValues[2]=self.defaultProperties[2]
        self.styleValues[3]=self.defaultProperties[3]
        self.styleValues[4]=self.defaultProperties[4]
        self.root.destroy()
        
    #Ingresar weightes
    def weight(self,weightLine):
        self.value = weightLine
        self.root.destroy()
    
    #Funcion para crear un color hexadecimal
    def crearColor(self,X):
        r = self.R.get()
        g = self.V.get()
        b = self.A.get()
        if r!="" and g!="" and b!="":
            if r.isdigit() and g.isdigit() and b.isdigit():
                r = int(r)
                g = int(g)
                b = int(b)
                if valueBetween(r,0,255) and valueBetween(g,0,255) and valueBetween(b,0,255):
                    hr = hex(r).replace("0x","").zfill(2)
                    hg = hex(g).replace("0x","").zfill(2)
                    hb = hex(b).replace("0x","").zfill(2)
                    hexcolor = ("#"+hr+hg+hb).upper()
                    self.paleta.config(bg=hexcolor)
                    self.color.config(text=hexcolor)
                    self.value = hexcolor
                    self.enviarb.config(state=NORMAL)
                else:
                    self.enviarb.config(state=DISABLED)
                    self.color.config(text="ERROR, VALORES ENTRE [0,255]")
                    lib("sonido","minimo")
            else:
                self.color.config(text="ERROR, VALORES DEBEN SER DIGITOS")
                lib("sonido","minimo")
                self.enviarb.config(state=DISABLED) 
        else:
            self.enviarb.config(state=DISABLED)
            self.color.config(text="Elija un color")       
        
    #Ingresar color personalizado
    def colorPersonalizado(self):
        colorCreated = pyv("Color Personalizado","Data/Icons/palete.ico","createColor",(250,150))
        colorCreated.root.mainloop(2)
        if colorCreated.value!=0: self.putcolor(colorCreated.value)
