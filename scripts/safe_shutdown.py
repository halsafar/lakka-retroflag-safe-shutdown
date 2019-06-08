import os
from multiprocessing import Process
import sys
import time

sys.path.append('./lib')
import RPi.GPIO as GPIO


# initialize pins
PIN_POWER = 3  # pin 5
PIN_LED = 14  # TXD
PIN_RESET = 2  # pin 13

# powerenPin = 4  # pin 5


def init():
    """
    initialize gpio
    :return:
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_POWER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_LED, GPIO.OUT)
    # GPIO.setup(powerenPin, GPIO.OUT)
    # GPIO.output(powerenPin, GPIO.HIGH)
    GPIO.setwarnings(False)


def poweroff():
    """
    Waits for user to hold power button up to 1 second before issuing poweroff command
    :return:
    """
    while True:
        GPIO.wait_for_edge(PIN_POWER, GPIO.FALLING)
        os.system("systemctl stop retroarch")
        os.system("shutdown -h now")


def led_blink():
    """
    Blinks the LED to signal button being pushed
    :return:
    """
    while True:
        GPIO.output(PIN_LED, GPIO.HIGH)
        GPIO.wait_for_edge(PIN_POWER, GPIO.FALLING)
        while GPIO.input(PIN_POWER) == GPIO.LOW:
            GPIO.output(PIN_LED, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(PIN_LED, GPIO.HIGH)
            time.sleep(0.2)


def reset():
    """
    Resets the pi
    :return:
    """
    while True:
        GPIO.wait_for_edge(PIN_RESET, GPIO.FALLING)
        os.system("systemctl stop retroarch")
        os.system("systemctl start retroarch")


def main():
    """
    Entry Point
    :return:
    """
    init()

    # create a multiprocessing.Process instance for each function to enable parallelism
    power_process = Process(target=poweroff)
    power_process.start()

    led_process = Process(target=led_blink)
    led_process.start()

    reset_process = Process(target=reset)
    reset_process.start()

    power_process.join()
    led_process.join()
    reset_process.join()

    GPIO.cleanup()


if __name__ == "__main__":
    main()
