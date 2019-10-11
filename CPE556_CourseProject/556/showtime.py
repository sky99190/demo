import RPi.GPIO as GPIO
import time

LED_A = 31
LED_B = 37
LED_C = 16
LED_D = 36
LED_E = 32
LED_F = 35
LED_G = 18
LED_DP = 22

DIGIT1 = 15
DIGIT2 = 29
DIGIT3 = 33
DIGIT4 = 38

btn = 7

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_A, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)
GPIO.setup(LED_C, GPIO.OUT)
GPIO.setup(LED_D, GPIO.OUT)
GPIO.setup(LED_E, GPIO.OUT)
GPIO.setup(LED_F, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_DP, GPIO.OUT)
GPIO.setup(DIGIT1, GPIO.OUT)
GPIO.setup(DIGIT2, GPIO.OUT)
GPIO.setup(DIGIT3, GPIO.OUT)
GPIO.setup(DIGIT4, GPIO.OUT)

GPIO.output(DIGIT1, False)
GPIO.output(DIGIT2, False)
GPIO.output(DIGIT3, False)
GPIO.output(DIGIT4, False)

GPIO.setup(btn, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def show(no, num, showDotPoint):
    GPIO.output(DIGIT1, True)
    GPIO.output(DIGIT2, True)
    GPIO.output(DIGIT3, True)
    GPIO.output(DIGIT4, True)

    if (num == 0):
        GPIO.output(LED_A, True)
        GPIO.output(LED_B, True)
        GPIO.output(LED_C, True)
        GPIO.output(LED_D, True)
        GPIO.output(LED_E, True)
        GPIO.output(LED_F, True)
        GPIO.output(LED_G, False)
        GPIO.output(LED_DP, not showDotPoint)
    elif (num == 1):
        GPIO.output(LED_A, False)
	GPIO.output(LED_B, True)
	GPIO.output(LED_C, True)
	GPIO.output(LED_D, False)
	GPIO.output(LED_E, False)
	GPIO.output(LED_F, False)
	GPIO.output(LED_G, False)
        GPIO.output(LED_DP, not showDotPoint)
    elif (num == 2):
        GPIO.output(LED_A, True)
	GPIO.output(LED_B, True)
	GPIO.output(LED_C, False)
	GPIO.output(LED_D, True)
	GPIO.output(LED_E, True)
	GPIO.output(LED_F, False)
	GPIO.output(LED_G, True)
        GPIO.output(LED_DP, not showDotPoint)
    elif (num == 3):
        GPIO.output(LED_A, True)
	GPIO.output(LED_B, True)
	GPIO.output(LED_C, True)
	GPIO.output(LED_D, True)
	GPIO.output(LED_E, False)
	GPIO.output(LED_F, False)
	GPIO.output(LED_G, True)
        GPIO.output(LED_DP, not showDotPoint)
    elif (num == 4):
        GPIO.output(LED_A, False)
	GPIO.output(LED_B, True)
	GPIO.output(LED_C, True)
	GPIO.output(LED_D, False)
	GPIO.output(LED_E, False)
	GPIO.output(LED_F, True)
	GPIO.output(LED_G, True)
        GPIO.output(LED_DP, not showDotPoint)
    elif (num == 5):
        GPIO.output(LED_A, True)
	GPIO.output(LED_B, False)
	GPIO.output(LED_C, True)
	GPIO.output(LED_D, True)
	GPIO.output(LED_E, False)
	GPIO.output(LED_F, True)
	GPIO.output(LED_G, True)
        GPIO.output(LED_DP, not showDotPoint)
    elif (num == 6):
        GPIO.output(LED_A, True)
	GPIO.output(LED_B, False)
	GPIO.output(LED_C, True)
	GPIO.output(LED_D, True)
	GPIO.output(LED_E, True)
	GPIO.output(LED_F, True)
	GPIO.output(LED_G, True)
        GPIO.output(LED_DP, not showDotPoint)
    elif (num == 7):
        GPIO.output(LED_A, True)
	GPIO.output(LED_B, True)
	GPIO.output(LED_C, True)
	GPIO.output(LED_D, False)
	GPIO.output(LED_E, False)
	GPIO.output(LED_F, False)
	GPIO.output(LED_G, False)
        GPIO.output(LED_DP, not showDotPoint)
    elif (num == 8):
        GPIO.output(LED_A, True)
	GPIO.output(LED_B, True)
	GPIO.output(LED_C, True)
	GPIO.output(LED_D, True)
	GPIO.output(LED_E, True)
	GPIO.output(LED_F, True)
	GPIO.output(LED_G, True)
        GPIO.output(LED_DP, not showDotPoint)
    elif (num == 9):
        GPIO.output(LED_A, True)
	GPIO.output(LED_B, True)
	GPIO.output(LED_C, True)
	GPIO.output(LED_D, True)
	GPIO.output(LED_E, False)
	GPIO.output(LED_F, True)
	GPIO.output(LED_G, True)
        GPIO.output(LED_DP, not showDotPoint)

    if (no == 1):
        GPIO.output(DIGIT1, False)
    elif (no == 2):
        GPIO.output(DIGIT2, False)
    elif (no == 3):
        GPIO.output(DIGIT3, False)
    elif (no == 4):
        GPIO.output(DIGIT4, False)

try:
    t = 0.001
    while True:
        tm = time.localtime()
        if (GPIO.input(btn) == 1):
            time.sleep(t)
            show(1, tm.tm_hour // 10, True)
            time.sleep(t)
            show(2, tm.tm_hour % 10, False)
            time.sleep(t)
            show(3, tm.tm_min // 10, True)
            time.sleep(t)
            show(4, tm.tm_min % 10, True)
        else:
            time.sleep(t)
            show(1, tm.tm_mon // 10, True)
            time.sleep(t)
            show(2, tm.tm_mon % 10, False)
            time.sleep(t)
            show(3, tm.tm_mday // 10, True)
            time.sleep(t)
            show(4, tm.tm_mday % 10, True)
            
except KeyboardInterrupt:
    pass
                
GPIO.cleanup()