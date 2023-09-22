import inspirobot
from gtts import gTTS
import playsound
import os
import time

def text_to_speech(msg):
        tts = gTTS(msg)
        tts.save("temp.mp3")
        time.sleep(1) 
        playsound.playsound("temp.mp3")
        os.remove("temp.mp3")

flow = inspirobot.flow()  # Generate a flow object
text_to_speech(flow[0].text)