#pyright: ignore[reportShadowedImports]
import board, time, digitalio
NONE = 0
WHITE = 1
BLUE = 2
BLACK = 3
YELLOW = 4
RED = 5

"""
solution = {
    "3wire":[
        #Serial only1 not   more  last   solution
        [[NONE, NONE, RED , NONE, NONE]  , 2],
        [[NONE, NONE, NONE, NONE, WHITE] ,-1],
        [[NONE, NONE, NONE, BLUE, NONE]  ,-1],
        [[NONE, NONE, NONE, NONE, NONE]  ,-1], #ELSE
    ],
    "4wire":[
        #Serial only1 not   more  last   solution
        [[ODD , NONE, NONE, RED , NONE]  ,-1],
        [[NONE, NONE, RED , NONE, YELLOW], 1],
        [[NONE, BLUE, NONE, NONE, NONE]  , 1],
        [[NONE, NONE, NONE, YELLOW, NONE],-1],
        [[NONE, NONE, NONE, NONE, NONE]  , 2], #ELSE
    ],
    "5wire":[
        #Serial only1 not   more  last   solution
        [[ODD , NONE, NONE, NONE, BLACK] , 4],
        [[NONE, RED , NONE, YELLOW, NONE], 1],
        [[NONE, NONE, RED , NONE, NONE]  , 2],
        [[NONE, NONE, NONE, NONE, NONE]  , 1], #ELSE
    ],
    "6wire":[
        #Serial only1 not   more  last   solution
        [[ODD , NONE, YELLOW, NONE, NONE], 3],
        [[NONE, YELLOW,NONE, WHITE, NONE], 4],
        [[NONE, NONE, RED , NONE, NONE]  ,-1],
        [[NONE, NONE, NONE, NONE, NONE]  , 4], #ELSE
    ],
}
"""
wires = [
    [digitalio.DigitalInOut(board.GP0), BLUE ],
    [digitalio.DigitalInOut(board.GP1), NONE ],
    [digitalio.DigitalInOut(board.GP2), NONE ],
    [digitalio.DigitalInOut(board.GP3), YELLOW],
    [digitalio.DigitalInOut(board.GP4), NONE ],
    [digitalio.DigitalInOut(board.GP5), WHITE],
]

for i in wires:
    i[0].switch_to_input()
    i[0].pull = digitalio.Pull.DOWN
o = 0
while o != len(wires):
    print(wires[o][1])
    if wires[o][1] == NONE:
        wires.pop(o)
    o+=1
print(str(wires))

class wireRules:
    #RETURNS BOOLEAN VALUES
    #Checks if array of wires contains specified color
    def contains(wires, color=int):
        for i in wires:
            if i[1] == color:
                return True
        return False
    #Checks if a specified colored wire is at the end of wire sequence
    def lastPos(wires, color=int):
        #a, b = wires[-1]
        if wires[-1][1] == color:
            return True
        return False
    #Checks if a wire sequence contains more than minAmount of specified color
    def moreThan(wires, color, minAmount=1):
        #result = [el for el in wires if el[1]==color]
        duplicateIndex = 0
        for i in wires:
            if i[1] == color:
                duplicateIndex +=1
        if duplicateIndex > minAmount:
            return True
        return False
    #Check if only one wire with certain color is present
    def onlyOne(wires, color):
        hasWires = False
        for i in wires:
            if i[1] != NONE:
                hasWires = True
        if hasWires == True:
            return not wireRules.moreThan(wires, color)
        return False
    def serialOdd(serialNum):
        serialNum.strip()
        return int(serialNum[-1]) % 2 != 0

def checkAlgorythm(cutWire, wireTot=len(wires), wires=wires, serialNum="HRL21"):
    if wireTot == 3:
        #WORKS
        if not wireRules.contains(wires,RED):
            return cutWire == 2
        elif wireRules.lastPos(wires, WHITE):
            return cutWire == 3
        elif wireRules.moreThan(wires, BLUE):
            return cutWire == 3
        else:
            return cutWire == 3
    elif wireTot == 4:
        #WORKS
        if wireRules.moreThan(wires, RED) and wireRules.serialOdd(serialNum):
            return cutWire == 4
        elif wireRules.lastPos(wires, YELLOW) and (not wireRules.contains(wires, RED)):
            return cutWire == 1
        elif wireRules.onlyOne(wires, BLUE):
            return cutWire == 1
        elif wireRules.moreThan(wires, YELLOW):
            return cutWire == 4
        else:
            return cutWire == 2
    elif wireTot == 5:
        if wireRules.lastPos(wires, BLACK) and wireRules.serialOdd(serialNum):
            return cutWire == 4
        elif wireRules.moreThan(wires, YELLOW) and wireRules.onlyOne(wires, RED):
            return cutWire == 1
        elif not wireRules.contains(wires, RED):
            return cutWire == 2
        else:
            return cutWire == 1
    elif wireTot == 6:
        if (not wireRules.contains(wires, YELLOW)) and wireRules.serialOdd(serialNum):
            return cutWire == 3
        elif wireRules.moreThan(wires, WHITE) and wireRules.onlyOne(wires, YELLOW):
            return cutWire == 4
        elif not wireRules.contains(wires, RED):
            return cutWire == 6
        else:
            return cutWire == 4

while True:
    i=0
    while i != len(wires):
        if wires[i][0].value == False:
            print(i+1,checkAlgorythm(i+1))
            input()
        i+=1


    """
    print(wireRules.contains(wires, RED))
    print(wireRules.lastPos(wires, WHITE))
    print(wireRules.moreThan(wires, RED))
    print(wireRules.onlyOne(wires, RED))
    input(">")
    """



while True:
    for i in wires:
        print(i[0].value)
    print("-----")
    time.sleep(0.5)



