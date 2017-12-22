#File to create windows
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

#Icons window
class iconWin:
    
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

#Clase create windows
class popWin:
    
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
    
        #Menu insert text
        if type_win=="inserttext":
            Label(self.root,text="Insert Text",font=DEFAULT_FONT_TITLE,border=10).pack()
            self.texto = Entry(self.root)
            self.texto.pack()
            Label(self.root,text=" ").pack()
            Button(self.root, text="Write",command=self.sendText,width=10,relief=GROOVE).pack()
            self.texto.focus_force()
            
        #Menu savefile
        if type_win=="savefile":
            Label(self.root,text="Choose name",font=DEFAULT_FONT_TITLE,border=10).pack()
            self.texto = Entry(self.root)
            self.texto.pack()
            Label(self.root,text=" ").pack()
            Button(self.root, text="Save",command=self.sendText,width=10,relief=GROOVE).pack()
            self.texto.focus_force()
            
        #Menu save
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
            Label(self.root,text="Creators"+properties[0],font=DEFAULT_FONT_TITLE,border=5).pack()
            Label(self.root,text="Version: "+str(properties[1]),font=DEFAULT_FONT_TITLE,border=5).pack()
            Button(self.root, text="Close",command=self.root.destroy).pack()

        #License
        if type_win=="license" or type_win=="changelog" or type_win=="help":
            archive = open(properties[1],"r")
            Yscroll = Scrollbar(self.root)
            Yscroll.pack(side=RIGHT, fill=Y)
            text = Text(self.root,wrap=NONE,
            yscrollcommand=Yscroll.set)
            text.focus_force()
            for i in archive: text.insert(INSERT,i)
            text.pack()
            text.configure(state="disabled")
            Yscroll.config(command=text.yview)
            archive.close()
        
    #Sends response to gui
    def response(self,resp):
        if resp=="yes": self.value = True
        if resp=="no": self.value = False
        self.root.destroy()
 
    #Enviar un texto
    def sendText(self):
        text = self.texto.get()
        if len(text)>0:
            self.value=text
            self.root.destroy()
    
    #Send weightes
    def weight(self,weightLine):
        self.value = weightLine
        self.root.destroy()
     
