#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import json
import sys

# Mapping of pumps to their GPIO pins
PUMP_PINS = {
    "Pump 1": {"IA": 17, "IB": 4},
    "Pump 2": {"IA": 22, "IB": 27},
    "Pump 3": {"IA": 10, "IB": 9},
    "Pump 4": {"IA": 5,  "IB": 11},
    "Pump 5": {"IA": 13, "IB": 6},
    "Pump 6": {"IA": 26, "IB": 19},
    "Pump 7": {"IA": 20, "IB": 21},
    "Pump 8": {"IA": 12, "IB": 16},
    "Pump 9": {"IA": 8,  "IB": 7},
    "Pump 10": {"IA": 24, "IB": 25},
    "Pump 11": {"IA": 18, "IB": 23},
    "Pump 12": {"IA": 14, "IB": 15},
}

# Setup GPIO mode and pins
GPIO.setmode(GPIO.BCM)
for pump, pins in PUMP_PINS.items():
    GPIO.setup(pins["IA"], GPIO.OUT)
    GPIO.setup(pins["IB"], GPIO.OUT)
    GPIO.output(pins["IA"], GPIO.LOW)
    GPIO.output(pins["IB"], GPIO.LOW)

def run_pump(pump_name, duration):
    """
    Run a pump by setting its IA pin HIGH and IB pin LOW for the specified duration,
    then stopping it (setting both pins LOW).
    """
    pins = PUMP_PINS[pump_name]
    print(f"Starting {pump_name} (IA: {pins['IA']}, IB: {pins['IB']}) for {duration:.2f} seconds")
    GPIO.output(pins["IA"], GPIO.HIGH)
    GPIO.output(pins["IB"], GPIO.LOW)
    time.sleep(duration)
    GPIO.output(pins["IA"], GPIO.LOW)
    GPIO.output(pins["IB"], GPIO.LOW)
    print(f"Stopped {pump_name}")

def main():
    # Load pump configuration
    try:
        with open("pump_config.json", "r") as f:
            pump_config = json.load(f)
    except Exception as e:
        print("Error reading pump_config.json:", e)
        GPIO.cleanup()
        sys.exit(1)
    
    # Build a mapping from ingredient (lowercase) to pump name
    ingredient_to_pump = {}
    for pump, ingredient in pump_config.items():
        ingredient_to_pump[ingredient.strip().lower()] = pump

    # Load cocktails data
    try:
        with open("cocktails.json", "r") as f:
            cocktails_data = json.load(f)
            cocktails = cocktails_data.get("cocktails", [])
    except Exception as e:
        print("Error reading cocktails.json:", e)
        GPIO.cleanup()
        sys.exit(1)

    # Read the selected cocktail's safe name from file (e.g., "whiskey_sour")
    try:
        with open("selected_cocktail.txt", "r") as f:
            selected_cocktail_safe = f.read().strip()
    except Exception as e:
        print("Error reading selected_cocktail.txt:", e)
        GPIO.cleanup()
        sys.exit(1)

    # Find the cocktail whose normal_name (converted to safe name) matches the selection
    selected_cocktail = None
    for cocktail in cocktails:
        safe_name = cocktail["normal_name"].lower().replace(" ", "_")
        if safe_name == selected_cocktail_safe:
            selected_cocktail = cocktail
            break

    if not selected_cocktail:
        print("Selected cocktail not found in cocktails.json")
        GPIO.cleanup()
        sys.exit(1)
    
    print("Selected cocktail:", selected_cocktail["normal_name"])
    ingredients = selected_cocktail.get("ingredients", {})

    # Conversion factor: seconds per ounce (adjust this constant as needed)
    SECONDS_PER_OZ = 5.0

    # For each ingredient, check if a pump is configured and run it for the computed duration
    for ingredient, measurement in ingredients.items():
        try:
            amount = float(measurement.split()[0])
        except Exception as e:
            print(f"Error parsing measurement for {ingredient}: '{measurement}'", e)
            continue
        
        pump_name = ingredient_to_pump.get(ingredient.strip().lower())
        if not pump_name:
            print(f"No pump configured for ingredient: {ingredient}")
            continue

        run_time = amount * SECONDS_PER_OZ
        print(f"Running pump for {ingredient} ({pump_name}) for {run_time:.2f} seconds")
        run_pump(pump_name, run_time)

    print("Drink complete.")
    GPIO.cleanup()

if __name__ == "__main__":
    main()
