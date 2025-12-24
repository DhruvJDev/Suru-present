import sys
import os

# Check Python version
if sys.version_info < (3, 8):
    print("Error: Python 3.8 or higher is required.")
    print(f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print("\nPlease upgrade Python:")
    print("  macOS: brew install python@3.11")
    print("  Windows: Download from python.org")
    print("  Linux: sudo apt install python3.11")
    sys.exit(1)

import speech_recognition as sr
import time
import threading

from module import genai
from module import open_app as app_opener
from module import weather
from module import speak
from module import search_site_on_google as search_site
from module import google_search as search_google

# ---------- LISTEN FUNCTION ----------
def listen():
    recognizer = sr.Recognizer()

    try:
        microphone = sr.Microphone()
    except OSError:
        print("Microphone not found or not accessible.")
        speak.say("Microphone not found or not accessible.")
        sys.exit(1)

    with microphone as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("No speech detected within 10 seconds. Exiting...")
            speak.say("No speech detected within 10 seconds. Goodbye.")
            sys.exit()

    time.sleep(2)

    try:
        command = recognizer.recognize_google(audio).strip().lower()
        print(f"\nYou said: {command}")
        speak.say(f"You said: {command}")
        return command

    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak.say("Sorry, I did not understand that.")
        return ""

    except sr.RequestError:
        print("Speech recognition service error.")
        speak.say("Speech recognition service error.")
        return ""


# ---------- PROCESS COMMAND ----------
def process_command(command):
    if not command:
        return

    print("\nProcessing command...")

    if command.startswith("weather in ") or command.startswith("weather for "):
        city = command.replace("weather in ", "").replace("weather for ", "").strip()
        print(f"\nFetching weather for: {city}")

        spoken_report, point_report = weather.get_weather(city)
        print(f"\nFull report:\n{spoken_report}\n{point_report}")
        speak.say(spoken_report)

    elif command.startswith("search "):
        query = command.replace("search ", "").strip()
        print(f"\nSearching Google for: {query}")
        search_google.search_on_google(query)

    elif command.startswith("search site "):
        query = command.replace("search site ", "").strip()
        print(f"\nOpening site for: {query}")
        search_site.search_site_on_google(query)

    elif command.startswith("open "):
        app_name = command.replace("open ", "").strip()
        print(f"\nOpening application: {app_name}")
        speak.say(f"Opening {app_name}")
        app_opener.app_opener(app_name)

    else:
        response = genai.llm_response(command)
        print(f"\nResponse: \n\n{response}")
        speak.say(response)


# ---------- RUN GUI ----------
def gui_interface():
    # Import and run GUI directly (keeps terminal attached until GUI closes)
    project_root = os.path.dirname(os.path.abspath(__file__))
    gui_script = os.path.join(project_root, "gui", "gui.py")

    try:
        # Execute GUI script directly in the same process
        with open(gui_script, 'r', encoding='utf-8') as f:
            gui_code = f.read()
        exec(gui_code, {'__name__': '__main__', '__file__': gui_script})
    except Exception as e:
        print("Failed to launch GUI:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Launching Suru A.I. Desktop GUI...")
    speak.say("Launching Suru A.I. Desktop Interface.")
    gui_interface()


