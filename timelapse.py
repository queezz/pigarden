from picamera import PiCamera
from os import system
from time import sleep
import datetime

camera = PiCamera()
camera.resolution = (1024, 768)
camera.rotation = -90

i = 0
while True:
    # for i in range(1):
    name = f"images/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    # name = f"images/image{i:04d}.jpg"
    camera.capture(name)

    s = f"{datetime.datetime.now().strftime('%d %b %Y %H:%M:%S')} image #{i}"
    print(s)

    sleep(1200)
    i += 1
