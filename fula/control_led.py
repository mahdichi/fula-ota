# control_led.py
import RPi.GPIO as GPIO
import time
import argparse
import logging

led_r_pin=24
led_b_pin=16
led_g_pin=12

#setup logging
logging.basicConfig(filename='/home/pi/fula.sh.log', filemode='a', level=logging.INFO, format='%(asctime)s %(message)s')

#setup LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(led_r_pin, GPIO.OUT)
GPIO.setup(led_b_pin, GPIO.OUT)
GPIO.setup(led_g_pin, GPIO.OUT)

# LEDs are active low. So, set high for turning off
GPIO.output(led_r_pin, GPIO.HIGH)
GPIO.output(led_g_pin, GPIO.HIGH)
GPIO.output(led_b_pin, GPIO.HIGH)

logging.info('All LEDs were turned off initially.')

# Create a parser for command line arguments
parser = argparse.ArgumentParser(description='Control LEDs.')
parser.add_argument('color', type=str, help='LED color (red, green, or blue).')
parser.add_argument('time', type=int, help='Time to flash the LED.')

args = parser.parse_args()
logging.info(f'{args.color} and {args.time} was received.')

led_pin = {"red": led_r_pin, "green": led_g_pin, "blue": led_b_pin}.get(args.color)

# Calculate the end time for 10 minutes in the future
end_time = time.time() + 10 * 60

try:
    # if time is -1, stop all flashing by setting all to 1
    if args.time == -1:
        GPIO.output(led_r_pin, GPIO.HIGH)
        GPIO.output(led_g_pin, GPIO.HIGH)
        GPIO.output(led_b_pin, GPIO.HIGH)
        logging.info('All LEDs were turned off by -1.')
    else:
        # flash the LED
        while True:
            if time.time() > end_time:
                # More than 10 minutes have passed
                logging.info('10 minutes have passed. All LEDs were turned off.')
                break
            
            GPIO.output(led_pin, GPIO.LOW)
            logging.info(f'{args.color} LED was turned on.')
            time.sleep(1)
            GPIO.output(led_pin, GPIO.HIGH)
            logging.info(f'{args.color} LED was turned off.')
            time.sleep(1)
            
            if args.time > 0:
                args.time -= 1
            elif args.time == 0:
                continue
            else:
                break

except KeyboardInterrupt:
    # Handle the Ctrl-C case to ensure we cleanup GPIO settings
    logging.info('Interrupted by user.')
    
finally:
    # This block will run no matter how the try block was exited.
    GPIO.output(led_r_pin, GPIO.HIGH)
    GPIO.output(led_g_pin, GPIO.HIGH)
    GPIO.output(led_b_pin, GPIO.HIGH)
    logging.info('All LEDs were turned off in finally.')
    GPIO.cleanup()
