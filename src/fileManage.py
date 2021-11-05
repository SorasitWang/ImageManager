import json
import shutil
import os

def addNewFile(catTags,nameFile,fromWaiting=False):

    with open("src/database.json",'r+') as file:

        fileData = json.load(file)

        for e in catTags:
            category , tag = e.split(",")
            category = category.strip().lower()
            tag = tag.strip().lower()
            if tag is None:
                continue
            if category not in fileData :
                fileData[category] = {}
            
            if tag not in fileData[category]:
                fileData[category][tag] = []

            if nameFile not in fileData[category][tag]:
                fileData[category][tag].append(nameFile)
            
            if nameFile in fileData["WAITING"]:
                fileData["WAITING"].pop(fileData["WAITING"].index(nameFile))
    
        file.seek(0)
        # convert back to json.
        json.dump(fileData, file, indent = 4)

def moveFile(type,name):  
    directory = ""
  
    parent_dir = ""
    
    # Path
    path = os.path.join(parent_dir, directory)

    try :
        os.mkdir(path)
    except OSError as e:
        print(e) 

    try :
        shutil.move("mouse.png", '''{type}/mouse.png''')
    except OSError as e:
        print(e)

def classifyImg(img):

    
    return 

def searchFile(category,tag=""):
    category = category.lower()
    tag = tag.lower()
    with open("src/database.json",'r') as file:
        
        fileData = json.load(file)
       
        inCat = fileData.get(category)
        if inCat is None :
            return None
        if len(tag) == 0 :
            return inCat
        if inCat.get(tag) is None:
            return None
        return {tag:inCat.get(tag)}

def searchInfo(nameImg):
    nameImg = nameImg.lower()
    with open("src/database.json",'r') as file:
        
        fileData = json.load(file)
        result = []
        for cat,data in fileData.items():
            if type(data) == list:
                if nameImg in data :
                    result.append((cat,""))
            elif type(data) == dict:
                for tag,subData in data.items():
                    if nameImg in subData:
                        result.append((cat,tag))
        

    return result



