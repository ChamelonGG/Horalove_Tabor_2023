#pyright: ignore[reportShadowedImports]
import time
import digitalio
import board
import random
#How long we want the LED to stay on
onDuration = 0.6

#How long we want the LED to stay off
offDuration = 1

#When we last changed the LED state
lastStateTime = -1

#Setup the LED pin.
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

rows = [board.GP3, board.GP4, board.GP5, board.GP6]
columns = [board.GP0, board.GP1, board.GP2]
row_pins = [digitalio.DigitalInOut(pin) for pin in rows]
column_pins = [digitalio.DigitalInOut(pin) for pin in columns]

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
    generatedAnswer = []
    for number in generatedValues[1]:
        generatedAnswer.append(number)
    print(userInput, generatedAnswer)
    if userInput == generatedAnswer:
        return True
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
    print(str(answer))
def morseTranslate(message):
    morseDict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
        'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
        'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
        'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.',
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

generatedValues = codes[random.randrange(len(codes))]
print(generatedValues[0], generatedValues[1])
sentence = morseTranslate(generatedValues[0])
finished = False
realId = ["1","2","3","4","5","6","7","8","9","*","0","#"]
while True:
    #Store the current time to refer to later.
    for symbol in sentence:
        for signal in symbol:
            while not finished:
                #print(signal, symbol)
                if signal == "-":
                    onDuration = .6
                else:
                    onDuration = .3
                now = time.monotonic()
                if not led.value:
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
            finished = False
        setDuration = time.monotonic_ns()+2*1000000000
        while True:
            now = time.monotonic_ns()
            keyPressed = buttonMatrix()
            if keyPressed is not None:
                setAnswer(realId[int(keyPressed)], generatedValues)
                while buttonMatrix() is not None:
                    pass
            if now > setDuration:
                break