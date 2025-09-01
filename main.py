import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import wikipedia
from openai import OpenAI

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index for male/female voice

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Say that again please...")
        return "None"
    return query.lower()

def get_news():
    api_key = "YOUR_NEWS_API_KEY"  # from https://newsapi.org/
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    news = requests.get(url).json()
    articles = news["articles"][:5]
    for i, article in enumerate(articles, 1):
        speak(f"News {i}: {article['title']}")

def get_weather(city="Delhi"):
    api_key = "YOUR_OPENWEATHERMAP_KEY"  # from https://openweathermap.org/api
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] != "404":
        main = response["main"]
        temp = main["temp"]
        desc = response["weather"][0]["description"]
        speak(f"The weather in {city} is {desc} with {temp} degree Celsius.")
    else:
        speak("City not found.")

# --- ChatGPT integration ---
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # put your key here

def chatgpt_answer(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # lightweight, fast model
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your AI Assistant. How can I help you today?")

if _name_ == "_main_":
    wish()
    while True:
        query = take_command()

        if "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "open youtube" in query:
            webbrowser.open("https://youtube.com")

        elif "open google" in query:
            webbrowser.open("https://google.com")

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif "news" in query:
            get_news()

        elif "weather" in query:
            speak("Which city?")
            city = take_command()
            get_weather(city)

        elif "stop" in query or "exit" in query:
            speak("Goodbye!")
            break

        else:
            # Default → ChatGPT
            answer = chatgpt_answer(query)
            speak(answer)
