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
        self.frame = Frame(root,height=130,width =100,highlightbackground="black",highlightthickness=1)
        self.nameImg = nameImg
        self.frame.pack(side = "left")
        self.img = ImageTk.PhotoImage(Image.open(nameImg).resize((100,100), Image.ANTIALIAS))
        self.ui = ui
        self.panel = Label(self.frame,image = self.img)
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


class imgRow:
    def __init__(self,ui,root,cat,tag,imgs):
        self.imgLists = []
        self.idx = 0
        self.frame = Frame(root,height=200,width = 480,highlightbackground="gray",highlightthickness=2)
        self.frame1 = Frame(self.frame,height=150,width = 480,highlightbackground="gray",highlightthickness=2)
        
        h=Scale(self.frame, orient='horizontal')
        h.pack(side=BOTTOM, fill='x')
        self.label = Text(self.frame,height=25,width =100)
        self.label.insert(INSERT,cat+":"+tag)
        self.frame1.pack(side="bottom")
        self.frame.pack(padx = 5, pady = 5)
        self.frame.pack_propagate(False)
        for img in imgs:
           self.imgLists.append(imgBox(ui,self.frame1,img))
        self.label.pack(side="top")

        def nextImg(i):
            i = int(i)
            for e in self.imgLists:
                e.show(False)
            for j in range(max(0,i-4),min(i,len(self.imgLists)),1):
                self.imgLists[j].show(True)
           

        h.config(command=nextImg, from_=min(4,len(self.imgLists)), to=len(self.imgLists))

    def show(self,t):
        if t :
            self.frame.pack(padx = 5, pady = 5)
        else :
            self.frame.pack_forget()

    def unpack(self):
        self.frame.destroy()


class imgBlog:
    def __init__(self,ui,root,cat,tags,imgs):
        self.frame = Frame(root,bg="yellow")
        self.frame.pack(padx = 5, pady = 8)
        self.frameL = Frame(self.frame,highlightbackground="black",highlightthickness=2)
        self.frameL.pack(side=LEFT)
        self.imgRows = []
        h=Scale(self.frame, orient='vertical')
        h.pack(side=RIGHT,fill="y")
        for tag in tags :
            self.imgRows.append(imgRow(ui,self.frameL,cat,tag,imgs.get(tag)))
        
        
        
        def nextRow(i):
            i = int(i)
            print(i)
            for e in self.imgRows:
                e.show(False)
            for j in range(max(0,i-2),min(i,len(self.imgRows)),1):
                self.imgRows[j].show(True)
        h.config(command=nextRow, from_=min(2,len(self.imgRows)), to=len(self.imgRows))

        if len(self.imgRows) <= 2:
            h.pack_forget()
        
        
    def unpack(self):
        self.frame.destroy()
       


class ui :
    def __init__(self):
        self.size = (720,660)
        self.imgBlogs = []
        self.root = Tk()
        self.root.geometry(str(self.size[0])+"x"+str(self.size[1]))

        self.fileView = Frame(self.root,height=self.size[1],width = 0.75*self.size[0],highlightbackground="black",highlightthickness=1)
        self.fileView.pack(side=LEFT)
        self.fileView.pack_propagate(False)

        self.searchView = Frame(self.root,height=self.size[1],width = 0.25*self.size[0],highlightbackground="black",highlightthickness=1)
        self.searchView.pack(side=RIGHT)
        self.searchView.pack_propagate(False)

        
        self.waitingView = Frame(self.fileView,height=self.size[0],width = 0.25*self.size[1],highlightbackground="black",highlightthickness=1)
        self.waitingView.pack(side="bottom")
        result = searchFile("WAITING")
        self.row = imgRow(ui,self.waitingView,"Waiting","",result)
        self.setupSearchView()
        self.setupWaitingView()
        self.root.mainloop()

    def setupSearchView(self):
        def sendInput():
            catValue=catBox.get("1.0","end-1c").strip()
            tagValue=tagBox.get("1.0","end-1c").strip()
            result = searchFile(catValue,tagValue)
            print(result)
            for blog in self.imgBlogs :
                blog.unpack()
            if result is None :
                return
            self.imgBlogs = []
            if len(catValue) == 0:
                return
            if len(tagValue) == 0 :
                self.imgBlogs.append(imgBlog(self,self.fileView,catValue,result.keys(),result))
            else :
                self.imgBlogs.append(imgBlog(self,self.fileView,catValue,[tagValue],result))

        self.searchBox = Frame(self.searchView,height=100,width = 0.33*self.size[1],highlightbackground="black",highlightthickness=1)
        self.searchBox.pack()
        self.searchBox.pack_propagate(False)
        catLabel = Label(self.searchBox,text="Category : ")
        catLabel.grid(row=1,column=1)
        catBox=Text(self.searchBox, height=2, width=10)
        catBox.grid(row=1,column=2)

        tagLabel = Label(self.searchBox,text="Tag : ")
        tagLabel.grid(row=2,column=1)
        tagBox = Text(self.searchBox, height=2, width=10)
        tagBox.grid(row=2,column=2)
        buttonCommit=Button(self.searchBox, height=1, width=10, text="Commit", 
                            command=lambda: sendInput())
        #command=lambda: retrieve_input() >>> just means do this when i press the button
        buttonCommit.grid(row=3,column=2)


        def updateTag():
            value = self.infoBox.get("1.0","end-1c").strip().split("\n")
            addNewFile(value,selectImg["name"])
            self.setupWaitingView()
        self.updateBtn = Button(self.searchView, height=1, width=10, text="Update", 
                            command=lambda: updateTag())
        self.infoBox = Text(self.searchView, height=5, width=10)
        self.panel = Label(self.searchView)
        self.namePreview = Label(self.searchView)
        self.buffer = None
        self.refreshSystem()

        
    def setupWaitingView(self):
        result = searchFile("WAITING")
        self.row.unpack()
        self.row = imgRow(ui,self.waitingView,"Waiting","",result)

        
        
        

       
    def refreshSystem(self):
        global selectImg
        if selectImg["img"] != None and selectImg["img"] != self.buffer:

            
            self.infoBox.pack_forget()
            self.updateBtn.pack_forget()
            
            self.namePreview.config(text=selectImg["name"])
            self.namePreview.pack()
            self.panel.config(image=selectImg["img"])
            self.panel.pack(side="top")
            self.buffer = selectImg["img"]

            catTag = searchInfo(selectImg["name"])
            for i in range(len(catTag)):
                if len(catTag[i][1]) == 0:
                    catTag = []
                    break
                catTag[i] =catTag[i][0] + ":" +catTag[i][1]
            txt = "\n".join(catTag)

            self.infoBox.delete(1.0,"end")    
            self.infoBox.insert(1.0,txt)
            self.infoBox.pack()
            self.updateBtn.pack()
        
        self.root.after(1000, self.refreshSystem)

   
    


u = ui()
