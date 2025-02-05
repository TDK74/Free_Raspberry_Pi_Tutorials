import RPi.GPIO as GPIO
from time import sleep


dt = 0.1
b1 = 40
b2 = 38
b1State = 1
b1StateOld = 1
b2State = 1
b2StateOld = 1
LEDpin = 37
DC = 99
BP = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setup(b1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(b2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(LEDpin, GPIO.OUT)

myPWM = GPIO.PWM(LEDpin, 200)
myPWM.start(DC)

try:
    while True:
        b1State = GPIO.input(b1)
        b2State = GPIO.input(b2)

        if b1StateOld == 0 and b1State == 1:
            # lin
            #DC = DC - 10
            # exp
            #DC = DC / 2
            # log
            BP = BP - 1
            #DC = 1.5849 ^ BP
            DC = 1.5849 ** BP
            print("Dim event")

        if b2StateOld == 0 and b2State == 1:
            # lin
            #DC = DC + 10
            # exp
            #DC = DC * 2
            # log
            BP = BP + 1
            #DC = 1.5849 ^ BP
            DC = 1.5849 ** BP
            print("Bright event")

        if DC > 99:
            DC = 99

        if DC < 0:
            D = 0

        print(DC)
        myPWM.ChangeDutyCycle(int(DC))
        b1StateOld = b1State
        b2StateOld = b2State
        sleep(dt)

except KeyboardInterrupt:
    myPWM.stop()
    GPIO.cleanup()
    print(" GPIO good to go ")
