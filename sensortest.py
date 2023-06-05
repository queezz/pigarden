import RPi.GPIO as GPIO
import time
import datetime
import os

TEST = True
DRYSTATE = False
tbetween = 0.5

chn = {"soil0": 17, "soil1": 22, "soil": 27, "soilon": 16, "v1": 20, "v2": 21}
GPIO.setmode(GPIO.BCM)
GPIO.setup(chn["soil"], GPIO.IN)
[GPIO.setup(chn[i], GPIO.OUT) for i in ["soilon"]]

if not os.path.exists("logwater.txt"):
    with open("logwater.txt", "w") as f:
        f.write("")
try:
    GPIO.output(chn["soilon"], 1)
    time.sleep(1)
    while True:
        if GPIO.input(chn["soil"]) == 0:
            DRYSTATE = False
        elif GPIO.input(chn["soil"]) == 1:
            DRYSTATE = True

        now_time = datetime.datetime.now().time()

        s = f"{datetime.datetime.now().strftime('%d %b %Y %H:%M:%S')}"
        s += f",\t{'Soil is Dry' if DRYSTATE else 'Soil is Wet'}"
        print(s)

        time.sleep(tbetween)

except Exception as e:
    print(e)
finally:
    GPIO.cleanup()

GPIO.cleanup()
