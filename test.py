import RPi.GPIO as GPIO
import time
import datetime
import os

TEST = True
TBETWEEN = {"day": 60 * 30, "night": 60 * 60 * 2, "test": 2}
DRYSTATE = False

chn = {"soil0": 17, "soil1": 22, "soil": 27, "soilon": 16, "v1": 20, "v2": 21}
GPIO.setmode(GPIO.BCM)
GPIO.setup(chn["soil"], GPIO.IN)
[GPIO.setup(chn[i], GPIO.OUT) for i in ["soilon", "v1", "v2"]]

[GPIO.output(chn[i], 0) for i in ["v1", "v2"]]

if not os.path.exists("logwater.txt"):
    with open("logwater.txt", "w") as f:
        f.write("")
try:
    while True:
        GPIO.output(chn["soilon"], 1)
        time.sleep(0.2)
        if GPIO.input(chn["soil"]) == 0:
            DRYSTATE = False
            [GPIO.output(chn[i], 0) for i in ["v1", "v2"]]
        elif GPIO.input(chn["soil"]) == 1:
            DRYSTATE = True

        GPIO.output(chn["soilon"], 0)

        now_time = datetime.datetime.now().time()
        night = now_time >= datetime.time(23, 0) or now_time <= datetime.time(7, 30)
        if not night:
            tbetween = TBETWEEN["day"]
        else:
            tbetween = TBETWEEN["night"]
        if TEST:
            tbetween = TBETWEEN["test"]

        s = f"{datetime.datetime.now().strftime('%d %b %Y %H:%M:%S')}"
        s += f",\tnight = {night},\tDRYSTATE = {DRYSTATE}"
        print(s)
        with open("logwater.txt", "a") as f:
            f.write(s + "\n")

        if DRYSTATE:
            if not night:
                [GPIO.output(chn[i], 1) for i in ["v1", "v2"]]
                time.sleep(0.5)
                [GPIO.output(chn[i], 0) for i in ["v1", "v2"]]

        time.sleep(tbetween)

except Exception as e:
    print(e)

GPIO.cleanup()
