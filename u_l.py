#!/usr/bin/env python3

import time
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.display import Display
from ev3dev2.sound import Sound

# -----------------------------------------------------------------------------
# ΑΡΧΙΚΟΠΟΙΗΣΗ ΣΥΣΚΕΥΩΝ
# -----------------------------------------------------------------------------
# Αρχικοποίηση του αισθητήρα χρώματος
try:
    color_sensor = ColorSensor()
except Exception as e:
    # Εμφάνιση σφάλματος εάν ο αισθητήρας δεν είναι συνδεδεμένος
    display = Display()
    display.text_grid('ERROR: Color Sensor not connected.', x=0, y=4)
    display.update()
    time.sleep(5)
    exit()

# Αρχικοποίηση της οθόνης και του ήχου
display = Display()
sound = Sound()

# -----------------------------------------------------------------------------
# ΚΥΡΙΟ ΠΡΟΓΡΑΜΜΑ
# -----------------------------------------------------------------------------
sound.beep()  # Ειδοποίηση έναρξης

try:
    # Ατέρμονος βρόχος για συνεχή εκτέλεση
    while True:
        # Ανάγνωση της τιμής της ανακλώμενης έντασης φωτός (0-100)
        reflected_light = color_sensor.reflected_light_intensity

        # Δημιουργία του μηνύματος με τη μέθοδο .format() για συμβατότητα
        message = "Reflected: {}".format(reflected_light)
        print(reflected_light)

        # Εμφάνιση του μηνύματος στην οθόνη του EV3
        # Χρησιμοποιείται μεγάλη, ευανάγνωστη γραμματοσειρά (lutBS18)
        display.text_pixels(
            message,
            clear_screen=True,
            x=0,
            y=60,
            font='lutBS18'
        )

        # Ενημέρωση της οθόνης
        display.update()

        # Παύση για 0.5 δευτερόλεπτα
        time.sleep(0.5)

except KeyboardInterrupt:
    # Ομαλός τερματισμός και καθαρισμός της οθόνης
    display.clear()
    display.update()
    print("Program terminated.")