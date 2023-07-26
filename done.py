# pyright: ignore[reportShadowedImports]
import board, busio, time
import board
import displayio 
import displayio as dio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import math, random
import rotaryio, digitalio, terminalio, pwmio
import adafruit_ssd1306 
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
dc = board.GP4
reset = board.GP0
#Encoder configuration
encoder = rotaryio.IncrementalEncoder(board.GP7, board.GP6)
btn = digitalio.DigitalInOut(board.GP5)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

#DisplayIO setup
displayio.release_displays()
display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=reset)

display = GC9A01(display_bus, width=240, height=240)
#Morse
i2c = busio.I2C(board.GP19, board.GP18)
display_morse = adafruit_ssd1306.SSD1306_I2C(128,64,i2c, addr=0x3C)

display_morse.fill(0)
display_morse.show()

splash = displayio.Group()
display.show(splash)

timer = Label(font=terminalio.FONT, text="00:00", color=0x0000FF, x=0, y=0, anchor_point=(0.5, 0.5), scale=3)
timer.anchored_position = ((display.width//2)-0,(display.height//2)-35)
splash.append(timer)

status = Label(font=terminalio.FONT, text="DEFUSED", color=0x00FF00, x=0, y=0, anchor_point=(0.5, 0.5), scale=2)
status.anchored_position = ((display.width//2)+5,(display.height//2)-62)
splash.append(status)
def convert(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%02d:%02d" % (minutes, seconds)

while btn.value != False:
    position = encoder.position
    detonationTime = (position*10)
    status.text = "Detonation time"
    timer.text = convert(detonationTime)
encoder.position = 0
while btn.value != True: 
    print("waiting to release")
while btn.value != False:
    position = encoder.position
    strikeLimit = position
    status.text = "Num of mistakes"
    timer.text = str(strikeLimit)
encoder.position = 0
while btn.value != True: 
    print("waiting to release")
while btn.value != False:
    position = encoder.position
    status.text = "Press to start"
    timer.text = "--:--"
encoder.position = 0
status.text = "Strikes: 0"

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
#pyright: ignore[reportShadowedImports]
import time
import digitalio
import board
import random
uart = busio.UART(board.GP16, board.GP17, baudrate=9600, timeout=0)
#How long we want the LED to stay on
onDuration = 0.6

#How long we want the LED to stay off
offDuration = 1

#When we last changed the LED state
lastStateTime = -1
lastStateTime2 = -1
#Setup the LED pin.
led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT

rows = [board.GP8, board.GP10, board.GP9, board.GP11]
columns = [board.GP12, board.GP13, board.GP14]
row_pins = [digitalio.DigitalInOut(pin) for pin in rows]
column_pins = [digitalio.DigitalInOut(pin) for pin in columns]
err = 0
strikes = 0
codes = [
    ["WXYZ", "6845"],
    ["WYXZ", "7648"],
    ["WYWX", "1248"],
    ["WYWV", "1976"],
    ["VYWV", "1645"],
    ["VYVV", "7286"],
    ["VYVU", "4486"],
    ["XYVU", "1669"],
    ["XYUU", "6986"],
    ["XYUT", "2485"],
    ["XZUT", "5736"],
    ["XZUS", "6128"],
    ["XZUR", "7482"],
    ["XZER", "7836"],
    ["XZAR", "9824"],
    ["XZAP", "1982"],
    ["XZBP", "8293"],
    ["XZBO", "4763"],
    ["XZBN", "9861"],
    ["XZNN", "7843"],
]
morse_done = False


def buttonMatrix():
    for i in range(len(rows)):
        row_pins[i].direction = digitalio.Direction.OUTPUT
        row_pins[i].value = False
        for j in range(len(columns)):
            column_pins[j].direction = digitalio.Direction.INPUT
            column_pins[j].pull = digitalio.Pull.UP
            if not row_pins[i].value and not column_pins[j].value:
                key_index = i * len(columns) + j
                return key_index
        row_pins[i].direction = digitalio.Direction.INPUT
        row_pins[i].pull = digitalio.Pull.UP
def verifyAnswer(userInput, generatedValues):
    global morse_done
    generatedAnswer = []
    for number in generatedValues[1]:
        generatedAnswer.append(number)
    print(userInput, generatedAnswer)
    if userInput == generatedAnswer:
        display_morse.fill(0)
        display_morse.text("OK",0,0,1,size=2)
        display_morse.show()
        morse_done = True
        return True
    display_morse.fill(0)
    display_morse.text("WRONG",0,0,1,size=2)
    display_morse.show()
    strikes += 1
    return False
answer = []
def setAnswer(key, geneatedValues):
    if key == "*":
        if len(answer) != 0:
            answer.pop(-1)
    elif key == "#":
        print(verifyAnswer(answer, geneatedValues))
        
    else:
        answer.append(key)
    if not morse_done:
        display_morse.fill(0)
        display_morse.text(" ".join(answer), 0, 20, 1, size=2)
        display_morse.show()
def morseTranslate(message):
    morseDict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
        'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
        'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
        'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
        ' ': ' ',  #Space between words
    }
    
    #Convert text to uppercase
    message = message.upper()
    morseCode = []
    #Translate message to Morse code and blink the LED accordingly
    for char in message:
        if char in morseDict:
            morseCode.append(morseDict[char])
    return morseCode
import supervisor
generatedValues = codes[random.randrange(len(codes))]
print(generatedValues[0], generatedValues[1])
sentence = morseTranslate(generatedValues[0])
finished = False
realId = ["1","2","3","4","5","6","7","8","9","*","0","#"]
buzzer = digitalio.DigitalInOut(board.GP20)
buzzer.direction = digitalio.Direction.OUTPUT
started = True
message_started = False
explodeTime = detonationTime+time.monotonic_ns()/1000000000
hiero_done = False

while True: 
    if started == True:
        for symbol in sentence:
            for signal in symbol:
                while not finished:
                    print(signal, symbol)
                    now2 = time.monotonic()
                    if 0 > (explodeTime - now2) or strikes > strikeLimit :
                        status.text = "EXPLODED!"
                        status.color = 0xFF0000
                        buzzer.value = True
                        time.sleep(3)
                        buzzer.value = False
                        while btn.value != False:
                            pass
                        supervisor.reload()
                    if morse_done and hiero_done:
                        status.text = "DEFUSED!"
                        status.color = 0x00FF00
                        while btn.value != False:
                            pass
                        supervisor.reload()
                    timer.text = convert(explodeTime - now2)
                    status.text = f"Strikes: {strikes}/{strikeLimit}"
                    if not buzzer.value:
                        #Is it time to turn on?
                        if now2 >= lastStateTime2 + 0.85 and not finished:
                            buzzer.value = True
                            lastStateTime2 = now2
                    if buzzer.value:
                        #Is it time to turn off?
                        if now2 >= lastStateTime2 + 0.15 and not finished:
                            buzzer.value = False
                            lastStateTime2 = now2
                    if signal == "-":
                        onDuration = .6
                    else:
                        onDuration = .15
                    now = time.monotonic()
                    if not led.value and not morse_done:
                        #Is it time to turn on?
                        if now >= lastStateTime + offDuration:
                            led.value = True
                            lastStateTime = now
                            finished = False
                            #print("ON")
                    if led.value:
                        #Is it time to turn off?
                        if now >= lastStateTime + onDuration:
                            led.value = False
                            lastStateTime = now
                            finished = True
                            #print("OFF")
                    keyPressed = buttonMatrix()
                    if keyPressed is not None:
                        setAnswer(realId[int(keyPressed)], generatedValues)
                        while buttonMatrix() is not None:
                            pass
                    #print("DAMN")
                    position = encoder.position
                    passcode.text = "e".join(code)
                    if code == key:
                        passcode.color = 0x00FF00
                        hiero_done = True
                    elif "?" in code:
                        pass
                    else:
                        passcode.color = 0xFF0000
                        code = ["?","?","?","?"]
                        o = 0
                        strikes += 1
                        time.sleep(2)
                        passcode.color = 0x0000FF
                    try:
                        if last_position is None or position != last_position:
                            if(len(letters)==position):
                                encoder.position = 0
                                position = encoder.position
                            elif((-1)*len(letters)==position):
                                encoder.position = 0
                                position = encoder.position
                            highlightLetter(position, -16, -1)
                            print(position, letters[position])
                    except:
                        encoder.position = 0
                    if btn.value == False and btn.value != prev_val and not hiero_done:
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
                finished = False
            setDuration = time.monotonic_ns()+2*1000000000
            while True:
                now = time.monotonic_ns()
                keyPressed = buttonMatrix()
                if keyPressed is not None:
                    setAnswer(realId[int(keyPressed)], generatedValues)
                    while buttonMatrix() is not None:
                        pass
                now2 = time.monotonic()
                timer.text = convert(explodeTime - now2)
                status.text = f"Strikes: {strikes}/{strikeLimit}"
                if 0 > (explodeTime - now2):
                        buzzer.value = True
                        time.sleep(3)
                        buzzer.value = False
                        while btn.value != False:
                            pass
                        supervisor.reload()
                if morse_done and hiero_done:
                        status.text = "DEFUSED!"
                        status.color = 0x00FF00
                        while btn.value != False:
                            pass
                        supervisor.reload()
                if not buzzer.value:
                    #Is it time to turn on?
                    if now2 >= lastStateTime2 + 0.85 and not finished:
                        buzzer.value = True
                        lastStateTime2 = now2
                if buzzer.value:
                    #Is it time to turn off?
                    if now2 >= lastStateTime2 + 0.15 and not finished:
                        buzzer.value = False
                        lastStateTime2 = now2
                if now > setDuration:
                    break
                position = encoder.position
                passcode.text = "e".join(code)
                if code == key:
                    passcode.color = 0x00FF00
                    hiero_done = True
                elif "?" in code:
                    pass
                else:
                    passcode.color = 0xFF0000
                    code = ["?","?","?","?"]
                    o = 0
                    strikes += 1
                    time.sleep(2)
                    passcode.color = 0x0000FF
                try:
                    if last_position is None or position != last_position:
                        if(len(letters)==position):
                            encoder.position = 0
                            position = encoder.position
                        elif((-1)*len(letters)==position):
                            encoder.position = 0
                            position = encoder.position
                        highlightLetter(position, -16, -1)
                        print(position, letters[position])
                except:
                    encoder.position = 0
                if btn.value == False and btn.value != prev_val and not hiero_done:
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
    else:
        byte_read = uart.read(1)  # Read one byte over UART lines
        if not byte_read:
            # Nothing read.
            continue

        if byte_read == b"<":
            # Start of message. Start accumulating bytes, but don't record the "<".
            message = []
            message_started = True
            continue

        if message_started:
            if byte_read == b">":
                # End of message. Don't record the ">".
                # Now we have a complete message. Convert it to a string, and split it up.
                #print(message)
                message_parts = "".join(message).split(",")
                message_type = message_parts[0]
                message_started = False
                if message_parts[0]=="START":
                    started = True
            else:
                # Accumulate message byte.
                message.append(chr(byte_read[0]))

