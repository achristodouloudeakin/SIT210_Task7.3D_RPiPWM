import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create and initialise LED
led1 = 14
GPIO.setup(led1, GPIO.OUT)
GPIO.output(led1, GPIO.LOW)

# Create and initialise PWM
pwm = GPIO.PWM(led, 100)
pwm.start(0)


def led_brightness(cycle_amount):
    pwm.ChangeDutyCycle(cycle_amount)
    sleep(0.01)


def message_function(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    message.replace("argonLog", '')

    range_in_centimetres = int(message)

    if(range_in_centimetres > 151):
        led_brightness(0)

    elif(range_in_centimetres > 101 and range_in_centimetres < 150):
        led_brightness(20)

    elif(range_in_centimetres > 51 and range_in_centimetres < 100):
        led_brightness(40)

    elif(range_in_centimetres > 21 and range_in_centimetres < 50):
        led_brightness(60)

    elif(range_in_centimetres > 11 and range_in_centimetres < 20):
        led_brightness(80)

    elif(range_in_centimetres < 10):
        led_brightness(100)


def main():
    try:
        ourClient = mqtt.Client("makerio_mqtt")
        ourClient.connect("test.mosquitto.org", 1883)
        ourClient.subscribe("photonLog")
        ourClient.on_message = message_function
        ourClient.loop_start()

        while(1):
            time.sleep(0.3)

    except:
        KeyboardInterrupt()


main()
