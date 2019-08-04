import os
import sys
from collections import deque

#I wrote makefile for cfiles but i couldn't run the make command properly. I don't know why.
#I also create the makefile

#for cfiles and their roots
cfiles = []
#for cfiles
cfiles1 = []
#for hfiles
hfiles = []
#for hfiles
hfiles1 = []
#for include statements in the .c files
includes = []
#for error checking
counterror = 0
#for addresses of the .h files in makefile
address = []
#the string which will be written to makefile
write = ""

#taking the argument
qlist = deque([sys.argv[1]])
#taking the current directory
currentdir = qlist.popleft()
for root, dirs, files in os.walk(currentdir):
    for file in files:
        if file.endswith(".c"):
            #appending to an array cfiles and roots
            cfiles.append(os.path.join(root, file))
            # appending to an array cfiles
            cfiles1.append(os.path.join(file))
            #reading the cfiles line by line
            with open(cfiles[len(cfiles) - 1]) as f:
                content = f.read().splitlines()
            for x in range(0, len(content)):
                #searching for include statements
                if content[x].startswith("#include"):
                    #splitting by spaces
                    lhs, rhs = content[x].split(' ')
                    state = rhs[1:-1]
                    if not state == "stdio.h":
                        # appending to include statements to includes array
                        includes.append(state)

        if file.endswith(".h"):
            # appending to an array cfiles
            hfiles.append(os.path.join(file))
            # appending to an array cfiles
            hfiles1.append(file)
            #splitting by '\\'
            arr = root.split("\\")
            # appending the root directory of hfiles to address
            address.append(arr[len(arr) - 1])
            #checking whether there is already that address in the array or not
            if len(address) > 1:
                if not address[len(address)-1] == address[len(address)-2]:
                    write += arr[len(arr) - 1] + "_ = " + root + "\n"
            else:
                write += arr[len(arr) - 1] + "_ = " + root + "\n"


#If there is an error, it prints the error message
for x in range(len(includes)):
    if not hfiles.__contains__(includes[x]):
        print("Error: The file", includes[x], "is not found.")
        counterror += 1
        break

#If there is a warning, it prints the warning message
for x in range(len(hfiles)):
    if not includes.__contains__(hfiles[x]):
        print("Warning: The file", hfiles[x], "is not used.")

#the exe() function creates a string which will be written in the makefile.
# This string is the .exe part
def exe():
    #cf is a string for exe part of the makefile
    cf = os.path.basename(currentdir) + ":\n\t"
    #adding cfiles.o's
    for x in range(0, len(cfiles)):
        cf += cfiles1[x][0:-2]
        cf += ".o"
        cf += " "

    cf += "\n\t"
    cf += "gcc "
    #
    for x in range(0, len(cfiles)):
        cf += cfiles1[x][0:-2]
        cf += ".o"
        cf += " "
    cf = cf + "-o " + os.path.basename(currentdir) + " lm\n\t" + "echo \"done\""
    return cf

#the obj() function creates a string which will be written in the makefile.
# This string is the .o parts
def obj():
    cfiles1 = []
    cfiles = []
    can = ""
    for root, dirs, files in os.walk(currentdir):
        for file in files:
            if file.endswith(".c"):
                cfiles.append(os.path.join(root, file))
                # cfiles1.append(os.path.join(file))
                # print(os.path.join(root, file)[2:])
                if not os.path.join(root, file).__contains__("\\"):
                    can += os.path.join(file)
                    can = can[0:-2] + ".o:\n\t"
                    can += os.path.join(file) + " "
                else:
                    can += os.path.join(file)
                    can = can[0:-2] + ".o:\n\t" + os.path.join(root, file) + " "

                with open(cfiles[len(cfiles) - 1]) as f:
                    content = f.read().splitlines()

                inc = ""
                for x in range(0, len(content)):
                    if content[x].startswith("#include"):
                        lhs, rhs = content[x].split(' ')
                        state = rhs[1:-1]
                        if not state == "stdio.h":
                            for x in range(0, len(hfiles1)):
                                if hfiles1[x].__contains__(state):
                                    can += "$(" + address[x] + "_)/" + hfiles1[x] + " "
                                    if not inc.__contains__(address[x]):
                                        inc += "$(" + address[x] + "_) "
                can = can + "\n\t" + "gcc -c -I " + inc + os.path.join(root, file)
                can += "\n"
    return can


#if there is no error, writes makefile
if counterror == 0:

    write = write + exe() + "\n" + obj()
    write = write + "clean: -rm - f *.o\n\t-rm - f " + os.path.basename(currentdir)

    #opens a file in current directory and writes makefile
    f1 = open(currentdir + '/makefile', 'w+')
    f1.write(write)
    f1.close()

#is there is an error, it says 'error'
else:

    f1 = open(currentdir + '/makefile', 'w+')
    f1.write("error")
    f1.close()

print()
print("done")
