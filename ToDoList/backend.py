import os
import json

task = []

def loadTask():
    global task
    with open("tasks.json","r") as f :
        task = json.load(f)

def saveTask():
    with open ("tasks.json","w") as f:
        json.dump(task,f,indent=4)

if os.path.exists("tasks.json"):   # check if file exists
    loadTask()
    taskId = max(t["taskId"] for  t in task) if task else 0
    total = rem = len(task)
    rem = sum(1 for t in task if not t["done"])
else:
    task = [] 
    taskId = 0      

def clearData():
           global task, taskId
           task = []
           taskId = 0
           if os.path.exists("tasks.json"):
               os.remove("tasks.json")

def getAllTask():
    return task
    
def getPenTask():
    return [ t for t in task if not t["done"]]               

def getCompTask():
    return [ t for t in task if t["done"]]
        
def searchTask(keyword):
            return [ t for t in task if keyword.lower() in t["title"].lower()]

def addTask(tsk):
    global taskId
    taskId += 1
    task.append({"taskId":taskId,
                 "title":tsk,
                 "done":False,
   })
    saveTask()

def addAt(tskno,tsk):
    global taskId
    taskId += 1
    task.insert(tskno-1,{"taskId":taskId,
                         "title":tsk,
                         "done":False
                         })
    saveTask()

def replaceTask(tid,tsk):
    for t in task:
        if t["taskId"] == tid:
           t["title"] = tsk
           break
    saveTask()   

def deleteTask(tid):
    for t in task:
        if t["taskId"] == tid:
            task.remove(t)
            break    
    saveTask()

def doneTask(tid):
    for t in task:
        if t["taskId"] == tid:
          if  not t["done"]:
            t["done"] = True
    saveTask()

def undoneTask(tid):
    for t in task:
        if t["taskId"] == tid:
            t["done"] = False
            break
    saveTask()       

def doneAll():
    for t in task:
        if  not t["done"]:
           t["done"] = True
    saveTask()
        
def progress():
    total = len(task)
    if total == 0 :
        return (0,0)
    rem = sum (1  for t in task if not t["done"])
    return (total,rem)


