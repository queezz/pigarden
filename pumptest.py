import RPi.GPIO as GPIO
import time
import datetime
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-t","--time",dest="wateringtime",type=float)
args = parser.parse_args()
print(args.wateringtime)

TEST = True
TBETWEEN = {"day": 60 * 15, "night": 60 * 60 * 1, "test": 5}
DRYSTATE = False
WATERINGTIME = 3
if args.wateringtime is not None:
    WATERINGTIME = args.wateringtime 

chn = {"soil0": 17, "soil1": 22, "soil": 27, "soilon": 16, "v1": 20, "v2": 21}
GPIO.setmode(GPIO.BCM)
GPIO.setup(chn["soil"], GPIO.IN)
[GPIO.setup(chn[i], GPIO.OUT) for i in ["soilon", "v1", "v2"]]

[GPIO.output(chn[i], 0) for i in ["v1", "v2"]]

try:
    print(f"watering for {WATERINGTIME}s")
    print("voltage on")
    [GPIO.output(chn[i], 1) for i in ["v1", "v2"]]
    time.sleep(WATERINGTIME)
    [GPIO.output(chn[i], 0) for i in ["v1", "v2"]]

except Exception as e:
    print(e)

GPIO.cleanup()
