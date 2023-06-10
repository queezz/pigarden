try:
    import RPi.GPIO as GPIO
except:
    print("importing Mock.GPIO instead of RPi.GPIO")
    from Mock import GPIO
import time
import datetime
import os

from argparse import ArgumentParser, BooleanOptionalAction

parser = ArgumentParser()
parser.add_argument("--test", dest="test", action=BooleanOptionalAction)
args = parser.parse_args()

TEST = False
if args.test:
    TEST = bool(args.test)

TBETWEEN = {"day": 60 * 30, "night": 60 * 60 * 1, "test": 1}
DRY = False
WATERINGTIME = 5.0
WATERING_MORNING = 30.0
MORNING_DONE = False

chn = {"soil0": 17, "soil1": 22, "soil sensor 0": 27, "soil sensor power": 16, "v1": 20, "v2": 21}


def init_logfile():
    if not os.path.exists("logwater.txt"):
        with open("logwater.txt", "w") as f:
            f.write("")


class Watering:
    def __init__(self):
        self.DRY = False
        self.morning_watering_done = False
        self.watering_time = WATERINGTIME
        self.init_gpio()
        self.time_between_soil_checks = TBETWEEN["day"]
        self.counter = 0

    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(chn["soil sensor 0"], GPIO.IN)
        [GPIO.setup(chn[i], GPIO.OUT) for i in ["soil sensor power", "v1", "v2"]]

    def power_soil_sensor(self, on=False):
        GPIO.output(chn["soil sensor power"], on)

    def read_soil_sensor(self):
        return bool(GPIO.input(chn["soil sensor 0"]))

    def pump_some_water(self):
        [GPIO.output(chn[i], 1) for i in ["v1", "v2"]]
        if not TEST:
            time.sleep(self.watering_time)
        [GPIO.output(chn[i], 0) for i in ["v1", "v2"]]

        print("pumping")

        if self.morning and not self.morning_watering_done:
            self.morning_watering_done = True

    def check_soil_moisture(self):
        self.power_soil_sensor(on=True)
        if not TEST:
            time.sleep(1.5)
        self.DRY = self.read_soil_sensor()

    def watering(self):
        self.counter += 1
        print(self.counter)
        self.set_time_intervals()
        print(
            f"{self.time_between_soil_checks}"
            f" watering time: {self.watering_time}"
            f" morning: {self.morning}"
            f" night: {self.night}"
            f" morning done: {self.morning_watering_done}"
        )

        self.check_soil_moisture()
        self.log_message()

        if self.morning and not self.morning_watering_done:
            self.pump_some_water()

        if self.DRY:
            self.pump_some_water()

        self.power_soil_sensor(on=False)

    def which_time_of_day(self):
        time_now = datetime.datetime.now().time()
        self.night = time_now >= datetime.time(20, 0) or time_now <= datetime.time(5, 30)
        self.morning = time_now >= datetime.time(5, 31) and time_now <= datetime.time(14, 30)

    def set_time_intervals(self):
        self.which_time_of_day()

        if self.morning and self.morning_watering_done:
            self.watering_time = WATERINGTIME

        if self.morning and not self.morning_watering_done:
            self.watering_time = WATERING_MORNING

        if self.night:
            self.watering_time = WATERINGTIME
            self.morning_watering_done = False
            self.time_between_soil_checks = TBETWEEN["night"]
        else:
            self.time_between_soil_checks = TBETWEEN["day"]

        if TEST:
            self.time_between_soil_checks = TBETWEEN["test"]

    def log_message(self):
        s = f"{datetime.datetime.now().strftime('%d %b %Y %H:%M:%S')}"
        s += f",{'Soil is Dry' if self.DRY else 'Soil is Wet'}"
        s += f",{self.watering_time}"
        print(s)
        with open("logwater.txt", "a") as f:
            f.write(s + "\n")


def main():
    init_logfile()
    try:
        w = Watering()
        while True:
            w.watering()
            time.sleep(w.time_between_soil_checks)

    except Exception as e:
        print(e)
        GPIO.cleanup()
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
