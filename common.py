from machine import Pin
from time import sleep_ms
import asyncio
import config


# Asyncio event loop exception handler
def exception_handler(loop, context):
    if 'task' in context:
        task = f"'{context['task']}' "
    else:
        task = ''
    print(f"Task {task} failed: msg={context['message']}, exception={context['exception']}")


# ESP32c3 LED
__led__ = Pin(config.LED_PIN, Pin.OUT)
__led__.value(1)


def sleep_with_blink(seconds: int, blink_interval_ms: int = 100):
    millis = seconds * 1000
    while millis > 0:
        __led__.value(not __led__.value())
        sleep_ms(blink_interval_ms)
        millis -= blink_interval_ms
    __led__.value(1)


async def blink(times: int, blink_interval_ms: int = 20):
    for _ in range(times):
        __led__.value(0)
        await asyncio.sleep_ms(blink_interval_ms)
        __led__.value(1)
        await asyncio.sleep_ms(blink_interval_ms)
