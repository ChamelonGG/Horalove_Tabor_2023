# pyright: ignore[reportShadowedImports]
import board, busio, time
import board
import displayio 
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import math, random
import rotaryio, digitalio, terminalio, pwmio
from gc9a01 import GC9A01
displayio.release_displays()

font = bitmap_font.load_font("/Hieroglyfy_tabor-Regular.bdf")
#GC9A01 configuration
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3)
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000)  #24MHz
spi.unlock()
cs = board.GP1
dc = board.GP0
reset = board.GP14
#Encoder configuration
encoder = rotaryio.IncrementalEncoder(board.GP7, board.GP8)
btn = digitalio.DigitalInOut(board.GP15)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

#DisplayIO setup
displayio.release_displays()
display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=reset)

display = GC9A01(display_bus, width=240, height=240)

splash = displayio.Group()
display.show(splash)
#Infotext setup
passcode = Label(font=font, text="?e?e?e?", color=0x0000FF, x=0, y=0, anchor_point=(0.5, 0.5), scale=1)
passcode.anchored_position = ((display.width//2)-0,(display.height//2)-0)
splash.append(passcode)

highlight = Label(font=terminalio.FONT, text="[]", color=0xFF0000, x=0, y=0, anchor_point=(0.5, 0.5), scale=4)
splash.append(highlight)
offsetx = 12
offsety = 0
offsetr = 15
def shuffleArray(array):
    for i in range(len(array) - 1, 0, -1):
        j = random.randint(0, i)
        array[i], array[j] = array[j], array[i]
def letterAlgorythm(numletters=4):
    key = []
    lettercolumns = [
        ["O","A","D","I","B","H","J"],
        ["G","O","J","M","X","H","R"],
        ["K","N","M","W","U","D","Y"],
        ["V","P","Q","B","W","R","C"],
        ["E","C","Q","Y","P","I","X"],
        ["V","G","L","S","E","F","T"]
    ]
    column = lettercolumns[random.randrange(len(lettercolumns))]
    key.append(column[random.randint(0,1)])
    key.append(column[random.randint(2,3)])
    key.append(column[random.randint(4,5)])
    key.append(column[-1])
    print(str(key))
    result = []
    for i in key:
        result.append(i)
    while len(result)!=numletters:
        letter = letters[random.randrange(len(letters))]
        if letter not in result:
            result.append(letter)
    shuffleArray(result)
    result.append("!")
    return [result, key]

def generateLetters(letters):
    display_center_x = (display.width // 2) - offsetx
    display_center_y = (display.height // 2) - offsety
    radius = min(display.width, display.height) // 2 - offsetr
    angle_increment = (2 * math.pi) / len(letters)
    for i, letter in enumerate(letters):
        angle = i * angle_increment

        x = int(display_center_x + radius * math.cos(angle))
        y = int(display_center_y + radius * math.sin(angle))

        color = 0xFFFFFF
        if(letter == "!"):color = 0xFF0000
        label = Label(font=font, text=letter, color=color, x=x, y=y, anchor_point=(0.5, 0.5), scale=1)

        splash.append(label)
    display.show(splash)
def highlightLetter(index, offsetx_, offsety_):
    display_center_x = (display.width // 2) - offsetx
    display_center_y = (display.height // 2) - offsety
    radius = min(display.width, display.height) // 2 - offsetr
    angle = index*(2 * math.pi) / len(letters)
    x = int(display_center_x + radius * math.cos(angle))
    y = int(display_center_y + radius * math.sin(angle))

    highlight.anchored_position = (x-offsetx_,y-offsety_)
    display.refresh()

data = letterAlgorythm()
letters = data[0]
key = data[1]
generateLetters(letters)


prev_val = None
last_position = None
code = ["?","?","?","?"]
o = 0

"""
buzzer = pwmio.PWMOut(board.GP26, variable_frequency=True)
buzzer.duty_cycle = 65535 // 6

while True:
    buzzer.frequency = 3520
    asyncio.sleep(0.4)
    buzzer.frequency = 2793
    asyncio.sleep(0.1)
    buzzer.frequency = 65535
    asyncio.sleep(0.7)
"""
while True:
    position = encoder.position
    passcode.text = "e".join(code)
    if code == key:
        passcode.color = 0x00FF00
        input()
    elif "?" in code:
        pass
    else:
        passcode.color = 0xFF0000
        code = ["?","?","?","?"]
        o = 0
        time.sleep(2)
        passcode.color = 0x0000FF
    if last_position is None or position != last_position:
        if(len(letters)==position):
            encoder.position = 0
            position = encoder.position
        elif((-1)*len(letters)==position):
            encoder.position = 0
            position = encoder.position
        highlightLetter(position, -16, -1)
        print(position, letters[position])
    if btn.value == False and btn.value != prev_val:
        print("run")
        if(letters[position]=="!"):
            if(o==0):
                pass
            else:
                o-=1
                code[o] = "?"
        else:
            code[o] = letters[position]
            o+=1
    prev_val = btn.value
    last_position = position   
        

