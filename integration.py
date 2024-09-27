import os
import sys
import threading
import random
import datetime
import webbrowser
import wikipedia
import cv2
import pywhatkit as kit
import smtplib
import openai
import speech_recognition as sr
from requests import get
from Bujjivoice import speak_bujji
from Jarvisvoice import speak_jarvis

# Initialize OpenAI
openai.api_key = 'Your_OpenAI_API_Key'

# Define listen function
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
    except Exception as e:
        speak_bujji("Say that again please...")
        return "None"
    return query

# Define functions used by both assistants
def open_application(app_name):
    paths = {
        'notepad': r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\notepad.exe",
        'adobe reader': r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\adobe reader",
    }
    os.startfile(paths.get(app_name.lower()))

def open_camera():
    cap = cv2.VideoCapture(0)
    while True:
        rect, img = cap.read()
        cv2.imshow('webcam', img)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def get_ip():
    ip = get('https://api.ipify.org').text
    speak_bujji(f"Your IP is {ip}")
    return ip

def search_wikipedia(query, assistant='bujji'):
    results = wikipedia.summary(query, sentences=1)
    if assistant == 'bujji':
        speak_bujji(f"According to Wikipedia, {results}")
    else:
        speak_jarvis(f"According to Wikipedia, {results}")
    return results

def open_website(url, assistant='bujji'):
    webbrowser.open(url)
    if assistant == 'bujji':
        return f"Opened {url}"
    else:
        return f"Opened {url}"

def send_whatsapp_message(contact_name, message):
    contacts = {
        'chetan': '+919848976688',
        # Add more contacts here
    }
    contact_number = contacts.get(contact_name.lower())
    if contact_number:
        kit.sendwhatmsg(contact_number, message, 13, 1)  # Send message at 10:25 PM
        return f"Sent message to {contact_name}"
    else:
        speak_bujji(f"Contact {contact_name} not found.")
        return f"Contact {contact_name} not found."

def generate_email_content(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def get_email_address(name):
    email_addresses = {
        'avi': 'avi@example.com',
        # Add more email addresses here
    }
    return email_addresses.get(name.lower())

def send_email(to, subject, content):
    email_text = f"Subject: {subject}\n\n{content}"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your-email@gmail.com', 'your-email-password')
    server.sendmail('your-email@gmail.com', to, email_text)
    server.close()
    return f"Email sent to {to}"

def handle_command(query, assistant='bujji'):
    if assistant == 'bujji':
        speak = speak_bujji
        assistant_name = "bujji"
    else:
        speak = speak_jarvis
        assistant_name = "jarvis"

    if 'open notepad' in query:
        speak(open_application('notepad'))
    elif 'open adobe reader' in query:
        speak(open_application('adobe reader'))
    elif 'open command prompt' in query:
        os.system("start cmd")
        speak("Opened command prompt")
    elif 'open camera' in query:
        open_camera()
        speak("Camera opened")
    elif 'play music' in query:
        music_dir = 'path_to_music_directory'
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, random.choice(songs)))
        speak("Playing music")
    elif 'ip address' in query:
        ip = get_ip()
        speak(f"{assistant_name}: Your IP is {ip}")
    elif 'wikipedia' in query:
        query = query.replace('wikipedia', '')
        result = search_wikipedia(query, assistant=assistant)
        speak(f"{assistant_name}: According to Wikipedia, {result}")
    elif 'open youtube' in query:
        open_website('https://www.youtube.com', assistant=assistant)
        speak(f"{assistant_name}: Opened YouTube")
    elif 'open google' in query:
        speak("What should I search on Google?")
        search_query = takeCommand().lower()
        open_website(f"https://www.google.com/search?q={search_query}", assistant=assistant)
        speak(f"{assistant_name}: Opened Google search for {search_query}")
    elif 'send message to' in query:
        contact_name = query.replace('send message to', '').strip()
        speak(f"What message do you want to send to {contact_name}?")
        message = takeCommand()
        result = send_whatsapp_message(contact_name, message)
        speak(f"{assistant_name}: {result}")
        print(f"{assistant_name}: {result}")
    elif 'send email to' in query:
        recipient_name = query.replace('send email to', '').strip()
        speak(f"What should be the subject?")
        subject = takeCommand()
        speak(f"What should be the content?")
        prompt = takeCommand()
        email_content = generate_email_content(prompt)
        recipient_email = get_email_address(recipient_name)
        result = send_email(recipient_email, subject, email_content)
        speak(f"{assistant_name}: {result}")
    elif 'no thanks' in query or 'goodbye' in query:
        speak(f"{assistant_name}: Thank you for using our assistant. Have a good day!")
        sys.exit()
    else:
        speak(f"{assistant_name}: I didn't understand that. Please say it again.")

def main():
    bujji_active = False
    jarvis_active = False

    while True:
        query = takeCommand().lower()

        if 'activate bujji' in query:
            bujji_active = True
            speak_bujji("Bujji activated.")
        elif 'deactivate bujji' in query:
            bujji_active = False
            speak_bujji("Bujji deactivated.")
        elif 'activate jarvis' in query:
            jarvis_active = True
            speak_jarvis("Jarvis activated.")
        elif 'deactivate jarvis' in query:
            jarvis_active = False
            speak_jarvis("Jarvis deactivated.")

        if bujji_active:
            handle_command(query, assistant='bujji')
        elif jarvis_active:
            handle_command(query, assistant='jarvis')

if __name__ == "__main__":
    main()
