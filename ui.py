from os import name
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from fileManage import addNewFile, searchFile , searchInfo

'''data: list / dict 
   [cat1,cat2,...] / {"cat1" : [tag1,tag2,...] , "cat1" : [tag1,tag2,...]}
'''
selectImg = {"img":None,"name":None}


class imgBox:
      
    def __init__(self,ui,root,nameImg):
        self.frame = Frame(root,height=130,width =100,bg="red",borderwidth=5)
        self.nameImg = nameImg
        self.frame.pack(side = "left")
        self.img = ImageTk.PhotoImage(Image.open(nameImg).resize((100,100), Image.ANTIALIAS))
        self.ui = ui
        self.panel = Label(self.frame,text="555555", image = self.img)
        self.panel.pack(side="top")
            
        self.panel.bind("<Button>",lambda event : self.onClick(event))
   
    def onClick(self,event):
        global selectImg
        selectImg["img"] = self.img
        selectImg["name"] = self.nameImg
    def show(self,t):
        if t :
            self.frame.pack(side = "left")
        else :
            self.frame.pack_forget()
        '''
        self.label = Text(self.frame,height=25,width =100)
        self.label.insert(INSERT,nameImg)
        self.label.pack(side="bottom")
        '''

class imgRow:
    def __init__(self,ui,root,tag,imgs):
        self.imgLists = []
        self.idx = 0
        self.frame = Frame(root,height=150,width = 550,bg="blue",borderwidth=5)
        h=Scale(self.frame, orient='horizontal')
        h.pack(side=BOTTOM, fill='x')
        self.frame.pack(padx = 5, pady = 5)
        self.frame.pack_propagate(False)
        for img in imgs:
            self.imgLists.append(imgBox(ui,self.frame,img))

        def nextImg(i):
            i = int(i)
            for e in self.imgLists:
                e.show(False)
            for j in range(max(0,i-4),min(i,len(self.imgLists)),1):
                self.imgLists[j].show(True)
           

        h.config(command=nextImg, from_=min(4,len(self.imgLists)), to=len(self.imgLists))

    def unpack(self):
        self.frame.destroy()


class imgBlog:
    def __init__(self,ui,root,cat,tags,imgs):
        self.frame = Frame(root,bg="yellow")
        self.frame.pack(padx = 5, pady = 8)
        self.imgRows = []
        for tag in tags :
            self.imgRows.append(imgRow(ui,self.frame,tag,imgs.get(tag)))
    def unpack(self):
        self.frame.destroy()
       


class ui :
    def __init__(self):
        self.size = (720,720)
        self.imgBlogs = []
        self.root = Tk()
        self.root.geometry(str(self.size[0])+"x"+str(self.size[1]))

        self.fileView = Frame(self.root,height=self.size[1],width = 0.67*self.size[0],bg="red",borderwidth=5)
        self.fileView.pack(side=LEFT)
        self.fileView.pack_propagate(False)

        self.searchView = Frame(self.root,height=self.size[1],width = 0.33*self.size[0],bg="green",borderwidth=5)
        self.searchView.pack(side=RIGHT)
        self.searchView.pack_propagate(False)

        
        self.waitingView = Frame(self.fileView,height=self.size[0],width = 0.33*self.size[1],bg="green",borderwidth=5)
        self.waitingView.pack(side="bottom")
        result = searchFile("WAITING")
        self.row = imgRow(ui,self.waitingView,"Waiting",result)
        self.setupSearchView()
        self.setupWaitingView()
        self.root.mainloop()

    def setupSearchView(self):
        def sendInput():
            catValue=catBox.get("1.0","end-1c").strip()
            tagValue=tagBox.get("1.0","end-1c").strip()
            result = searchFile(catValue,tagValue)
            for blog in self.imgBlogs :
                blog.unpack()
            self.imgBlogs = []
            if len(catValue) == 0:
                return
            if len(tagValue) == 0 :
                self.imgBlogs.append(imgBlog(self,self.fileView,catValue,result.keys(),result))
            else :
                self.imgBlogs.append(imgBlog(self,self.fileView,catValue,[tagValue],result))

        self.searchBox = Frame(self.searchView,height=100,width = 0.33*self.size[1],bg="blue",borderwidth=5)
        self.searchBox.pack()
        self.searchBox.pack_propagate(False)
        catBox=Text(self.searchBox, height=2, width=10)
        catBox.pack()

        tagBox = Text(self.searchBox, height=2, width=10)
        tagBox.pack()
        buttonCommit=Button(self.searchBox, height=1, width=10, text="Commit", 
                            command=lambda: sendInput())
        #command=lambda: retrieve_input() >>> just means do this when i press the button
        buttonCommit.pack()


        def updateTag():
            value = self.infoBox.get("1.0","end-1c").strip().split("\n")
            addNewFile(value,selectImg["name"])
            self.setupWaitingView()
        self.updateBtn = Button(self.searchView, height=1, width=10, text="Update", 
                            command=lambda: updateTag())
        self.infoBox = Text(self.searchView, height=5, width=10)
        self.panel = Label(self.searchView)
        self.buffer = None
        self.refreshSystem()

        
    def setupWaitingView(self):
        result = searchFile("WAITING")
        self.row.unpack()
        self.row = imgRow(ui,self.waitingView,"Waiting",result)
        print(result)
        
        
        

       
    def refreshSystem(self):
        global selectImg
        if selectImg["img"] != None and selectImg["img"] != self.buffer:

            self.panel.pack_forget()
            self.infoBox.pack_forget()
            self.updateBtn.pack_forget()
            self.panel = Label(self.searchView,image = selectImg["img"])
            self.panel.pack(side="top")
            self.buffer = selectImg["img"]

            catTag = searchInfo(selectImg["name"])
            for i in range(len(catTag)):
                if len(catTag[i][1]) == 0:
                    catTag = []
                    break
                catTag[i] =catTag[i][0] + "," +catTag[i][1]
            txt = "\n".join(catTag)

            self.infoBox.delete(1.0,"end")    
            self.infoBox.insert(1.0,txt)
            self.infoBox.pack()
            self.updateBtn.pack()
        
        self.root.after(1000, self.refreshSystem)

   
    


u = ui()
#print(u)


y= {'ANI': {'cat': ['cat.png', 'cat1.jpg'], 'dog': ['dog.png', 'dogg.jpg']}, 'color': {'red': ['tomato.png'], 'orange': []}}
print("ANI" in y)