DEBUGGING = False
extrastufffordebuggingnotthatnagging = False
try:
    import sys,tty,termios
except:
    print("sorry u gotta use linux or wsl or mac for this")
    exit(1)

import json
global todolist
global maxchoice
todofilename = "todo.json"

# todolist = {
#         "tungtung": False,
#         "sigmaboy": True,
#         "im not sure": True,
#         "testingg": False,
#         "buy groceries": True
# }


# load todolist
try:
    open(todofilename)
    print("todo exists")
    with open(todofilename) as jsonn:
        todolist = json.load(jsonn)
except:
    print("todo doesnt exist... creating")
    with open(todofilename, "a") as smth:
        smth.write("{}")




selectedone = 1
maxchoice = len(todolist)
addchoice = maxchoice  + 1
wipechoice = maxchoice  + 2
firstbutton = addchoice # CHANGE THIS WHEN U ADD A NEW BUTTON
frlastchoice = wipechoice # CHANGE THIS WHEN U ADD A NEW BUTTON
onaddchoice = False
onwipechoice = False
on_a_button = onaddchoice or onwipechoice # CHANGE THIS WHEN U ADD A NEW BUTTON

def updatevars(todolist):
    global selectedone, maxchoice, addchoice, wipechoice, firstbutton, frlastchoice, onaddchoice, onwipechoice, on_a_button
    maxchoice = len(todolist)
    addchoice = maxchoice + 1
    wipechoice = maxchoice + 2
    firstbutton = addchoice
    frlastchoice = wipechoice
    onaddchoice = False
    onwipechoice = False
    on_a_button = False
    selectedone = maxchoice  # land cursor on the new task


def yabadadoo(key):
    # update stuff
    global selectedone, maxchoice, addchoice, onaddchoice, onwipechoice, wipechoice, selectedkey
    # selectedone = 1
    maxchoice = len(todolist)
    addchoice = maxchoice  + 1
    wipechoice = maxchoice + 2
    onaddchoice = False
    onwipechoice = False
    if selectedone == firstbutton:
        on_a_button = True
    keys = list(todolist.keys())
    # sorry for being messy
    if int(selectedone) == int(addchoice):
        onaddchoice = True
    elif int(selectedone) == int(wipechoice):
        onwipechoice = True
        onaddchoice = False
    else:
        on_a_button = False
        selectedkey = keys[selectedone - 1] # this function is worse than
    if key == "up arrow" and selectedone != 1:
        if onaddchoice == True:
            onaddchoice = False
        elif onwipechoice == True:
            onwipechoice = False
        selectedone -= 1
    elif key == "down arrow" and selectedone != frlastchoice:
        if selectedone == wipechoice:
            onwipechoice = False
        selectedone += 1
    elif key == "space": # for any other task
        if selectedone != wipechoice and selectedone != addchoice:
            todolist[selectedkey] = not todolist[selectedkey]

        if selectedone == addchoice:
            if not DEBUGGING == True:
                print("\033c\033[3J", end='') 
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
            sigmaboy = input("Add task: ")
            todolist[sigmaboy] = False
            tty.setraw(sys.stdin.fileno())  
            # check all this bs
        
            updatevars(todolist)

        if selectedone == wipechoice:
            if not DEBUGGING == True:
                print("\033c\033[3J", end='')
            print("\r", end="")
            print("Removing done tasks...")
            toberemoved = []
            # make a list of all the stuff thats gonna get removed
            for i in todolist:
                if DEBUGGING == True: 
                    print("\r", end="")
                    print("checking ", i)
                if todolist[i] == True:
                    toberemoved.append(i)
            print("\r", end="")
            # inflate wakatime hours by adding PURE bs
            word = "these"
            if len(toberemoved) == 1:
                word = "this one"
            
            # ask the user if its OK to remove allat and also list it
            print("\r", end="")
            print("Are you sure you want to remove", word+ "?")
            for i in toberemoved:
                print("\r", end="")
                print(i)
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
            print("\r", end="")
            sigmaboy = input("Okay to remove? (y/N): ")
            
            ok_to_remove = None
            # more useless bs no one is gonna use

            if sigmaboy == "yes" or sigmaboy == "y" or sigmaboy == "yh" or sigmaboy == "yeah" and ok_to_remove == None:
                ok_to_remove = True
            elif sigmaboy == "no" or sigmaboy == "n" or sigmaboy == "nah" and ok_to_remove:
                ok_to_remove = False
            # check for edge cases
            elif sigmaboy == "" or not sigmaboy:
                ok_to_remove = False

            tty.setraw(sys.stdin.fileno())  
            # slime that boy out
            if ok_to_remove == True:
                for i in toberemoved:
                    todolist.pop(i)

            # update vars
            updatevars(todolist)
            

    
    if selectedone == addchoice:
        on_a_button = True
        onaddchoice = True
    elif selectedone == wipechoice:
        on_a_button = True
        onwipechoice = True
    
    renderthing(selectedone)




def renderthing(selectedchoice):
    # clear the console so its prettier
    if not DEBUGGING == True:
        print("\033c\033[3J", end='')
    
    global name
    global addchoice
    global on_a_button, onaddchoice, onwipechoice
    on_a_button = False
    onaddchoice = False   # reset both here
    onwipechoice = False  # reset both here

    # i imagine it like
    # [ ] tungtung
    # [X] sigmaboy
    if int(selectedone)  == int(wipechoice):
        if DEBUGGING: print("called")
        onwipechoice = True
    elif int(selectedone) == int(addchoice):
        onaddchoice = True

    keys = list(todolist.keys())
    if onaddchoice == True or onwipechoice == True:
        selectedkey = ""
    else:
        if DEBUGGING: print("called the fuckass thing at 110")
        if DEBUGGING: print("on_buton = ", on_a_button)
        if DEBUGGING: print("selected one: ", selectedone)

        selectedkey = keys[selectedone - 1]

    for i in todolist:
        
        # add the [X] thing
        cross = ""
        if todolist[i] == True:
            cross = "[X]"
        else:
            cross = "[ ]"
        
        # add the bolding
        # from https://github.com/bobbyhadz/how-to-print-bold-text-in-python/blob/main/main.py
        name = i
        selectedchoice = int(selectedchoice)
        if selectedkey == name:
            name = '\033[1m' + name + '\033[0m' + " <"

        

        print("\r", end="")
        print(cross, name)

    # add a new task
    text = "+ Add a new task"
    print("\r", end="")
    if onaddchoice:
        print('\033[1m' + text + '\033[0m'  + " <")  # bold that
    else:
        print(text)

    # add the wipe thing
    text = "> Remove all done tasks"
    print("\r", end="")
    if onwipechoice:
        print('\033[1m' + text + '\033[0m'  + " <")  # bold that
    else:
        print(text)

    if DEBUGGING == True or extrastufffordebuggingnotthatnagging == True:
        print("\r", end="")
        print("on_a_button = ", on_a_button)
        print("\r", end="")
        print("onwipechoice= ", onwipechoice)
        print("\r", end="")
        print("onaddchoice= ", onaddchoice)
        print("\r", end="")
        print("selectedone= ", selectedone)
        print("\r", end="")
        print("selectedchoice= ", selectedchoice)
        print("\r", end="")
        print("wipechoice= ", wipechoice)
        print("\r", end="")
        print("firstbutton= ", firstbutton)
        print("\r", end="")
        print("maxchoice= ", maxchoice)
        print("\r", end="")
        print("frlastchoice= ", frlastchoice)
        




# really complicated thing i copied from stackoverflow V
###############
# Source - https://stackoverflow.com/a/69065464
# Posted by MRule
# Retrieved 2026-03-13, License - CC BY-SA 4.0

# Commands and escape codes
END_OF_TEXT = chr(3)  # CTRL+C (prints nothing)
END_OF_FILE = chr(4)  # CTRL+D (prints nothing)
CANCEL      = chr(24) # CTRL+X
ESCAPE      = chr(27) # Escape
CONTROL     = ESCAPE +'['

# Escape sequences for terminal keyboard navigation
ARROW_UP    = CONTROL+'A'
ARROW_DOWN  = CONTROL+'B'
ARROW_RIGHT = CONTROL+'C'
ARROW_LEFT  = CONTROL+'D'

# Escape sequences to match
commands = {
    ARROW_UP   :'up arrow',
    ARROW_DOWN :'down arrow',
    ARROW_RIGHT:'right arrow',
    ARROW_LEFT :'left arrow',
}

# Blocking read of one input character, detecting appropriate interrupts
def getch():
    k = sys.stdin.read(1)[0]
    if k in {END_OF_TEXT, END_OF_FILE, CANCEL}: raise KeyboardInterrupt
    return k

# Println for raw terminal mode
def println(*args):
    print(*args,end='\r\n',flush=True)

renderthing(0)

# Preserve current terminal settings (we will restore these before exiting)
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

try:
    # Enter raw mode (key events sent directly as characters)
    tty.setraw(sys.stdin.fileno())

    # Loop, waiting for keyboard input
    while 1:
        # Parse known command escape sequences
        read = getch()
        while any(k.startswith(read) for k in commands.keys()): 
            if read in commands:
                if commands[read] == " ":
                    commands[read] = "space"
                # println(commands[read])
                yabadadoo(str(commands[read]))
                read = ''
                break
            read += getch()
        # Interpret all other inputs as text input
        for c in read:
            if c == " ":
                c = "space"
            # println(c)
            yabadadoo(c)

# if its a ctrl c then just say bye
except KeyboardInterrupt:
    # clear the console so its prettier
    if not DEBUGGING == True:
        print("\033c\033[3J", end='')

except Exception as e:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
    import traceback
    print("info:")
    if DEBUGGING == True:
        print("\r", end="")
        print("on_a_button = ", on_a_button)
        print("\r", end="")
        print("onwipechoice= ", onwipechoice)
        print("\r", end="")
        print("onaddchoice= ", onaddchoice)
        print("\r", end="")
        print("selectedone= ", selectedone)
        print("\r", end="")
        print("wipechoice= ", wipechoice)
        print("\r", end="")
        print("firstbutton= ", firstbutton)
    print("\nCrash:")
    traceback.print_exc()
    sys.exit(1)


# Always clean up
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
    with open(todofilename, "w") as f:
        prettydump = json.dumps(todolist,sort_keys=True,indent=2)
        f.write(prettydump)
    sys.exit(0)
