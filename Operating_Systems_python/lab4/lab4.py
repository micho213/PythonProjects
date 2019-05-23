import platform
import os
if platform.system() == "Windows":
    print("I see that you are running this python file on Windows")
    print("Now we will execute .bat, a windows specific file, instead of .sh, for linux")

    # this program prints, that it is running, then prints the current directory listing
    os.system("windowsScript.bat")

elif platform.system() == "Linux":
    print("I see that you are running this python file on linux")
    print("Now we will execute .sh, a Linux specific file, instead of .bat, for Windows")

    # this program prints, that it is running, then prints the current directory listing
    os.system("bash linuxScript.sh")




























# import os
# import sys
#
# pid = os.fork()
# if pid == 0: # the child
#     print ("this is the child")
# elif pid > 0:
#     print ("the child is pid %d"% (pid))
# else:
#     print("An error occured")
#
#
# pid = os.fork()
# # fork and exec together
# print ("second test")
# if pid == 0: # This is the child
#      print ("this is the child")
#      print ("I'm going to exec another program now")
#      os.execv(sys.executable, [sys.executable])
# else:
#      print ("the child is pid %d" % (pid))
#      os.wait()
#
