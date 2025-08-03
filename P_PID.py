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

# --- 2. Δυναμικές Παράμετροι PID ανά Περιβάλλον ---
if IN_SIMULATOR:
    print("Running in: GearsBot Simulator\n")
    # Συντελεστές PID για τον προσομοιωτή
    KP = 1  # Proportional gain
    KI = 0.01 # Integral gain
    KD = 1.5  # Derivative gain
    REFLECTION_BLACK = 0
    REFLECTION_WHITE = 100
    POWER_MIN = 20
    POWER_TARGET = 40
    POWER_MAX = 50
else:
    print("Running on: EV3 Brick\n")
    # Συντελεστές PID για το φυσικό ρομπότ (χρειάζονται ρύθμιση)
    KP = 2.5
    KI = 0.02
    KD = 2.0
    REFLECTION_BLACK = 10
    REFLECTION_WHITE = 70
    POWER_MIN = 30
    POWER_TARGET = 50
    POWER_MAX = 70

# --- 3. Σταθερές & Αρχικοποίηση Συσκευών ---
WHEEL_DIAMETER_CM = 5.6

ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
# Αρχικοποίηση ΕΝΟΣ αισθητήρα χρώματος στην πόρτα S1
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

def line_follow_pid_controller(distance_cm, motor_power_target, kp, ki, kd):
    """
    Follows the right edge of a line using a PID controller.

    :param distance_cm: The distance to travel in cm.
    :param motor_power_target: The base power for the motors.
    :param kp: The proportional gain.
    :param ki: The integral gain.
    :param kd: The derivative gain.
    """
    TARGET_VALUE = (REFLECTION_BLACK + REFLECTION_WHITE) / 2
    target_degrees = (distance_cm / (WHEEL_DIAMETER_CM * math.pi)) * 360
    
    # Αρχικοποίηση μεταβλητών PID
    integral = 0
    last_error = 0

    left_motor.reset_angle(0)

    while left_motor.angle() < target_degrees:
        reflection = color_sensor.reflection()
        
        # Υπολογισμός όρων PID
        error = TARGET_VALUE - reflection
        integral = integral + error
        derivative = error - last_error
        
        # Η διόρθωση είναι ο συνδυασμός των τριών όρων
        turn_power = (kp * error) + (ki * integral) + (kd * derivative)
        
        # Ενημέρωση του last_error για την επόμενη επανάληψη
        last_error = error
        
        # Εφαρμογή της διόρθωσης στις ταχύτητες των κινητήρων
        left_speed = motor_power_target + turn_power
        right_speed = motor_power_target - turn_power

        # Clamping (Περιορισμός των τιμών εντός έγκυρου εύρους)
        if left_speed > POWER_MAX: left_speed = POWER_MAX
        elif left_speed < -POWER_MIN: left_speed = -POWER_MIN
        if right_speed > POWER_MAX: right_speed = POWER_MAX
        elif right_speed < -POWER_MIN: right_speed = -POWER_MIN

        left_motor.dc(left_speed)
        right_motor.dc(right_speed)
        
        wait(10)

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
            distance_to_run = 520
        
        print("--- Mission Start (Pybricks - 1-Sensor PID-Controller) ---")
        print("Path Type: {}. Distance: {} cm".format(path_type, distance_to_run))
        start_time = time.time()
        
        line_follow_pid_controller(
            distance_cm=distance_to_run, 
            motor_power_target=POWER_TARGET, 
            kp=KP,
            ki=KI,
            kd=KD
        )
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("\n--- Mission Complete ---")
        print("Total time: {:.3f} seconds.".format(elapsed_time))

    except Exception as e:
        print("\n!!! An error occurred !!!")
        print(e)
        stop_robot_safely()
