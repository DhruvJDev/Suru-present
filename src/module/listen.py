# Function to listen for user input and recognize speech

import sys
import time

import speech_recognition as sr
import speak as speak


def listen():
    recognizer = sr.Recognizer()

    try:
        microphone = sr.Microphone()
    except OSError:
        print("Microphone not found or not accessible.")
        speak.say("Microphone not found or not accessible.")
        sys.exit(1)

    print("\nLISTENING...")
    # print("\nListening...")
    # speak.say("Listening...")

    full_audio = None
    last_spoken_time = time.time()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        
        while True:
            try:
                # print("Listening for speech...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

                if full_audio is None:
                    full_audio = audio
                else:
                    # Concatenate audio if needed
                    full_audio = sr.AudioData(
                        full_audio.get_raw_data() + audio.get_raw_data(),
                        full_audio.sample_rate,
                        full_audio.sample_width
                    )

                last_spoken_time = time.time()

                # Wait 5 seconds to check for more speech
                # print("Waiting 5 seconds for more speech...")
                while time.time() - last_spoken_time < 5:
                    try:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        full_audio = sr.AudioData(
                            full_audio.get_raw_data() + audio.get_raw_data(),
                            full_audio.sample_rate,
                            full_audio.sample_width
                        )
                        last_spoken_time = time.time()
                        # print("Detected more speech. Continuing...")
                    except sr.WaitTimeoutError:
                        # print("No additional speech detected.")
                        break

                    # Done listening — recognize speech
                    try:
                        command = recognizer.recognize_google(full_audio).strip().lower()
                        speak.say(f"You said: {command}")
                        return command

                    except sr.UnknownValueError:
                        return None

                    except sr.RequestError:
                        return None

            except sr.WaitTimeoutError:
                sys.exit()
                
                
if __name__ == "__main__":
  
    command = listen()
    