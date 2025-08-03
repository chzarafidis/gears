#!/usr/bin/env pybricks-micropython

import time
import math
import sys
#from pybricks  import EV3Brick
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
    # Συντελεστές PID
    KP = 2.4  # Proportional gain
    KI = 0.02  # Integral gain
    KD = 2  # Derivative gain

    REFLECTION_BLACK = 0
    REFLECTION_WHITE = 100
    POWER_MIN = 15  # Ισχύς για τα pivot turns
    POWER_TARGET = 35  # Βασική ισχύς για τον PID
    POWER_MAX = 40
else:
    print("Running on: EV3 Brick\n")
    # Συντελεστές PID
    KP = 2.5
    KI = 0.02
    KD = 2.0

    REFLECTION_BLACK = 10
    REFLECTION_WHITE = 70
    POWER_MIN = 25
    POWER_TARGET = 40
    POWER_MAX = 60

# --- 3. Σταθερές & Αρχικοποίηση Συσκευών ---
WHEEL_DIAMETER_CM = 5.6

#ev3 = EV3Brick()
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
    """Stops the robot  the motors."""
    left_motor.stop()
    right_motor.stop()


def line_follow_hybrid_for_distance(distance_cm, motor_power_target, kp, ki, kd):
    """
    Follows a line using a hybrid controller:
    - PID for small errors.
    - Pivot turns for large errors.
    """
    TARGET_VALUE = (REFLECTION_BLACK + REFLECTION_WHITE) / 2
    ERROR_LIMIT = (
        TARGET_VALUE - REFLECTION_BLACK
    ) / 2  # Όριο για την ενεργοποίηση του pivot

    target_degrees = (distance_cm / (WHEEL_DIAMETER_CM * math.pi)) * 360

    integral = 0
    last_error = 0

    left_motor.reset_angle(0)

    while left_motor.angle() < target_degrees:
        reflection = color_sensor.reflection()
        error = TARGET_VALUE - reflection

        if abs(error) > ERROR_LIMIT:
            # Ζώνη Μεγάλου Σφάλματος -> Ενεργοποίηση Pivot Turn
            # Μηδενισμός του integral για να μην επηρεάσει την επόμενη κίνηση
            integral = 0
            if error > 0:
                # Σφάλμα θετικό (στο μαύρο) -> στροφή δεξιά
                left_speed = POWER_MIN
                right_speed = -POWER_MIN
            else:
                # Σφάλμα αρνητικό (στο λευκό) -> στροφή αριστερά
                left_speed = -POWER_MIN
                right_speed = POWER_MIN
        else:
            # Ζώνη Μικρού Σφάλματος -> Ενεργοποίηση PID
            integral += error
            derivative = error - last_error
            turn_power = (kp * error) + (ki * integral) + (kd * derivative)

            left_speed = motor_power_target + turn_power
            right_speed = motor_power_target - turn_power

        last_error = error

        # Clamping
        if left_speed > POWER_MAX:
            left_speed = POWER_MAX
        elif left_speed < -POWER_MIN:
            left_speed = -POWER_MIN
        if right_speed > POWER_MAX:
            right_speed = POWER_MAX
        elif right_speed < -POWER_MIN:
            right_speed = -POWER_MIN

        left_motor.dc(left_speed)
        right_motor.dc(right_speed)

        wait(10)

    stop_robot_safely()


# --- 4. Κύριο Εκτελέσιμο Μέρος ---
if __name__ == "__main__":
    try:
        if not IN_SIMULATOR:
            pass
            #print_battery_info(ev3)

        path_type = "smooth"
        distance_to_run = 200
        if len(sys.argv) > 1 and sys.argv[1].lower() == "sharp":
            path_type = "sharp"
            distance_to_run = 520

        print("--- Mission Start (Pybricks - 1-Sensor Hybrid PID) ---")
        print("Path Type: {}. Distance: {} cm".format(path_type, distance_to_run))
        start_time = time.time()

        line_follow_hybrid_for_distance(
            distance_cm=distance_to_run,
            motor_power_target=POWER_TARGET,
            kp=KP,
            ki=KI,
            kd=KD,
        )

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("\n--- Mission Complete ---")
        print("Total time: {:.3f} seconds.".format(elapsed_time))

    except Exception as e:
        print("\n!!! An error occurred !!!")
        print(e)
        stop_robot_safely()
