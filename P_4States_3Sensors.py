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
    POWER_MIN    = 20
    POWER_TARGET = 35
    POWER_MAX    = 40
else:
    print("Running on: EV3 Brick\n")
    REFLECTION_BLACK = 10
    REFLECTION_WHITE = 70
    POWER_MIN    = 30
    POWER_TARGET = 60
    POWER_MAX    = 80

# --- 3. Σταθερές & Αρχικοποίηση Συσκευών ---
WHEEL_DIAMETER_CM = 5.6
THRESHOLD = (REFLECTION_BLACK + REFLECTION_WHITE) / 2

ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
# Διάταξη 3 αισθητήρων σύμφωνα με τις οδηγίες
color_sensor_left = ColorSensor(Port.S1)
color_sensor_right = ColorSensor(Port.S2)
color_sensor_center = ColorSensor(Port.S3)

def print_battery_info(brick):
    """
    Prints the battery voltage and current.
    """
    print("--- Battery Status ---")
    voltage = brick.battery.voltage() / 1000
    current = brick.battery.current() / 1000
    print("Voltage: {:.3f} V".format(voltage))
    print("Current: {:.3f} A\n".format(current))

def stop_robot_safely():
    """Stops the robot and holds the motors."""
    left_motor.hold()
    right_motor.hold()

def line_follow_for_distance(distance_cm):
    """
    Follows a line for a distance using a 3-sensor, 4-state controller.
    """
    target_degrees = (distance_cm / (WHEEL_DIAMETER_CM * math.pi)) * 360
    left_motor.reset_angle(0)

    while left_motor.angle() < target_degrees:
        # Ανάγνωση τιμών από τους 3 αισθητήρες
        on_left = color_sensor_left.reflection() < THRESHOLD
        on_right = color_sensor_right.reflection() < THRESHOLD
        on_center = color_sensor_center.reflection() < THRESHOLD
        
                
        left_speed = POWER_TARGET
        right_speed = POWER_TARGET

        # Βελτιωμένη Λογική 4 Καταστάσεων
        if on_right:
            # Κατάσταση 1: Απόκλιση αριστερά -> Στρίψε ΔΕΞΙΑ
            left_speed = POWER_MIN
            right_speed = -POWER_MIN
        elif on_left:
            # Κατάσταση 2: Απόκλιση δεξιά -> Στρίψε ΑΡΙΣΤΕΡΑ
            left_speed = -POWER_MIN
            right_speed = POWER_MIN
        elif on_center:
            # Κατάσταση 3: Στην πορεία -> Κινήσου ευθεία
            left_speed = POWER_TARGET
            right_speed = POWER_TARGET
        else:
            # Κατάσταση 4: Εκτός γραμμής -> Διατήρησε την κατεύθυνση
            pass

        left_motor.dc(left_speed)
        right_motor.dc(right_speed)
        
        wait(1)

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
            distance_to_run = 550
        
        print("--- Mission Start (Pybricks - 3-Sensor 4-State) ---")
        print("Path Type: {}. Distance: {} cm".format(path_type, distance_to_run))
        start_time = time.time()
        
        line_follow_for_distance(distance_cm=distance_to_run)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("\n--- Mission Complete ---")
        print("Total time: {:.3f} seconds.".format(elapsed_time))

    except Exception as e:
        print("\n!!! An error occurred !!!")
        print(e)
        stop_robot_safely()
