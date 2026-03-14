
import sys,tty,termios
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
onaddchoice = False

def yabadadoo(key):
    global selectedone, maxchoice, addchoice, onaddchoice
    keys = list(todolist.keys())
    # sorry for being messy
    if int(selectedone)  == int(addchoice):
        onaddchoice = True
    else:
        onaddchoice = False
        selectedkey = keys[selectedone - 1]
    if key == "up arrow" and selectedone != 1:
        onaddchoice = False
        selectedone -= 1
    elif key == "down arrow" and selectedone != addchoice:
        selectedone += 1
    elif key == "space" and selectedone != addchoice: # for any other task
        todolist[selectedkey] = not todolist[selectedkey]
    elif key == "space" and selectedone == addchoice:
        # clear the console so its prettier
        print("\033c\033[3J", end='')
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
        sigmaboy = input("Add task: ")
        todolist[sigmaboy] = False
        tty.setraw(sys.stdin.fileno())
        # check all this bs
        
        selectedone = 1
        maxchoice = len(todolist)
        addchoice = maxchoice  + 1
        onaddchoice = False

    
    renderthing(selectedone)




def renderthing(selectedchoice):
    # clear the console so its prettier
    print("\033c\033[3J", end='')
    global name
    global addchoice
    global onaddchoice
    # i imagine it like
    # [ ] tungtung
    # [X] sigmaboy
    if int(selectedone)  == int(addchoice):
        onaddchoice = True
    keys = list(todolist.keys())
    if selectedone == addchoice:
        selectedkey = "SIGMAA"
    else:
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
            name = '\033[1m' + name + '\033[0m'

        

        print("\r", end="")
        print(cross, name)

    # add choice
    text = "+ Add a new task"
    print("\r", end="")
    if onaddchoice:
        print('\033[1m' + text + '\033[0m') # bold that
    else:
        print(text)




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
    print("\033c\033[3J", end='')

except Exception as e:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
    import traceback
    print("\nCrash:", flush=True)
    traceback.print_exc()
    sys.exit(1)


# Always clean up
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
    with open(todofilename, "w") as f:
        prettydump = json.dumps(todolist,sort_keys=True,indent=2)
        f.write(prettydump)
    sys.exit(0)
