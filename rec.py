from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)



class hCamy():
    BeepHR=0.1
    buzzer=38
    button=40
    recState=0# 0 is false 1 is true 3 is trans
    def __init__(self):
        self.camera = PiCamera()
        self.recState=0 # 0 is false 1 is true 3 is trans
        GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)
        GPIO.input(button)
    def toggleRec(self):
        if self.recState:
            self.stopRecording()
        else:
            self.startRecording()
    def startRecording(self):
        #
        playTune(3)
        self.recState=1
    def stopRecording(self):
        #
        playTune(7)
        self.recState=0

    def playTune(self,iters):
        self.recState=3
        for i in range(iters):
            GPIO.output(self.buzzer, 1)
            time.sleep(self.BeepHR)
            GPIO.output(self.buzzer, 0)
            time.sleep(self.BeepHR)

if __name__=="__main__":
    cam=hCamy()
    while(True):
        if(cam.recState==0):
            GPIO.output(cam.buzzer,0)
            time.sleep(3)
            GPIO.output(cam.buzzer,1)
            time.sleep(0.05)
        elif(cam.recState==1):
            GPIO.output(cam.buzzer,0)
            time.sleep(3)
            GPIO.output(cam.buzzer,1)
            time.sleep(0.05)
            GPIO.output(cam.buzzer,0)
            time.sleep(0.05)
            GPIO.output(cam.buzzer,1)
            time.sleep(0.05)
        else:
            time.sleep(3)
        print("App Running... ",cam.recState)

