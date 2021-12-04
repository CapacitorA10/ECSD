import RPi.GPIO as GPIO
import time
from imread import imread
from motor import motor

out1 = 18 #17
out2 = 17 #18
out3 = 27 #27
out4 = 22 #22

GPIO.setmode(GPIO.BCM)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

# initializing
GPIO.output( out1, GPIO.LOW )
GPIO.output( out2, GPIO.LOW )
GPIO.output( out3, GPIO.LOW )
GPIO.output( out4, GPIO.LOW )

mem='n'
for i in range(11):
    drctn = imread(i, 1) # 각 이미지에서 받아오는 좌,우 정보 문자 direction

    if drctn == mem:
        pass
    elif mem == 'n':
        motor(drctn)
    elif mem == 'r':
        if drctn == 'n': motor('l')
        else:
            motor('l')
            motor('l')
    elif mem == 'l':
        if drctn == 'n': motor('r')
        else:
            motor('r')
            motor('r')
    # 모터 구동 끝

def clean():
    GPIO.output( out1, GPIO.LOW )
    GPIO.output( out2, GPIO.LOW )
    GPIO.output( out3, GPIO.LOW )
    GPIO.output( out4, GPIO.LOW )
    GPIO.cleanup()

clean()
