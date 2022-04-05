# import urllib library
from urllib.request import urlopen
import requests
from PIL import Image
import os
import pathlib
import random
import json
import csv
import wget

path=pathlib.Path(__file__).parent.resolve()
os.chdir(path)
os.mkdir('images')

url = "https://products.devscope.net/profiles/employees.json"

response = urlopen(url)

data_json = json.loads(response.read())
  
for x in data_json:
    url = x['Photo365']
    name = x['Alias'] 
    response = requests.get(url)
    grid = Image.new('RGB',(240,240),(255, 0, 0))
    grid.save("images/"+name+".png")
    file = open("images/"+name+".png", "wb")
    file.write(response.content)
    file.close()

def grid_pos_random(cols,rows):
    rand_cols=random.randrange(0,cols)
    rand_rows=random.randrange(0,rows)
    return rand_cols,rand_rows
    
def grid_depart():
    arr = os.listdir('./images')
    depart=[]
    for name in arr:
        try:
            img = Image.open("images/"+name)
        except:
            continue
        img = img.convert('L')
        if (((img.size[0])*(img.size[1]))!=57600):
            img=img.resize((240,240))
        depart.append(img)
    return depart

depart = grid_depart()    

cols=9
rows=5
#w=int(1920/cols)
#h=int(1080/rows)
w=240
h=240

grid = Image.new('RGBA', (cols*w, rows*h),(255, 0, 0,0))

canvas_list = []
i=0
cordslist=[]
for img in depart:
    if i<45:
        while True:
            cords = grid_pos_random(cols,rows)
            if cords in cordslist:
                continue
            else:
                cordslist.append(cords)
                random_col,random_row=cords
                break
    else:
        random_col,random_row = grid_pos_random(cols,rows)
    canvas = Image.new('RGBA', (cols*w, rows*h),(255, 255, 255,0))
    canvas.paste(img, box=(random_col*w,random_row*h))
    canvas_list.append(canvas)
    i+=1

grid.save("img/out.gif", transparency=0,save_all=True, append_images=canvas_list, duration=100, loop=0)

def delete():
    arr = os.listdir('./images')
    for name in arr:
        os.remove("images/"+name)

delete()
os.rmdir('images')

try:
    os.remove("./csv/trainings.csv")
except:
    pass
 
url = "https://products.devscope.net/profiles/trainings.csv"
wget.download(url, './csv/trainings.csv')

file = open('./csv/trainings.csv')
csvreader = csv.reader(file)

cert = []
exa = []



for x in csvreader:
    if "devscope" in x[6] or x[7] :
        if x[3] == "Certification":
            cert.append(x)
        elif x[3] == "Exam":
            exa.append(x)





url = "https://products.devscope.net/profiles/employees.json"

response = urlopen(url)

data_json = json.loads(response.read())

jsonfinal = []

for func in data_json:
    certeficados = []
    exames = []
    ass = 0
    fun = 0
    exp = 0
    
    photos = {"Photo96" : func["Photo96"],
              "PhotoWhite" : func["PhotoWhite"],
              "PhotoAD" : func["PhotoAD"],
              "Photo365" : func["Photo365"]}
    
    for cer in  cert:
        if cer[7] == func["CompanyEmail"]:
            lixo = {}
            lixo["Name"] = cer[2]
            lixo["Data"] = cer[8]
            certeficados.append(lixo)
            if "Associate" in cer[2]:
                ass +=1
            elif "Fundamentals" in cer[2]:
                fun +=1
            elif "Expert" in cer[2]:
                exp +=1 
            
    for ex in  exa:
        if ex[7] == func["CompanyEmail"]:
            lixo = {}
            lixo["Name"] = cer[2]
            lixo["Data"] = cer[8]
            exames.append(lixo)
            
    
    Person = {"CompanyEmail" : func["CompanyEmail"],
           "Title" : func["Title"],
           "Job" : func["Job"],
           "Department" : func["Department"],
           "Superior" : func["Superior"],
           "Alias" : func["Alias"],
           "Photos_Links" : photos,
           "Certifications": certeficados,
           "Associate" : ass,
           "Fundamentals" : fun,
           "Expert" : exp,
           "Exams" : exames,
    }

    jsonfinal.append(Person)
    
with open('./json/Person.json', 'w') as fp:
    json.dump(jsonfinal, fp)

