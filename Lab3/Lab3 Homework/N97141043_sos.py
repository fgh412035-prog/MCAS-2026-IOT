import time

import RPi.GPIO as GPIO

LED_PIN = 29      # BCM GPIO17, physical pin 11
BUZZER_PIN = 7    # BCM GPIO5, physical pin 29
UNIT = 0.2        # One Morse time unit in seconds
FREQUENCY = 523   # For a passive buzzer

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)

buzzer = GPIO.PWM(BUZZER_PIN, FREQUENCY)
message = ("...", "---", "...")

try:
    while True:
        for letter in message:
            for index, signal in enumerate(letter):
                duration = UNIT if signal == "." else UNIT * 3
                GPIO.output(LED_PIN, GPIO.HIGH)
                buzzer.start(50)
                time.sleep(duration)
                buzzer.stop()
                GPIO.output(LED_PIN, GPIO.LOW)

                if index < len(letter) - 1:
                    time.sleep(UNIT)

            time.sleep(UNIT * 3)

        time.sleep(UNIT * 4)
except KeyboardInterrupt:
    pass
finally:
    buzzer.stop()
    GPIO.cleanup()