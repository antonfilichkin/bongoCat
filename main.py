from machine import Pin, SoftI2C
import time
import asyncio
import ssd1306
import framebuf
import config
import common
import images

button_l = Pin(config.BUTTON_L_PIN, Pin.IN, Pin.PULL_UP)
button_r = Pin(config.BUTTON_R_PIN, Pin.IN, Pin.PULL_UP)

i2c = SoftI2C(sda=Pin(config.I2C_DATA_PIN), scl=Pin(config.I2C_CLOCK_PIN))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.rotate(False)
display.contrast(255)
# display.invert(127)


async def __read_button(button: Pin):
    while True:
        current = button.value()
        active = 0
        while active < config.BUTTON_DEBOUNCE_DELAY_MS:
            if current == button.value():
                active += 1
            else:
                active = 0
                asyncio.sleep_ms(1)
        if active == config.BUTTON_DEBOUNCE_DELAY_MS:
            return button.value()
        await asyncio.sleep_ms(20)


last_tap = {}


def __paw_code(paw, state):
    if state:
        if paw not in last_tap:
            last_tap[paw] = time.ticks_ms()
        else:
            if time.ticks_diff(time.ticks_ms(), last_tap[paw]) > 400:
                return '1'
        return '2'
    else:
        if paw in last_tap:
            last_tap.pop(paw)
        return '0'


async def main_handler():
    while True:
        left = await __read_button(button_l)
        right = await __read_button(button_r)
        print(f'Button L = {left}')
        print(f'Button R = {right}')
        paw_code = f"p{__paw_code('left', left)}{__paw_code('right', right)}"
        display.fill(0)
        fbuf = framebuf.FrameBuffer(images.paws[paw_code], 128, 64, framebuf.MONO_HLSB)
        display.blit(fbuf, 0, 0)
        display.show()
        await asyncio.sleep_ms(20)

loop = asyncio.get_event_loop()
loop.set_exception_handler(common.exception_handler)
loop.create_task(main_handler())
loop.run_forever()
