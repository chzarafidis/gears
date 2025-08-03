#!/usr/bin/env python3

import time
import math
import sys
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
# Η PowerSupply θα εισαχθεί μόνο αν χρειαστεί

# --- 1. Ανίχνευση Περιβάλλοντος Εκτέλεσης ---
if sys.version_info[0] == 3 and sys.version_info[1] > 5:
    IN_SIMULATOR = True
else:
    IN_SIMULATOR = False

print("Python version:", sys.version)

# --- 2. Δυναμικές Παράμετροι ανά Περιβάλλον ---
if IN_SIMULATOR:
    print("Running in: GearsBot Simulator\n")
    REFLECTION_BLACK = 0
    REFLECTION_WHITE = 100
    # Μία σταθερή ισχύς για τις βηματικές κινήσεις
    STEP_POWER = 40
else:
    print("Running on: EV3 Brick\n")
    # Εισαγωγή και αρχικοποίηση μόνο για το φυσικό ρομπότ
    from ev3dev2.power import PowerSupply
    power_supply = PowerSupply()
    
    REFLECTION_BLACK = 10
    REFLECTION_WHITE = 70
    STEP_POWER = 50

# --- 3. Σταθερές & Αρχικοποίηση Συσκευών ---
WHEEL_DIAMETER_CM = 5.6
STEP_DURATION_S = 0.05 # Διάρκεια κάθε βήματος σε δευτερόλεπτα

sound = Sound()
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
left_motor.stop_action = 'hold'
right_motor.stop_action = 'hold'
color_sensor = ColorSensor(INPUT_1)

def print_battery_info(power):
    """Prints the battery voltage and current."""
    print("--- Battery Status ---")
    voltage = power.measured_volts
    current = power.measured_amps
    print("Voltage: {:.3f} V".format(voltage))
    print("Current: {:.3f} A\n".format(current))

def stop_robot_safely():
    """Stops the robot by turning off each motor individually."""
    left_motor.off()
    right_motor.off()

def line_follow_alternating_steps(distance_cm, power_percent):
    """
    Follows the right edge of a line by moving one wheel at a time
    in sequential steps.

    :param distance_cm: The distance to travel in cm.
    :param power_percent: The power to use for the steps.
    """
    THRESHOLD = (REFLECTION_BLACK + REFLECTION_WHITE) / 2
    
    target_degrees = (distance_cm / (WHEEL_DIAMETER_CM * math.pi)) * 360
    left_motor.position = 0

    while left_motor.position < target_degrees:
        reflection = color_sensor.reflected_light_intensity

        if reflection < THRESHOLD:
            # Βλέπει μαύρο -> Είναι αριστερά της άκρης -> Στρίψε δεξιά
            # 1. Κίνησε τον αριστερό τροχό μπροστά
            left_motor.on(speed=power_percent)
            time.sleep(STEP_DURATION_S)
            left_motor.stop() 
        
        else:
            # Βλέπει λευκό -> Είναι δεξιά της άκρης -> Στρίψε αριστερά
            # 1. Κίνησε τον δεξιό τροχό μπροστά
            right_motor.on(speed=power_percent)
            time.sleep(STEP_DURATION_S)
            right_motor.stop()

    stop_robot_safely()

# --- 4. Κύριο Εκτελέσιμο Μέρος ---
if __name__ == "__main__":
    try:
        if not IN_SIMULATOR:
            print_battery_info(power_supply)

        path_type = 'smooth'
        distance_to_run = 200
        if len(sys.argv) > 1 and sys.argv[1].lower() == 'sharp':
            path_type = 'sharp'
            distance_to_run = 50
        
        print("--- Mission Start (ev3dev2 - 1-Sensor Alternating Steps) ---")
        print("Path Type: {}. Distance: {} cm".format(path_type, distance_to_run))
        start_time = time.time()
        
        # Εκτέλεση της αποστολής
        line_follow_alternating_steps(
            distance_cm=distance_to_run,
            power_percent=STEP_POWER
        )

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("\n--- Mission Complete ---")
        print("Total time: {:.3f} seconds.".format(elapsed_time))
        sound.beep()

    except Exception as e:
        print("\n!!! An error occurred !!!")
        print(e)
        stop_robot_safely()
