# Všichni ne vedoucí Horalové opusťte tento repozitář prosím!

# HORALOVÉ TÁBOR 2023
## Loupení z trezoru - Puma

Repozitář obsahuje rekreace modulů ze hry KTANE **(Keep talking and nobody explodes)**.
Určeno k užítí v etapové hře na **Horalském táboře 2023**.

Interní logika pumy psána pro CircuitPython 8.2.0 na Pi Pico a Pi Pico W

### Obsah všech rekreovaných modulů **(viz složka ./Modules)**:
- Hieroglyfy >funkční prototyp<
- <s>Bludiště >zrušeno<</s>
- Morseova klávesnice >funkční prototyp<
- Napěťové dělení >integrováno<
- Dráty >integrováno<
- <s>"Jakub" řekl (Siamon Says) >zrušeno<</s>

- Časovač >integrováno<
### Využité moduly:
1. Displeje
- GC9A01 (SPI 240x240 kruhový LCD displej)
- <s>ST7735S (SPI 128x64 obdélníkový LCD displej)</s>
- SSD1306 (I2C 128x64 obdélníkový OLED displej)
- SSD1306 (I2C 64x32 obdélníkový OLED displej)
2. Bezdrátové připojení
- Infineon CYW43439 (SPI 802.11n, BLE 5.2)
3. Ostatní aktivní komponenty
- Neopixel LED
- Barevné LED 
4. Pasivní komponenty
- <s>Resitory ruzných hodnot</s>
5. Vstupní zařízení
- Rotační enkodér 
- Tlačitkový membránový matrix 4x3
- Potenciometr 10kohm
- <s>Joystick 2 osý</s>
- Mechanická tlačítka
