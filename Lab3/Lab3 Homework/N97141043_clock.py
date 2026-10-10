from datetime import datetime
from time import sleep

import RPi.GPIO as GPIO
import tm1637

# 沿用 demo.py 中能正常顯示的腳位設定
CLK = 4
DIO = 5

tm = tm1637.TM1637(clk=CLK, dio=DIO)

try:
    while True:
        now = datetime.now()
        colon_on = now.second % 2 == 0
        tm.numbers(now.hour, now.minute, colon=colon_on)
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()