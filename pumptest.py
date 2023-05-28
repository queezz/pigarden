import RPi.GPIO as GPIO
import time
import datetime
import os

TEST = True
TBETWEEN = {"day": 60 * 15, "night": 60 * 60 * 1, "test": 5}
DRYSTATE = False
WATERINGTIME = 5.0

chn = {"soil0": 17, "soil1": 22, "soil": 27, "soilon": 16, "v1": 20, "v2": 21}
GPIO.setmode(GPIO.BCM)
GPIO.setup(chn["soil"], GPIO.IN)
[GPIO.setup(chn[i], GPIO.OUT) for i in ["soilon", "v1", "v2"]]

[GPIO.output(chn[i], 0) for i in ["v1", "v2"]]

if not os.path.exists("logwater.txt"):
    with open("logwater.txt", "w") as f:
        f.write("")
try:
    print(f"watering for {WATERINGTIME}s")
    print("voltage on")
    [GPIO.output(chn[i], 1) for i in ["v1", "v2"]]
    time.sleep(WATERINGTIME)
    [GPIO.output(chn[i], 0) for i in ["v1", "v2"]]

except Exception as e:
    print(e)

GPIO.cleanup()
