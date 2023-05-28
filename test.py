import RPi.GPIO as GPIO
import time
import datetime
import os

TEST = False 
TBETWEEN = {"day": 60 * 30, "night": 60 * 60 * 1, "test": 1}
DRYSTATE = False
WATERINGTIME = 5.0
WATERING_MORNING = 30.0
MORNING_DONE = False

chn = {"soil0": 17, "soil1": 22, "soil": 27, "soilon": 16, "v1": 20, "v2": 21}
GPIO.setmode(GPIO.BCM)
GPIO.setup(chn["soil"], GPIO.IN)
[GPIO.setup(chn[i], GPIO.OUT) for i in ["soilon", "v1", "v2"]]

[GPIO.output(chn[i], 0) for i in ["v1", "v2"]]

def pump_some_water(watering_time):
    [GPIO.output(chn[i], 1) for i in ["v1", "v2"]]
    time.sleep(watering_time)
    [GPIO.output(chn[i], 0) for i in ["v1", "v2"]]

if not os.path.exists("logwater.txt"):
    with open("logwater.txt", "w") as f:
        f.write("")
try:
    while True:
        GPIO.output(chn["soilon"], 1)
        time.sleep(2.2)
        if GPIO.input(chn["soil"]) == 0:
            DRYSTATE = False
            [GPIO.output(chn[i], 0) for i in ["v1", "v2"]]
        elif GPIO.input(chn["soil"]) == 1:
            DRYSTATE = True

        GPIO.output(chn["soilon"], 0)

        now_time = datetime.datetime.now().time()
        night = now_time >= datetime.time(20, 0) or now_time <= datetime.time(5, 30)
        morning = now_time >= datetime.time(5, 0) and  now_time <= datetime.time(7, 0)
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

        if night:
            MORNING_DONE = False

        if morning and not MORNING_DONE:
            print('watering at morning') 
            pump_some_water(WATERING_MORNING)

        if DRYSTATE:
            if not night:
                print('watering')
                pump_some_water(WATERINGTIME)
            else:
                pump_some_water(1.0)

        time.sleep(tbetween)

except Exception as e:
    print(e)
    GPIO.cleanup()

def pump_some_water(watering_time):
    [GPIO.output(chn[i], 1) for i in ["v1", "v2"]]
    time.sleep(watering_time)
    [GPIO.output(chn[i], 0) for i in ["v1", "v2"]]


GPIO.cleanup()
