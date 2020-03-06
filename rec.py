import atexit
from picamera import PiCamera
import time,sys,signal
import RPi.GPIO as GPIO
from datetime import datetime
GPIO.setmode(GPIO.BOARD)

spaceTime=5
screamTime=0.02

class hCamy():
    BeepHR=0.1
    buzzer=38
    button=40
    recState=0# 0 is false 1 is true 3 is trans
    def __init__(self):
        self.camera = PiCamera()
        self.recState=0 # 0 is false 1 is true 3 is trans
        GPIO.setup(self.buzzer, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button, GPIO.RISING, callback=self.toggleRec, bouncetime=200)
        self.lastToggle=time.time()
    def toggleRec(self,event):
        if(time.time()-self.lastToggle<=2):
            return
        self.lastToggle=time.time()
        print(event)
        if self.recState:
            self.stopRecording()
        else:
            self.startRecording()
    def startRecording(self):
        #
        now = datetime.now()
        self.startTime=time.time()
        self.camera.start_recording('/home/pi/'+now.strftime("%m%d%Y%_H%M%S")+'.h264')
        self.playTune(3)
        self.recState=1
    def stopRecording(self):
        #
        self.camera.stop_recording() 
        print("%f s Recorded",time.time()-self.startTime)
        self.playTune(7)
        self.recState=0

    def playTune(self,iters):
        self.recState=3
        for i in range(iters):
            GPIO.output(self.buzzer, 1)
            time.sleep(self.BeepHR)
            GPIO.output(self.buzzer, 0)
            time.sleep(self.BeepHR)
@atexit.register
def exit_handler():
    GPIO.cleanup()
    sys.exit(0)
def cc_handler(sig,frame):
    print('You pressed Ctrl+C! or shit happened')
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, cc_handler)

if __name__=="__main__":
    cam=hCamy()
    while(True):
        if(cam.recState==0):
            GPIO.output(cam.buzzer,0)
            time.sleep(spaceTime)
            GPIO.output(cam.buzzer,1)
            time.sleep(screamTime)
        elif(cam.recState==1):
            GPIO.output(cam.buzzer,0)
            time.sleep(spaceTime)
            GPIO.output(cam.buzzer,1)
            time.sleep(screamTime)
            GPIO.output(cam.buzzer,0)
            time.sleep(screamTime*3)
            GPIO.output(cam.buzzer,1)
            time.sleep(screamTime)
        else:
            time.sleep(spaceTime)
        print("App Running... ",cam.recState)


    GPIO.cleanup()


