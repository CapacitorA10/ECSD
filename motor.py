import RPi.GPIO as GPIO
import time


def motor(i):
    out1 = 18  # 17
    out2 = 17  # 18
    out3 = 27  # 27
    out4 = 22  # 22
    step_sleep = 0.005
    step_count = 100
    if i == 'r':
        for i in range(step_count):
            if i % 4 == 0:
                GPIO.output(out4, GPIO.HIGH)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out1, GPIO.LOW)
            if i % 4 == 1:
                GPIO.output(out4, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out2, GPIO.HIGH)
                GPIO.output(out1, GPIO.LOW)
            if i % 4 == 2:
                GPIO.output(out4, GPIO.LOW)
                GPIO.output(out3, GPIO.HIGH)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out1, GPIO.LOW)
            if i % 4 == 3:
                GPIO.output(out4, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out1, GPIO.HIGH)
            time.sleep(step_sleep)

    elif i == 'l':
        for i in range(step_count):
            if i % 4 == 0:
                GPIO.output(out4, GPIO.HIGH)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out1, GPIO.LOW)
            if i % 4 == 1:
                GPIO.output(out4, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out1, GPIO.HIGH)
            if i % 4 == 2:
                GPIO.output(out4, GPIO.LOW)
                GPIO.output(out3, GPIO.HIGH)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out1, GPIO.LOW)
            if i % 4 == 3:
                GPIO.output(out4, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out2, GPIO.HIGH)
                GPIO.output(out1, GPIO.LOW)
            time.sleep(step_sleep)
