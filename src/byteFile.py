import pickle
import base64
import string
import sys

def write(fileName, dictionary):
    f=open(fileName, "wb")
    pickle.dump(dictionary, f)
    f.close

def read(fileName):
    f = open(fileName, 'rb')
    d = pickle.load(f)
    f.close
    return d


def based64(image):
    with open(image, "rb") as imageFile:
        b64String = str(base64.b64encode(imageFile.read()))
        imageFile.close()
        #print(b64String[2:-1])
        #print(str[2:-1])
        return b64String[2:-1]
        


icons = ['folder.png', 'saveIcon.svg', 'trimIcon.svg', 'logo.png', 'icon.png', 'null.png', 
'undo.png', 'redo.png', 'help.png', 'info.png', 'desc.png', 'sort.png']
dict = {}

for item in icons:
    dict[item] = str(based64(item))

write('res.dat', dict)