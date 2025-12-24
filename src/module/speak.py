import os
import platform
import subprocess

# Silent mode: set to True to disable all audio output
SILENT_MODE = False

def say(text):
    """Speak text. Uses native TTS for each OS."""
    
    if SILENT_MODE:
        print(f"[SURU]: {text}")
        return
    
    system_platform = platform.system()

    if system_platform == "Darwin":  # macOS - uses built-in 'say' command
        os.system(f'say "{text}"')

    elif system_platform == "Windows":
        try:
            # Use PowerShell System.Speech (Windows native, most reliable)
            escaped_text = text.replace("'", "''").replace('"', '\\"')
            ps_command = f"""
$synth.Speak('{escaped_text}')
"""
            # Note: This uses the default Windows audio output device.
            # To change which device is used, go to Windows Sound Settings
            # and set "Speakers" as the default playback device.
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_command],
                capture_output=True,
                timeout=30
            )
        except subprocess.TimeoutExpired:
            print(f"[SURU]: {text} (speech timed out)")
        except Exception as e:
            print(f"[SURU]: {text} (speech failed: {e})")

    elif system_platform == "Linux":
        try:
            # Try espeak on Linux
            os.system(f'espeak "{text}"')
        except Exception as e:
            print(f"[SURU]: {text} (speech failed: {e})")

    else:
        print("Speech not supported on this platform.")
