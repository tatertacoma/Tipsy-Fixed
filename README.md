
# Tipsy the AI Cocktail Maker Project

This project is a multi-part cocktail maker system designed to run on a Raspberry Pi. It integrates three separate modules:

1. **Streamlit App (app.py):**  
   Allows users to configure pump settings, generate cocktail recipes (using an OpenAI API), and view a recipe book with cocktail images and details.

2. **Pygame Interface (interface.py):**  
   Provides a full-screen, swipeable interface for cocktail selection. The interface displays a background image (`tipsy.png`), overlays the selected cocktail logo, and includes extra interactive logos (`single.png` and `double.png`) to select drink mode (single or double). It features various animations such as text zoom and logo pop effects, and displays pouring/loading overlays.

3. **Pump Controller (controller.py):**  
   Reads the selected cocktail and pump configuration (from `cocktails.json` and `pump_config.json`), then controls 12 pumps via the Raspberry Pi GPIO (using L91105 motor drivers) to mix the drink. The controller uses a mapping of ingredients to pump pins.

4. **Main Launcher (main.py) (optional):**  
   A helper script to launch both the Streamlit app and Pygame interface concurrently.

---

## Features

- **Cocktail Recipe Generation:**  
  Generates cocktail recipes (via OpenAI API) based on pump configuration and bartender requests.

- **Swipe & Mode Selection Interface:**  
  Use touch/mouse swipe gestures to navigate cocktail logos. Tap the extra logos (`single.png` and `double.png`) to select drink mode, triggering animations and overlays.

- **Pump Control:**  
  Uses Raspberry Pi GPIO and L91105 motor drivers to run pumps based on the selected cocktail’s ingredients.

- **Configurable Pump Setup:**  
  Pump-to-ingredient mapping is stored in `pump_config.json`.

- **Persistent API Key:**  
  The Streamlit app prompts for an OpenAI API key (if not found in a `.env` file) and saves it for future use.

---

## File Structure

- **app.py:**  
  Streamlit-based user interface for configuration and recipe management.

- **interface.py:**  
  Pygame full-screen interface for cocktail selection and mode (single/double) using swipe and click gestures.

- **controller.py:**  
  Reads cocktail and pump configurations, then controls the pumps via Raspberry Pi GPIO based on the selected cocktail.

- **main.py:**  
  (Optional) A launcher that runs both the Streamlit app and Pygame interface concurrently.

- **pump_config.json:**  
  JSON file mapping pump numbers to ingredients.

- **cocktails.json:**  
  JSON file containing generated cocktail recipes.

- **selected_cocktail.txt & selected_mode.txt:**  
  Files written by the interface to communicate the selected cocktail and drink mode to the controller.

- **.env:**  
  File for storing environment variables (like the OpenAI API key).

- **Image Assets:**  
  - `tipsy.png`: Background image for the Pygame interface.  
  - `drink_logos/`: Folder containing cocktail logo images (PNG).  
  - `single.png` and `double.png`: Logos for selecting drink mode.  
  - `pouring.png`: Full-screen overlay image for when the drink is pouring.  
  - `loading.png`: A 720×720 loading image that spins during the pouring sequence.

---

## Hardware Requirements

- **Raspberry Pi (any recent model)**  
- **L91105 Motor Drivers** for each pump  
- **12 Pumps** connected to the L91105 boards, with the following GPIO pin configuration:

  | Pump    | IA Pin | IB Pin |
  |---------|--------|--------|
  | Pump 1  | GPIO17 | GPIO4  |
  | Pump 2  | GPIO22 | GPIO27 |
  | Pump 3  | GPIO10 | GPIO9  |
  | Pump 4  | GPIO5  | GPIO11 |
  | Pump 5  | GPIO13 | GPIO6  |
  | Pump 6  | GPIO26 | GPIO19 |
  | Pump 7  | GPIO20 | GPIO21 |
  | Pump 8  | GPIO12 | GPIO16 |
  | Pump 9  | GPIO8  | GPIO7  |
  | Pump 10 | GPIO24 | GPIO25 |
  | Pump 11 | GPIO18 | GPIO23 |
  | Pump 12 | GPIO14 | GPIO15 |

- **Touchscreen or Mouse** for interacting with the Pygame interface

---

## Software Dependencies

- **Python 3.x**
- **Streamlit**  
  `pip install streamlit`
- **Pygame**  
  `pip install pygame`
- **RPi.GPIO** (or similar, for Raspberry Pi GPIO control)  
  `pip install RPi.GPIO`
- **python-dotenv**  
  `pip install python-dotenv`
- **Requests**  
  `pip install requests`
- **OpenAI Python Library** (configured in `assist.py`)  
  `pip install openai`
- **Pydantic** (if used in your assistant module)  
  `pip install pydantic`

---

## Installation & Setup

1. **Clone the Repository:**  
   ```bash
   git clone https://your.repo.url
   cd your-repo-folder
   ```

2. **Install Dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```
   *(Alternatively, install the packages listed above individually.)*

3. **Configure GPIO & Hardware:**  
   Wire your pumps to the Raspberry Pi as per the pin mapping provided above. Ensure your L91105 drivers and pumps are correctly connected.

4. **Set Up API Key:**  
   When running the Streamlit app (app.py), you will be prompted to enter your OpenAI API key. This key will be saved to a `.env` file for future use.

5. **Prepare JSON Files:**  
   - Edit `pump_config.json` to map pumps to your desired ingredients.  
   - Generate cocktail recipes via the Streamlit interface (app.py) to create/update `cocktails.json`.

6. **Place Image Assets:**  
   - Ensure `tipsy.png` is in the project root.  
   - Place your cocktail logo images in the `drink_logos` folder.  
   - Ensure `single.png`, `double.png`, `pouring.png`, and `loading.png` are in the project root (or adjust paths accordingly).

---

## Running the Project

### Option 1: Launch Separately
- **Streamlit App:**  
  ```bash
  streamlit run app.py
  ```
- **Pygame Interface:**  
  ```bash
  python interface.py
  ```
- **Controller:**  
  After selecting a cocktail and mode, run the controller on the Raspberry Pi:  
  ```bash
  python controller.py
  ```

### Option 2: Launch Together Using Main Launcher
- **Main Launcher (main.py):**  
  ```bash
  python main.py
  ```
  This script launches both the Streamlit app and the Pygame interface concurrently. (You can run the controller separately when ready.)

---

## Controller Operation

The `controller.py` script will:
1. Read `pump_config.json` and `cocktails.json`.
2. Determine which cocktail is selected by reading `selected_cocktail.txt`.
3. Determine the drink mode (single or double) by reading `selected_mode.txt`.
4. Activate the appropriate pumps via GPIO for the required duration based on the cocktail recipe.  
*Adjust the conversion factor (seconds per ounce) in `controller.py` to suit your pump flow rate.*

---

## Troubleshooting

- **GPIO Issues:**  
  Ensure that your wiring matches the pin mappings in `controller.py` and that your Raspberry Pi user has permissions to access GPIO.

- **Image Loading Errors:**  
  Verify that all image files (`tipsy.png`, `pouring.png`, `loading.png`, logos, etc.) are present and paths are correct.

- **API Key Issues:**  
  If the API key prompt appears on every run, ensure the `.env` file is being written to and that you have appropriate write permissions.

- **Dependency Errors:**  
  Check that all Python dependencies are installed correctly. Use `pip freeze` to verify.

---

## License

*Include your project license here (e.g., MIT License).*

---

## Acknowledgments

*Mention any libraries, tutorials, or contributors that helped build this project.*

---

This README provides an overview of the system and instructions to set up and run the project on a Raspberry Pi. Adjust details as necessary to fit your exact implementation and hardware setup.

