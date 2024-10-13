import speech_recognition as sr
import pyttsx3
import os
import datetime
import webbrowser
import smtplib
from email.mime.text import MIMEText
import pyglet
import requests
import pywhatkit
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'YOUR_SPOTIPY_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'YOUR_SPOTIPY_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'YOUR_SPOTIPY_REDIRECT_URI'


# Define a function to listen for voice commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language='en-in')
            print(f"YOU: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, say again ")
            return None

# Define a function to respond to voice commands
def respond(command):
    if command == "hello":
        current_time = datetime.datetime.now().strftime("%H:%M")
        hour = int(current_time.split(":")[0])
        if hour < 12:
            engine.say("Good morning, what can I do for you?")
        elif hour < 17:
            engine.say("Good afternoon, what can I do for you?")
        elif hour < 20:
            engine.say("Good evening, what can I do for you?")
        else:
            engine.say("Good night, what can I do for you?")
        
        
        #For time
    elif command == "what is time":
        engine.say(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
        #for Opening Google

    elif command == "open google":
        engine.say("Opening Google")
        webbrowser.open("https://www.google.com")
        
        #FOr Opening YouTube
    elif command == "open youtube":
        engine.say("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")
    
    #FOr Opening Whatsapp
    elif command == "open whatsapp":
        engine.say("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com/")
    
    #For Opening Snapchat

    elif command == "open snapchat":
        engine.say("Opening Snapchat")
        webbrowser.open("https://web.snapchat.com/")
    
    #For Opening GitHub 
    elif command == "open github":
        engine.say("Opening GitHub")
        webbrowser.open("https://github.com/")
        
        #For send email
    elif command == "send email":
        send_email()
        
        #set reminder
    elif command == "set reminder":
        set_reminder()
        
        #play music
    elif command == "play music":
        play_music()
        
        #get weather
    elif command == "get weather":
        get_weather()
    elif command == "take notes":
        
        #take notes
        take_notes()
    
    # video call
    elif command == " video call":
        make_video_call()
        
        
    else:
        engine.say("Sorry, I didn't understand that")



#Functions

# Define a function to send an email
def send_email():
    engine.say("Please enter the recipient's ema0il address")
    recipient = listen()
    engine.say("Please enter the email subject")
    subject = listen()
    engine.say("Please enter the email body")
    body = listen()
    
    
    # Send the email using smtplib
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your_email_address'
    msg['To'] = recipient
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email_address', 'your_email_password')
    server.sendmail('your_email_address', recipient, msg.as_string())
    server.quit()
    engine.say("Email sent successfully")



# Define a function to set reminders
def set_reminder():
    engine.say("Please enter the reminder message")
    message = listen()
    engine.say("Please enter the reminder time in HH:MM format")
    time = listen()
    reminder_time = datetime.datetime.strptime(time, "%H:%M")
    while True:
        current_time = datetime.datetime.now().time()
        if current_time.hour == reminder_time.hour and current_time.minute == reminder_time.minute:
            engine.say(f"Reminder: {message}")
            break



# Define a function to play music
# Define a function to play music
def play_music():
    engine.say("Please enter the music file path")
    file_path = listen()
    music = pyglet.media.load(file_path, streaming=False)
    music.play()
    pyglet.app.run()




# Define a function to get weather information
def get_weather():
    engine.say("Please enter the city name")
    city = listen()
    api_key = "YOUR_WEATHER_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    engine.say(f"The weather in {city} is {weather_data['weather'][0]['description']}")


# Define a function to take notes
def take_notes():
    engine.say("Please enter the note")
    note = listen()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("notes.txt", "a") as f:
        f.write(f"{current_time}: {note}\n")
    engine.say("Note taken successfully")




# Define a function to make a video call def make_video_call():
    engine.say("Please enter the phone number of the person you want to call")
    phone_number = listen()
    pywhatkit.sendwhatmsg_instantly(phone_number, "Video call", 15, True, 15, True)
    engine.say("Video call initiated")
    
    
    
    # Main loop
while True:
    command = listen()
    if command:
        respond(command)
    engine.runAndWait()