from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution=(1280, 720)
camera.start_preview()

sleep(60)
camera.stop_preview()
