import ezdxf
import sys
import os
from os.path import exists
import time
import re

allowOverwrite = False
uncheckedOverwritePerms = True

def fixFile(file):
    global allowOverwrite
    global uncheckedOverwritePerms
    
    try:
        doc = ezdxf.readfile(file)
    except IOError:
        print(f"Not a DXF file or a generic I/O error.\n\nYou're not too smart, are you?\n")
        return(2)
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file.")
        for x in range(1000):
            print('Nightmare')
            return(3)


    msp = doc.modelspace()
    tic = time.perf_counter()
    for e in msp:
        #print("Original " + str(e.dxf.color))
        if e.dxf.color == 5:
            e.rgb = (255,0,0)
            e.dxf.color = 1
            #print(str(e.rgb) + str(e.dxf.color))
            e.rotate_z(1.5708)
        else:
            e.dxf.color = 5
            e.rgb = (0,0,255)
            #print(e.rgb)
            e.rotate_z(1.5708)

    toc = time.perf_counter()

    if file[0] == ".":
        fixedString = file[1:]
    else:
        fixedString = file

    #newName = os.path.join("./complete/", fixedString)
    #([\\|/][a-z]{1,}\.{1}dxf)
    #os.mkdir(path)
    newName = ".\complete\\" + fixedString
    newName = newName.replace("\\\\", "\\")
    makeDir = re.sub(r'([\\|/][0-9\-a-zA-Z]{1,}\.{1}dxf)',r'',newName)

    try:
        os.mkdir(makeDir)
    except FileExistsError:
        pass

    if uncheckedOverwritePerms == True:
        print("Would you like me to overwrite any existing files?")
        allow = input("y/n > ")
        if allow.lower() in ("yes", "y"):
            allowOverwrite = True
            uncheckedOverwritePerms = False
        else:
            allowOverwrite = False
            uncheckedOverwritePerms = False
    else:
        pass

    #print(allowOverwrite)
    #print(os.path.exists(newName))
    if allowOverwrite == True:
        doc.saveas(newName)
        print(f"Done! Converted file in {toc - tic:0.4f} seconds")
    elif os.path.exists(newName) == False:
        doc.saveas(newName)
        print(f"Done! Converted file in {toc - tic:0.4f} seconds")
    else:
        print("File unsaved as it already exists.")
        return(0)


    return(1)


path = sys.argv[1]
if os.path.isdir(path) == True:
    for filename in os.listdir(path):
        print(filename)
        fixFile(path + filename)
else:
    fixFile(path)
