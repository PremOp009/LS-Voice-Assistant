import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyautogui
import time

# --- ENGINE SETUP ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# 0 usually Male, 1 usually Female
engine.setProperty('voice', voices[0].id) 
engine.setProperty('rate', 180)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Mr. Prem!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Mr. Prem!")
    else:
        speak("Good Evening Mr. Prem!")
    
    speak("LS is online. Let's get things done, boss.")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎧 LS is Listening...")
        r.pause_threshold = 1
        # Adjust for ambient noise helps accuracy
        r.adjust_for_ambient_noise(source, duration=0.5) 
        audio = r.listen(source)

    try:
        print("⚡ Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Mr. Prem said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        speak("My bad, I didn't catch that.")
        return None
    except sr.RequestError:
        speak("Network glitch. Check your internet.")
        return None

# --- MAIN LOOP ---
if __name__ == "__main__":
    wish_me()

    while True:
        query = take_command()
        if not query:
            continue

        # --- OPEN ANY WEBSITE (FIXED) ---
        if 'open' in query and 'search' not in query:
            # 1. Extract the name (e.g., "youtube")
            domain_name = query.replace('open', '').strip()
            
            # 2. Speak the name immediately
            speak(f"Opening {domain_name}")
            
            # 3. Process URL
            site = domain_name.replace(' ', '')
            # Simple check to add .com if user just said "open google"
            if not site.endswith('.com') and not site.endswith('.org') and not site.endswith('.in'):
                site = site + ".com"
            if not site.startswith('http'):
                site = 'https://www.' + site
            
            webbrowser.open(site)

        # --- SEARCH THE WEB ---
        elif 'search for' in query or 'google' in query:
            if 'search for' in query:
                search_query = query.replace('search for', '').strip()
            else:
                search_query = query.replace('google', '').strip()
            
            speak(f"Searching Google for {search_query}")
            url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            webbrowser.open(url)

        # --- NOTEPAD FEATURE ---
        elif 'open notepad' in query or 'write a note' in query:
            speak("Opening Notepad, boss.")
            os.startfile("notepad.exe")
            time.sleep(2) # Wait for it to open
            speak("What are we writing?")
            
            content = take_command()
            if content:
                speak("Typing it out...")
                pyautogui.write(content, interval=0.05)
            else:
                speak("I didn't hear any text, skipping.")

        # --- WIKIPEDIA ---
        elif 'wikipedia' in query:
            speak('Checking Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except:
                speak("Couldn't find that page, sorry.")

        # --- TIME ---
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p") # 12-hour format
            speak(f"Mr. Prem, it's currently {strTime}")

        # --- QUIT ---
        elif 'quit' in query or 'stop' in query or 'exit' in query:
            speak("Signing off. Keep grinding, Mr. Prem!")
            exit()