# SPDX-FileCopyrightText: Copyright (c) 2021 Eva Herrada for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Code for communicating between two CircuitPlayground Express boards using UART.
Sends value from the onboard light sensor to the other board and the other board sets its
NeoPixels accordingly.
"""

import time
import board
import busio


# Use a timeout of zero so we don't delay while waiting for a message.
uart = busio.UART(board.GP16, board.GP17, baudrate=9600, timeout=0)

# Messages are of the form:
# "<TYPE,value,value,value,...>"
# We send and receive two types of messages:
#
# Message contains a light sensor value (float):
# <L,light>
#
# Message contains statuses of two buttons. Increment NeoPixel brightness by 0.1 if the second
# button is pressed, and reduce brightness by 0.1 if the first button is pressed.
# <B,btn_A,btn_B>

UPDATE_INTERVAL = .5
last_time_sent = 0

# Wait for the beginning of a message.
message_started = False
def sendSetup(type="S",data=""):
    uart.write(bytes(f"<{type}{data}>", "ascii"))

data = ";"+str({
    "wires":[

    ],
})
failed = 0
sendSetup()
while True:
        
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
            if message_parts[0] == "False":
                print("failed")
                failed += 1
                if failed >= 5:
                    sendSetup()


        else:
            # Accumulate message byte.
            message.append(chr(byte_read[0]))
