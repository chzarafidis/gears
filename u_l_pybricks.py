#!/usr/bin/env pybricks-micropython

import time
import sys
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait

# -----------------------------------------------------------------------------
# ΑΡΧΙΚΟΠΟΙΗΣΗ ΣΥΣΚΕΥΩΝ
# -----------------------------------------------------------------------------

# Αρχικοποίηση του EV3 Brick για πρόσβαση σε οθόνη και ηχείο
ev3 = EV3Brick()

# Αρχικοποίηση του αισθητήρα χρώματος στην πόρτα S1
# Σημείωση: Το Pybricks θα εμφανίσει σφάλμα κατά την εκκίνηση
# εάν ο αισθητήρας δεν είναι συνδεδεμένος στη σωστή πόρτα.
color_sensor = ColorSensor(Port.S1)

# -----------------------------------------------------------------------------
# ΚΥΡΙΟ ΠΡΟΓΡΑΜΜΑ
# -----------------------------------------------------------------------------

ev3.speaker.beep()  # Ειδοποίηση έναρξης

try:
    # Ατέρμονος βρόχος για συνεχή εκτέλεση
    while True:
        # Ανάγνωση της τιμής της ανακλώμενης έντασης φωτός (0-100)
        reflected_light = color_sensor.reflection()

        # Καθάρισμα της οθόνης πριν την εμφάνιση της νέας τιμής
        ev3.screen.clear()

        # Δημιουργία του μηνύματος με τη μέθοδο .format()
        message = "Reflected: {}".format(reflected_light)
        
        # Εκτύπωση της τιμής στο τερματικό (π.χ. στο VS Code)
        print(reflected_light)

        # Εμφάνιση του μηνύματος στην οθόνη του EV3
        # Η μέθοδος .print() κεντράρει αυτόματα το κείμενο
        ev3.screen.print(message)

        # Παύση για 0.5 δευτερόλεπτα (500 χιλιοστά του δευτερολέπτου)
        wait(500)

except KeyboardInterrupt:
    # Ομαλός τερματισμός και καθαρισμός της οθόνης
    ev3.screen.clear()
    print("Program terminated.")
