import os
import platform

projectName = input("enter project name: ")
os.mkdir("./" + projectName)
os.chdir("./" + projectName)
os.mkdir("./images")
os.mkdir("./php")
os.mkdir("./resources")
if platform.system() == "Windows":
    os.popen('copy index.html php\index.php')
    os.popen('copy ..\image.jpg images\image.jpg')
else:
    os.popen('cp index.html php/index.php')
    os.popen('cp ../image.jpg images/image.jpg')

index = open("index.html", "w+")
index.write("""<!DOCTYPE html>
<html>
<head>
<title>%s</title>
</head>
<body>
    <h1> Welcome to %s website </h1>
    <img src="images/image.jpg" >
</body>
</html>""" % (projectName,projectName))
files =os.listdir()
os.chdir("./php")
print(os.listdir())

print("These files and directories have been created for you: ")
print(files)
