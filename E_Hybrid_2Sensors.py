#!/usr/bin/env python3

import time
import math
import sys
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_1, INPUT_2
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
    # Συντελεστές PID
    KP = 0.6
    KI = 0.01
    KD = 0.4
    REFLECTION_BLACK = 0
    REFLECTION_WHITE = 100
    POWER_MIN = 20  # Ισχύς για τα pivot turns
    POWER_TARGET = 35  # Βασική ισχύς για τον PID
    POWER_MAX = 40
else:
    print("Running on: EV3 Brick\n")
    # --- Εισαγωγή και αρχικοποίηση μόνο για το φυσικό ρομπότ ---
    from ev3dev2.power import PowerSupply

    power_supply = PowerSupply()

    # Συντελεστές PID
    KP = 0.65
    KI = 0.02
    KD = 0.5
    REFLECTION_BLACK = 10
    REFLECTION_WHITE = 70
    POWER_MIN = 30
    POWER_TARGET = 60
    POWER_MAX = 80

# --- 3. Παράγωγοι Παράμετροι & Αρχικοποίηση ---
ERROR_MAX = REFLECTION_WHITE - REFLECTION_BLACK
ERROR_LIMIT = ERROR_MAX * 0.8  # Όριο για την ενεργοποίηση του pivot

WHEEL_DIAMETER_CM = 5.6

sound = Sound()
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
left_motor.stop_action = "hold"
right_motor.stop_action = "hold"
color_sensor_left = ColorSensor(INPUT_1)
color_sensor_right = ColorSensor(INPUT_2)


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


def line_follow_hybrid_2_sensor(distance_cm, motor_power_target, kp, ki, kd):
    """
    Follows a line using a 2-sensor hybrid controller (PID + Pivot Turn).
    """
    target_degrees = (distance_cm / (WHEEL_DIAMETER_CM * math.pi)) * 360

    integral = 0
    last_error = 0

    left_motor.position = 0

    while left_motor.position < target_degrees:
        reflection_left = color_sensor_left.reflected_light_intensity
        reflection_right = color_sensor_right.reflected_light_intensity

        error = reflection_left - reflection_right

        if abs(error) > ERROR_LIMIT:
            # Ζώνη Μεγάλου Σφάλματος -> Ενεργοποίηση Pivot Turn
            integral = 0  # Μηδενισμός του integral για ομαλή μετάβαση
            if error > 0:
                # Πολύ αριστερά -> Στρίψε ΔΕΞΙΑ
                left_speed = POWER_MIN
                right_speed = -POWER_MIN
            else:
                # Πολύ δεξιά -> Στρίψε ΑΡΙΣΤΕΡΑ
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

        left_motor.on(speed=left_speed)
        right_motor.on(speed=right_speed)

        time.sleep(0.01)

    stop_robot_safely()


# --- 4. Κύριο Εκτελέσιμο Μέρος ---
if __name__ == "__main__":
    try:
        if not IN_SIMULATOR:
            print_battery_info(power_supply)

        path_type = "smooth"
        distance_to_run = 200
        if len(sys.argv) > 1 and sys.argv[1].lower() == "sharp":
            path_type = "sharp"
            distance_to_run = 520

        print("--- Mission Start (ev3dev2 - 2-Sensor Hybrid PID) ---")
        print("Path Type: {}. Distance: {} cm".format(path_type, distance_to_run))
        start_time = time.time()

        line_follow_hybrid_2_sensor(
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
        sound.beep()

    except Exception as e:
        print("\n!!! An error occurred !!!")
        print(e)
        stop_robot_safely()
