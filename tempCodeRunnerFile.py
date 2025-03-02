import pyttsx3

def recognize_speech():
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except ModuleNotFoundError:
        print("Error: The 'speech_recognition' module is not installed. Please install it using 'pip install SpeechRecognition'.")
        return None
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        print("Could not request results, check your internet connection.")
        return None

def process_query(text):
    if text:
        if "restaurant" in text or "food" in text or "dishes" in text:
            return "I can help you find the top 5 dishes nearby!"
        else:
            return "I didn't understand that. Please ask about restaurant recommendations."
    return "Sorry, I couldn't hear you."

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Set to a soft female voice
    engine.setProperty('rate', 170)  # Slightly increase speed for a natural flow
    engine.setProperty('volume', 1.0)  # Set volume to max for clarity
    
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    user_input = recognize_speech()
    response = process_query(user_input)
    speak(response)
