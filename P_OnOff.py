#!/usr/bin/env pybricks-micropython

import time
import math
import sys
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

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
    REFLECTION_BLACK = 10
    REFLECTION_WHITE = 70
    STEP_POWER = 50

# --- 3. Σταθερές & Αρχικοποίηση Συσκευών ---
WHEEL_DIAMETER_CM = 5.6

STEP_DURATION_MS = 50 # Διάρκεια κάθε βήματος σε ms


ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
color_sensor = ColorSensor(Port.S1)

def print_battery_info(brick):
    """Prints the battery voltage and current."""
    print("--- Battery Status ---")
    voltage = brick.battery.voltage() / 1000
    current = brick.battery.current() / 1000
    print("Voltage: {:.3f} V".format(voltage))
    print("Current: {:.3f} A\n".format(current))

def stop_robot_safely():
    """Stops the robot and holds the motors."""
    left_motor.stop()
    right_motor.stop()

def line_follow_alternating_steps(distance_cm, power_percent):
    """
    Follows the right edge of a line by moving one wheel at a time
    in sequential 0.1-second steps.

    :param distance_cm: The distance to travel in cm.
    :param power_percent: The power to use for the steps.
    """
    THRESHOLD = (REFLECTION_BLACK + REFLECTION_WHITE) / 2
    
    target_degrees = (distance_cm / (WHEEL_DIAMETER_CM * math.pi)) * 360
    left_motor.reset_angle(0)

    while left_motor.angle() < target_degrees:
        reflection = color_sensor.reflection()

        if reflection < THRESHOLD:
            # Βλέπει μαύρο -> Είναι αριστερά της άκρης -> Στρίψε δεξιά
            # 1. Κίνησε τον αριστερό τροχό μπροστά
            left_motor.dc(power_percent)
            wait(STEP_DURATION_MS)
            left_motor.hold() 
 
       
        else:
            # Βλέπει λευκό -> Είναι δεξιά της άκρης -> Στρίψε αριστερά
            # 1. Κίνησε τον δεξιό τροχό μπροστά
            right_motor.dc(power_percent)
            wait(STEP_DURATION_MS)
            right_motor.hold()
 


    stop_robot_safely()

# --- 4. Κύριο Εκτελέσιμο Μέρος ---
if __name__ == "__main__":
    try:
        if not IN_SIMULATOR:
            print_battery_info(ev3)

        path_type = 'smooth'
        distance_to_run = 200
        if len(sys.argv) > 1 and sys.argv[1].lower() == 'sharp':
            path_type = 'sharp'
            distance_to_run = 50
        
        print("--- Mission Start (Pybricks - 1-Sensor Alternating Steps) ---")
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

    except Exception as e:
        print("\n!!! An error occurred !!!")
        print(e)
        stop_robot_safely()