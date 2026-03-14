# Source - https://stackoverflow.com/a/69065464
# Posted by MRule
# Retrieved 2026-03-13, License - CC BY-SA 4.0

import sys,tty,termios

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
                println(commands[read])
                read = ''
                break
            read += getch()
        # Interpret all other inputs as text input
        for c in read:
            if c == " ":
                c = "space"
            println(c)

# Always clean up
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
    println('bye')
    sys.exit(0)
