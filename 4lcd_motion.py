from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time
import datetime
import sys

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up the motion sensor pin
motion_sensor_pin = 18  # Change this to the appropriate pin
GPIO.setup(motion_sensor_pin, GPIO.IN)

# Set up the LCD
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=4)

# Clear the LCD display
lcd.clear()

def update_lcd(line1, line2, line3, line4):
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1)
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2)
    lcd.cursor_pos = (2, 0)
    lcd.write_string(line3)
    lcd.cursor_pos = (3, 0)
    lcd.write_string(line4)

def get_current_date_time():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    return current_date, current_time

def exit_program():
    lcd.clear()  # Clear the LCD display
    lcd.write_string("Exiting...")  # Display "Exiting" message

    # Fade in and turn on the backlight
    for brightness in range(0, 101, 10):
        lcd.backlight_enabled = True
        lcd.backlight_pwm = brightness
        time.sleep(0.2)  # Delay for fade-in effect

    lcd.clear()  # Clear the LCD display
    lcd.backlight_enabled = False  # Turn off the backlight
    GPIO.cleanup()  # Clean up GPIO pins
    sys.exit()  # Terminate the program

# Keep the message displayed and handle KeyboardInterrupt
try:
    while True:
        motion_detected = GPIO.input(motion_sensor_pin)
        current_date, current_time = get_current_date_time()

        if motion_detected:
            update_lcd("Motion Detected", "Date: " + current_date, "Time: " + current_time, "")
            print("Motion detected at", current_time)
        else:
            update_lcd("No Motion", "Date: " + current_date, "Time: " + current_time, "")
            print("No motion detected at", current_time)

        time.sleep(0.5)  # Delay between readings
except KeyboardInterrupt:
    exit_program()
