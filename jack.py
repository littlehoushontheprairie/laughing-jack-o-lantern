# Import the modules used in the script
import random, time, os
import RPi.GPIO as GPIO

# Assign the hardware PWM pin and name it
led = 18
button = 23
RUNNING = True
SOUND = False
strength = 9

# Configure the GPIO to BCM and set it to output mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set PWM
pwm = GPIO.PWM(led, 100)

print "Flickering LED. Press CTRL + C to quit"

# Main loop
try:
    while RUNNING:
        input_state = GPIO.input(button)

        if input_state == False:
            start = time.time()
            input_state = True
            SOUND = False

            while time.time() - start < 17:
                # Start PWM with the LED off
                pwm.start(0)
                # Randomly change the brightness of the LED
                pwm.ChangeDutyCycle(random.randint(5, 100))
                # Randomly pause on a brightness to simulate flickering
                time.sleep(random.random() / strength)
       
                if SOUND != True and ( time.time() - start > 1.5 ): 
                    SOUND = True
                    os.system('omxplayer /home/pi/laugh.mp3 &')
        

# If CTRL+C is pressed the main loop is broken
except KeyboardInterrupt:
    RUNNING = False
    print "\Quitting"
                   
# Actions under 'finally' will always be called
finally:
    # Stop and finish cleanly so the pins
    # are available to be used again
    pwm.stop()
    GPIO.cleanup()
