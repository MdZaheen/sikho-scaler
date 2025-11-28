import pyttsx3
import os

print("Initializing pyttsx3...")
try:
    engine = pyttsx3.init()
    print("Saving to file...")
    engine.save_to_file('Hello World', 'test_tts.wav')
    engine.runAndWait()
    print("Done.")
    
    if os.path.exists('test_tts.wav'):
        print(f"File created: {os.path.getsize('test_tts.wav')} bytes")
    else:
        print("File NOT created.")
except Exception as e:
    print(f"Error: {e}")
