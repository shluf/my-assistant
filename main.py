import os
import pygame
import pyautogui
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()


def speak(text):
    voice = "en-US-JennyNeural"
    edge_tts = os.getenv('DIR')
    command = f'{
        edge_tts} --voice "{voice}" --text "{text}" --write-media "output.mp3"'

    print('')
    os.system(command)
    print('')

    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load('output.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(e)

    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()


def take_command():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.7
        r.energy_threshold = 600
        print('listening...')
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio)

    except Exception as e:
        print(e)
        return ''

    return query


while True:
    query = take_command().lower()
    print(f'You: "{query}"')

    if "hello" in query:
        answer = 'hi how are you?'
        speak(answer)
        print("Assistant: " + answer)
    elif "open" in query:
        app_name = query.replace('open', '')
        speak('opening ' + app_name)
        pyautogui.press('super')
        pyautogui.sleep(0.7)
        pyautogui.typewrite(app_name)
        pyautogui.sleep(0.7)
        pyautogui.press('enter')
        speak("Is anything else?")

    elif "close" in query:
        speak('closing program')
        pyautogui.hotkey('alt', 'f4')
    elif "exit" in query:
        break
    else:
        answer = 'I dont understand'
        speak(answer)
        print("Assistant: " + answer)


# query = take_command()
# print(query)
