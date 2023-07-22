#pyright: ignore[reportShadowedImports]
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Mark Olsson <mark@markolsson.se>
# SPDX-License-Identifier: MIT

import time
import board
import busio
import digitalio

import adafruit_st7565


# Initialize SPI bus and control pins
spi = busio.SPI(board.GP6, MOSI=board.GP3)
dc = digitalio.DigitalInOut(board.GP2)  # data/command
cs = digitalio.DigitalInOut(board.GP0)  # Chip select
reset = digitalio.DigitalInOut(board.GP1)  # reset
display = adafruit_st7565.ST7565(spi, dc, cs, reset)

display.rotation = 2
display.contrast = 0

# Turn on the Backlight LED
backlight = digitalio.DigitalInOut(board.GP8)  # backlight
backlight.switch_to_output()
backlight.value = True
import time
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%02d:%02d" % (minutes, seconds)






setTime = round((900)+(time.monotonic_ns()/1000000000))
display.text("x-_", 42, 5, 1, size=2)
while True:
    timer = convert((setTime-round(time.monotonic_ns()/1000000000)))
    #print(setTime, timer)
    display.text(" - ", 42, 5, 0, size=2)
    display.text("x- ", 42, 5, 1, size=2)
    display.text(timer, 15, 25, 1, size=3)
    display.show()
    time.sleep(0.2)
    display.text("x- ", 42, 5, 0, size=2)
    display.text(" - ", 42, 5, 1, size=2)
    display.show()
    time.sleep(0.2)
    display.text(timer, 15, 25, 0, size=3)
    time.sleep(0.01)