import os
import platform
import subprocess

import module.speak as speak

# Lazy-load app mappings from Firebase
from database.firebase_utils import get_app_mappings_from_firebase

# Cache for app mappings to avoid multiple Firebase fetches
_app_mappings_cache = None

def _get_app_mappings():
    """Get app mappings from Firebase (cached after first call)."""
    global _app_mappings_cache
    if _app_mappings_cache is None:
        _app_mappings_cache = get_app_mappings_from_firebase()
    return _app_mappings_cache

def app_opener(app_alias):
    os_name = platform.system().lower()

    # Normalize and fetch OS-specific app name
    app_key = app_alias.lower()
    app_mappings = _get_app_mappings()
    app_name = app_mappings.get(app_key, {}).get(os_name, app_alias) if app_mappings else app_alias

    try:
        if os_name == "windows":
            os.system(f'start {app_name}')
        
        elif os_name == "darwin":  # macOS
            result = subprocess.run(["open", "-a", app_name], capture_output=True, text=True)
            
            if result.returncode != 0:
                if "Unable to find application named" in result.stderr:
                    msg = f"'{app_name}' app not found on your Mac. Please check the app name."
                    print(msg)
                    speak.say(msg)
                else:
                    print("Error:", result.stderr)
                    speak.say("There was an error opening the app.")
            else:
                print(f"Successfully opened {app_name}")
        
        elif os_name == "linux":
            subprocess.Popen([app_name])
        
        else:
            print("Unsupported OS.")
            speak.say("Your operating system is not supported.")
    
    except Exception as e:
        error_msg = f"Failed to open application: {e}"
        print(error_msg)
        speak.say(error_msg)