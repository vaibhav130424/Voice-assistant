import pyttsx3
import requests

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

def get_nearby_restaurants(cuisine_filter=None, min_rating=0, max_price=None):
    latitude = 28.6139  # Example Latitude (New Delhi)
    longitude = 77.2090  # Example Longitude (New Delhi)
    radius = 5000  # 5km radius
    
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["amenity"="restaurant"](around:{radius},{latitude},{longitude});
    out;
    """
    response = requests.get(overpass_url, params={"data": query})
    data = response.json()
    
    restaurants = []
    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name", "Unnamed Restaurant")
        cuisine = element.get("tags", {}).get("cuisine", "Unknown Cuisine")
        rating = float(element.get("tags", {}).get("rating", 0))  # Default rating 0
        price = element.get("tags", {}).get("price", "Unknown Price")
        
        if cuisine_filter and cuisine_filter.lower() not in cuisine.lower():
            continue
        if rating < min_rating:
            continue
        if max_price and price.lower() != max_price.lower():
            continue
        
        restaurants.append(f"{name} ({cuisine}) - Rating: {rating}, Price: ₹{price}")
    
    return restaurants[:5] if restaurants else ["No matching restaurants found"]

def process_query(text):
    if text:
        cuisine_filter = None
        min_rating = 0
        max_price = None
        
        if "chinese" in text:
            cuisine_filter = "chinese"
        elif "italian" in text:
            cuisine_filter = "italian"
        elif "indian" in text:
            cuisine_filter = "indian"
        
        if "best" in text or "top" in text:
            min_rating = 4.0  # Only show restaurants with 4+ rating
        
        if "cheap" in text:
            max_price = "₹"
        elif "mid-range" in text:
            max_price = "₹₹"
        elif "expensive" in text:
            max_price = "₹₹₹"
        
        if "restaurant" in text or "food" in text or "dishes" in text:
            restaurants = get_nearby_restaurants(cuisine_filter, min_rating, max_price)
            return "Here are the top restaurants near you: " + ", ".join(restaurants)
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
