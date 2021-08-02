from datetime import datetime
import schedule
import RPi.GPIO as GPIO
import time
led_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)  # Set GPIO led pin to output mode.

pwm = GPIO.PWM(led_pin, 100)   # Initialize PWM on pwmPin 100Hz frequency
dc=0                               # set dc variable to 0 for 0%
pwm.start(dc)

interval = 5                      # how much to dim
time_delay = 30                   # how often to dim by interval in seconds
#interval of 5 and time_delay of 30 seconds will take dc from 0 to 100 in 10 minutes

def turn_on():
    pwm.ChangeDutyCycle(100)

def turn_off():
    pwm.ChangeDutyCycle(0)
    
def dim_on(): 
    value = 5
    while value != 100:
        pwm.ChangeDutyCycle(value)
        value += interval
        time.sleep(time_delay)
    
def dim_off(): 
    value = 95
    while value != 0:
        pwm.ChangeDutyCycle(value)
        value -= interval
        time.sleep(time_delay)

def clean_up():
    pwm.stop()                         # stop PWM
    GPIO.cleanup()

try:
    now = datetime.now()

    if now.hour >= 6 and now.hour <= 20:
        turn_on()
    else:
        turn_off()
    
    schedule.every().day.at("06:00").do(dim_on())
    schedule.every().day.at("21:00").do(dim_off())
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        
except Exception as e:
    print(e.message, e.args)
finally:
    clean_up()