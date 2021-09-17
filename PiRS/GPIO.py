import RPi.GPIO as GPIO

DATA = 5

def initPiCom():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(DATA, GPIO.OUT)

def main():
    P = 1
    while 1:
        P = not P
        if P == 1:
            GPIO.output(DATA, GPIO.HIGH)
        else:
            GPIO.output(DATA, GPIO.LOW)
