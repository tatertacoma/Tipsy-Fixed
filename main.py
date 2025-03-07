# main.py
import subprocess
import sys

# Launch the Pygame interface in a separate process.
interface_process = subprocess.Popen([sys.executable, "interface.py"])

# Launch the Streamlit app in a separate process.
streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"])

# Wait for both processes to finish.
interface_process.wait()
streamlit_process.wait()
