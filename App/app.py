import os
import pyttsx3
import speech_recognition as sr
from qa_database import qa_pairs

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ai-dentist-e728f5548373.json"

# Initialize the global 'voices' variable
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Function to ask the user whether to continue with voice or typing
def ask_user_preference():
    engine.setProperty('voice', voices[1].id)  # Index 1 is typically a female voice
    engine.say("Do you want to continue with voice or typing? Please say 'voice' or 'typing'.")
    engine.runAndWait()

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjusting for ambient noise
        print("Listening...")
        try:
            audio_data = recognizer.listen(source, timeout=10)
            print("Recognizing...")
            user_input = recognizer.recognize_google(audio_data).lower()

            if "voice" in user_input:
                engine.say("You have selected the voice option. Now you can ask me any question.")
                engine.runAndWait()

            return user_input

        except sr.UnknownValueError:
            print("Sorry, I could not understand your preference. Please try again.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            print("Sorry, there was an error. Please try again.")
            return ""

# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusting for ambient noise
        print("Listening...")
        try:
            audio_data = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            user_input = recognizer.recognize_google(audio_data)
            return user_input.lower()

        except sr.UnknownValueError:
            print("Sorry, I could not understand your question. Please try again.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            print("Sorry, there was an error. Please try again.")
            return ""

# Function to fetch answer based on user input
def get_answer(user_input):
    user_input_lower = user_input.lower()

    # Check for exact match
    exact_match = qa_pairs.get(user_input_lower)
    if exact_match:
        return exact_match

    # If no exact match, search for answers based on keywords
    matching_answers = []
    for question, answer in qa_pairs.items():
        if any(keyword in user_input_lower for keyword in question.split()):
            matching_answers.append(answer)

    if matching_answers:
        return "\n".join(matching_answers)
    else:
        return "Sorry, I don't have an answer for that."
    
# Function to welcome the user
def welcome_message():
    engine.say("Welcome to Virtual AI Dentist. How may I help you?")
    engine.runAndWait()

# Main function
def activate_input():
    welcome_message()
    preference = ask_user_preference()
    
    while True:
        if "voice" in preference:
            user_input = recognize_speech()
        elif "typing" in preference:
            user_input = input("Please type your question: ").lower()
        else:
            print("Invalid preference. Please say 'voice' or 'typing'.")
            preference = ask_user_preference()
            continue

        if "bye" in user_input:
            break

        answer = get_answer(user_input)
        engine.say(answer)
        engine.runAndWait()

# Example usage
if __name__ == "__main__":
    activate_input()
