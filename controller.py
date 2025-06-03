# controller.py

DEBUG = True  # Toggle debug mode on/off
             # If True, no GPIO access, only prints what's happening.

if not DEBUG:
    import RPi.GPIO as GPIO
import time
import os
import json

# Define GPIO pins for each motor here (same as your test).
# Adjust these if needed to match your hardware.
MOTORS = [
    (17, 4),   # Pump 1
    (22, 27),  # Pump 2
    (9, 10),   # Pump 3
    (5, 11),   # Pump 4
    (13, 6),   # Pump 5
    (26, 19),  # Pump 6
    (20, 21),  # Pump 7
    (14, 15),  # Pump 8
    (23, 18),  # Pump 9
    (25, 23),  # Pump 10
    (7, 8),    # Pump 11
    (16, 12),  # Pump 12
]


def setup_gpio():
    """Set up all motor pins for OUTPUT."""
    if DEBUG:
        print("DEBUG: setup_gpio() called — Not actually initializing GPIO pins.")
    else:
        GPIO.setmode(GPIO.BCM)
        for ia, ib in MOTORS:
            GPIO.setup(ia, GPIO.OUT)
            GPIO.setup(ib, GPIO.OUT)

def motor_forward(ia, ib):
    """Drive motor forward."""
    if DEBUG:
        print(f"DEBUG: motor_forward(ia={ia}, ib={ib}) called — No actual motor movement.")
    else:
        GPIO.output(ia, GPIO.HIGH)
        GPIO.output(ib, GPIO.LOW)

def motor_stop(ia, ib):
    """Stop motor."""
    if DEBUG:
        print(f"DEBUG: motor_stop(ia={ia}, ib={ib}) called — No actual motor movement.")
    else:
        GPIO.output(ia, GPIO.LOW)
        GPIO.output(ib, GPIO.LOW)
def motor_reverse(ia,ib):
    if DEBUG:
        print("Debug reverse")
    else:
        GPIO.output(ia,GPIO.LOW)
        GPIO.output(ib,GPIO.HIGH)

def prime_pumps(duration):
    """
    Primes each pump for `duration` seconds in sequence (one after another).
    """
    setup_gpio()
    try:
        for index, (ia, ib) in enumerate(MOTORS, start=1):
            print(f"Priming pump {index} for {duration} seconds...")
            motor_forward(ia, ib)
            time.sleep(duration)
            motor_stop(ia, ib)
    finally:
        if not DEBUG:
            GPIO.cleanup()
        else:
            print("DEBUG: prime_pumps() complete — no GPIO cleanup in debug mode.")


def clean_pumps(duration=10):
    """
    Reverse each pump for `duration` seconds (one after another),
    e.g. for cleaning lines.
    """
    setup_gpio()
    try:
        for index, (ia, ib) in enumerate(MOTORS, start=1):
            print(f"Reversing pump {index} for {duration} seconds (cleaning)...")
            motor_reverse(ia, ib)
            time.sleep(duration)
            motor_stop(ia, ib)
    finally:
        if not DEBUG:
            GPIO.cleanup()
        else:
            print("DEBUG: clean_pumps() complete no GPIO cleanup in debug mode.")

def make_drink(pump_config_path, recipe, single_or_double="single"):
    """
    Prepare a drink using the hardware pumps, based on:
      1) pump_config.json (mapping from Pump # -> ingredient name)
      2) a `recipe` dict from cocktails.json (with "ingredients": {...})
      3) single_or_double parameter (either "single" or "double").

    In debug mode, only prints messages instead of driving motors.
    """
    # 1) Load the pump config dictionary, e.g. {"Pump 1": "vodka", "Pump 2": "gin", ...}
    if not os.path.exists(pump_config_path):
        print(f"pump_config file not found: {pump_config_path}")
        return

    try:
        with open(pump_config_path, "r") as f:
            pump_config = json.load(f)
    except Exception as e:
        print(f"Error reading {pump_config_path}: {e}")
        return

    # 2) Extract the recipe's ingredients
    ingredients = recipe.get("ingredients", {})
    if not ingredients:
        print("No ingredients found in recipe.")
        return

    # 3) Single or double factor
    factor = 2 if single_or_double.lower() == "double" else 1

    # 4) Get the 1oz coefficient (seconds per ounce) from environment or default to 8
    try:
        oz_coefficient = float(os.getenv("ONE_OZ_COEFFICIENT", "8"))
    except ValueError:
        oz_coefficient = 8.0

    setup_gpio()
    try:
        for ingredient_name, measurement_str in ingredients.items():
            parts = measurement_str.split()
            if not parts:
                print(f"Cannot parse measurement for {ingredient_name}. Skipping.")
                continue
            try:
                oz_amount = float(parts[0])  # parse numeric
            except ValueError:
                print(f"Cannot parse numeric amount '{parts[0]}' for {ingredient_name}. Skipping.")
                continue

            oz_needed = oz_amount * factor

            # find a matching pump label in pump_config
            chosen_pump = None
            for pump_label, config_ing_name in pump_config.items():
                if config_ing_name.strip().lower() == ingredient_name.strip().lower():
                    chosen_pump = pump_label
                    break

            if not chosen_pump:
                print(f"No pump mapped to ingredient '{ingredient_name}'. Skipping.")
                continue

            # parse 'Pump 1' -> index=0
            try:
                pump_num_str = chosen_pump.replace("Pump", "").strip()
                pump_index = int(pump_num_str) - 1
            except ValueError:
                print(f"Could not parse pump label '{chosen_pump}'. Skipping.")
                continue

            if pump_index < 0 or pump_index >= len(MOTORS):
                print(f"Pump index {pump_index} out of range for '{ingredient_name}'. Skipping.")
                continue

            ia, ib = MOTORS[pump_index]
            seconds_to_pour = oz_needed * oz_coefficient

            print(f"Pouring {oz_needed} oz of {ingredient_name} via {chosen_pump} for {seconds_to_pour:.2f} seconds.")
            motor_forward(ia, ib)
            time.sleep(seconds_to_pour)
            motor_stop(ia, ib)

        print("Finished making the drink!")
    finally:
        if not DEBUG:
            GPIO.cleanup()
        else:
            print("DEBUG: make_drink() complete — no GPIO cleanup in debug mode.")
