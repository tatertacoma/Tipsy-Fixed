import os
import json
import base64
import requests
import streamlit as st
from dotenv import load_dotenv, set_key
import assist
from rembg import remove
from PIL import Image

# Import your controller module
try:
    import controller
except ModuleNotFoundError:
    print('Controller modules not found. Pump control will be disabled for WebUI')

# Load .env variables
load_dotenv()

# ---------- API KEY SETUP ----------
if not os.getenv("OPENAI_API_KEY") and "openai_api_key" not in st.session_state:
    st.title("Enter OpenAI API Key")
    key_input = st.text_input("OpenAI API Key", type="password")
    if st.button("Submit"):
        st.session_state["openai_api_key"] = key_input
        set_key(".env", "OPENAI_API_KEY", key_input)
        st.rerun()
    st.stop()

# Motor Calibration
if not os.getenv("OZ_CALIBRATION"):
    st.title("Enter Motor Calibration")
    key_input = st.number_input("Seconds for 1oz of Liquid (Leave default if not yet known)", value=8)
    if st.button("Submit"):
        set_key(".env", "OZ_CALIBRATION", str(key_input))
        st.rerun()
    st.stop()

# ---------- Global Setup ----------
CONFIG_FILE = "pump_config.json"
COCKTAILS_FILE = "cocktails.json"
LOGO_FOLDER = "drink_logos"

if not os.path.exists(LOGO_FOLDER):
    os.makedirs(LOGO_FOLDER)

# We'll just keep track in session state if we show the gallery or the detail page
if "selected_cocktail" not in st.session_state:
    st.session_state.selected_cocktail = None

# ---------- Helper Functions ----------
def load_saved_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading configuration: {e}")
    return {}

def save_config(data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving configuration: {e}")

def load_cocktails():
    if os.path.exists(COCKTAILS_FILE):
        try:
            with open(COCKTAILS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading cocktails: {e}")
    return {}

def save_cocktails(data):
    try:
        with open(COCKTAILS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving cocktails: {e}")

def get_safe_name(name):
    """Convert a cocktail name to a safe filename-friendly string."""
    return name.lower().replace(" ", "_")

# ---------- Tabs ----------
tabs = st.tabs(["My Bar", "Settings", "Cocktail Menu"])

# ================ TAB 1: My Bar ================
with tabs[0]:
    st.markdown("<h1 style='text-align: center;'>My Bar</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Enter the drink names for each pump:</p>", unsafe_allow_html=True)
    
    saved_config = load_saved_config()
    pump_inputs = {}

    col1, col2 = st.columns(2)

    def get_default(pump_name):
        """Helper to retrieve default or saved value for each pump."""
        if pump_name in saved_config:
            return saved_config[pump_name]
        elif pump_name == "Pump 1":
            return "vodka"
        else:
            return ""

    # Pump naming: 1-6 in first column, 7-12 in second column
    with col1:
        for i in range(1, 7):
            pump_name = f"Pump {i}"
            pump_inputs[pump_name] = st.text_input(
                label=pump_name,
                value=get_default(pump_name)
            )

    with col2:
        for i in range(7, 13):
            pump_name = f"Pump {i}"
            pump_inputs[pump_name] = st.text_input(
                label=pump_name,
                value=get_default(pump_name)
            )

    st.markdown("<h3 style='text-align: center;'>Requests for the bartender</h3>", unsafe_allow_html=True)
    bartender_requests = st.text_area("Enter any special requests for the bartender", height=100)

    if st.button("Generate Recipes"):
        pump_to_drink = {pump: drink for pump, drink in pump_inputs.items() if drink.strip()}
        # Save the pump configuration to JSON
        save_config(pump_to_drink)

        st.markdown(f"<p style='text-align: center;'>Pump configuration: {pump_to_drink}</p>", unsafe_allow_html=True)
        
        # Ask AI to generate cocktails from these pumps + bartender requests
        cocktails_json = assist.generate_cocktails(pump_to_drink, bartender_requests)
        save_cocktails(cocktails_json)
        
        st.markdown("<h2 style='text-align: center;'>Generating Cocktail Logos...</h2>", unsafe_allow_html=True)
        image_paths = {}
        cocktails = cocktails_json.get("cocktails", [])
        total = len(cocktails) if cocktails else 1
        progress_bar = st.progress(0, text="Generating images...")

        for idx, cocktail in enumerate(cocktails):
            normal_name = cocktail.get("normal_name", "unknown_drink")
            safe_cname = get_safe_name(normal_name)
            filename = os.path.join(LOGO_FOLDER, f"{safe_cname}.png")

            if os.path.exists(filename):
                # If it already exists, skip generation
                image_paths[normal_name] = filename
            else:
                prompt = (
                    f"A realistic illustration of a {normal_name} cocktail on a plain white background. "
                    "The lighting and shading create depth and realism, making the drink appear fresh and inviting."
                )
                try:
                    # 1) Generate the image URL
                    image_url = assist.generate_image(prompt)

                    # 2) Download + remove background in memory
                    img_data = requests.get(image_url).content
                    from io import BytesIO
                    with Image.open(BytesIO(img_data)).convert("RGBA") as original_img:
                        bg_removed = remove(original_img)
                        bg_removed.save(filename, "PNG")

                    image_paths[normal_name] = filename

                except Exception as e:
                    image_paths[normal_name] = f"Error: {e}"

                progress_bar.progress((idx + 1) / total)

        progress_bar.empty()
        st.success("Image generation complete.")

# ================ TAB 2: Settings ================
with tabs[1]:
    st.title("Settings")

    st.subheader("Prime Pumps")
    primetime = st.number_input("Priming Time", step=1, value=10)
    if st.button("Prime Pumps"):
        st.info(f"Priming all pumps for {primetime} seconds each...")
        try:
            controller.prime_pumps(duration=primetime)
            st.success("Pumps primed successfully!")
        except Exception as e:
            st.error(f"Error priming pumps: {e}")

    # NEW: Clean Pumps
    st.subheader("Clean Pumps")
    if st.button("Clean Pumps"):
        st.info("Reversing all pumps for 10 seconds each (cleaning mode)...")
        try:
            controller.clean_pumps(duration=10)
            st.success("All pumps reversed (cleaned).")
        except Exception as e:
            st.error(f"Error cleaning pumps: {e}")

    # Motor Calibration
    st.subheader("Motor Calibration")
    key_input = st.number_input("Seconds per 1oz", value=int(os.getenv("OZ_CALIBRATION")))
    if st.button("Save Motor Calibration"):
        set_key(".env", "OZ_CALIBRATION", str(key_input))

    # Clear OpenAI Key
    st.subheader("(Re)set OpenAI API Key")
    ai_key = st.text_input("OpenAI API Key")
    if st.button("Save API Key"):
        set_key(".env", "OPENAI_API_KEY", ai_key)

# ================ TAB 3: Cocktail Menu ================
with tabs[2]:
    st.markdown("<h1 style='text-align: center;'>Cocktail Menu</h1>", unsafe_allow_html=True)

    # Load the cocktails from file
    cocktail_data = {}
    if os.path.exists(COCKTAILS_FILE):
        try:
            with open(COCKTAILS_FILE, "r") as f:
                cocktail_data = json.load(f)
        except Exception as e:
            st.error(f"Error loading cocktails: {e}")

    if st.session_state.selected_cocktail:
        # USER IS VIEWING A COCKTAIL DETAIL PAGE
        safe_name = st.session_state.selected_cocktail
        selected_cocktail = None

        # Find the matching cocktail in the JSON
        for c in cocktail_data.get("cocktails", []):
            if get_safe_name(c.get("normal_name", "")) == safe_name:
                selected_cocktail = c
                break

        if selected_cocktail is None:
            st.error("Cocktail not found.")
        else:
            st.markdown(
                f"<h1 style='text-align: center;'>{selected_cocktail.get('fun_name', 'Cocktail')}</h1>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<h3 style='text-align: center;'>{selected_cocktail.get('normal_name', '')}</h3>",
                unsafe_allow_html=True
            )

            # Show the image if it exists
            image_file = os.path.join(LOGO_FOLDER, f"{safe_name}.png")
            if os.path.exists(image_file):
                st.image(image_file, use_container_width=True)
            else:
                st.write("Image not found.")

            # Show the recipe
            st.markdown("<h2 style='text-align: center;'>Recipe</h2>", unsafe_allow_html=True)
            recipe_adjustments = {}
            for ingredient, measurement in selected_cocktail.get("ingredients", {}).items():
                parts = measurement.split()
                try:
                    default_value = float(parts[0])
                    unit = " ".join(parts[1:]) if len(parts) > 1 else ""
                except:
                    default_value = 1.0
                    unit = measurement

                value = st.slider(
                    f"{ingredient} ({measurement})",
                    min_value=0.0,
                    max_value=default_value * 4,
                    value=default_value,
                    step=0.1,
                )
                recipe_adjustments[ingredient] = f"{value} {unit}".strip()

            st.markdown("<h3 style='text-align: center;'><strong>Adjusted Recipe</strong></h3>", unsafe_allow_html=True)
            st.json(recipe_adjustments)

            cols = st.columns([1, 1])
            with cols[0]:
                if st.button("Save Recipe"):
                    updated = False
                    # Overwrite the JSON with new measurements
                    for idx, cktl in enumerate(cocktail_data.get("cocktails", [])):
                        if get_safe_name(cktl.get("normal_name", "")) == safe_name:
                            cocktail_data["cocktails"][idx]["ingredients"] = recipe_adjustments
                            updated = True
                            break
                    if updated:
                        try:
                            with open(COCKTAILS_FILE, "w") as f:
                                json.dump(cocktail_data, f, indent=2)
                            st.success("Recipe saved!")
                        except Exception as e:
                            st.error(f"Error saving recipe: {e}")
                    else:
                        st.error("Failed to update recipe.")

            with cols[1]:
                if st.button("Pour"):
                    st.info("Pouring a single serving...")
                    # We call controller.make_drink with single
                    # Build a dictionary that matches what the controller expects
                    # The 'selected_cocktail' is already a dict from cocktails.json
                    # so we can pass it directly.
                    try:
                        controller.make_drink(CONFIG_FILE, selected_cocktail, single_or_double="single")
                    except Exception as e:
                        st.error(f"Error while pouring: {e}")

            # Back to gallery
            if st.button("Back to Menu"):
                st.session_state.selected_cocktail = None
                st.rerun()

    else:
        # GALLERY VIEW
        cocktails_list = cocktail_data.get("cocktails", [])
        if cocktails_list:
            for cocktail in cocktails_list:
                normal_name = cocktail.get("normal_name", "unknown_drink")
                safe_cname = get_safe_name(normal_name)
                filename = os.path.join(LOGO_FOLDER, f"{safe_cname}.png")

                st.markdown(f"<h3 style='text-align: center;'>{normal_name}</h3>", unsafe_allow_html=True)
                if os.path.exists(filename):
                    with open(filename, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                    st.markdown(
                        f"<div style='text-align: center;'><img src='data:image/png;base64,{encoded_string}' width='300'></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown("<p style='text-align: center;'>Image not found.</p>", unsafe_allow_html=True)

                # Buttons
                btn_cols = st.columns([2, 1, 1, 2])
                with btn_cols[1]:
                    if st.button("View", key=f"view_{safe_cname}"):
                        st.session_state.selected_cocktail = safe_cname
                        st.rerun()
                with btn_cols[2]:
                    if st.button("Pour", key=f"pour_{safe_cname}"):
                        # If they pour from the gallery, we can do single as well,
                        # but we have no way to adjust recipe first. We'll just pour the default recipe.
                        st.info(f"Pouring a single serving of {normal_name} ...")
                        try:
                            controller.make_drink(CONFIG_FILE, cocktail, single_or_double="single")
                        except Exception as e:
                            st.error(f"Error while pouring: {e}")
        else:
            st.markdown("<p style='text-align: center;'>No recipes generated yet. Please use the 'My Bar' tab to generate recipes.</p>", unsafe_allow_html=True)
