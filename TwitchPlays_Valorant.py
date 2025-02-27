import concurrent.futures
import random
import keyboard
import time
import pydirectinput
import pyautogui
from gtts import gTTS
import playsound
import os
import inspirobot

import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *

##################### GAME VARIABLES #####################

# Replace this with your Twitch username. Must be all lowercase.
TWITCH_CHANNEL = 'tempeus' 

# If streaming on Youtube, set this to False
STREAMING_ON_TWITCH = True

# If you're streaming on Youtube, replace this with your Youtube's Channel ID
# Find this by clicking your Youtube profile pic -> Settings -> Advanced Settings
YOUTUBE_CHANNEL_ID = "YOUTUBE_CHANNEL_ID_HERE" 

# If you're using an Unlisted stream to test on Youtube, replace "None" below with your stream's URL in quotes.
# Otherwise you can leave this as "None"
YOUTUBE_STREAM_URL = None

##################### MESSAGE QUEUE VARIABLES #####################

# MESSAGE_RATE controls how fast we process incoming Twitch Chat messages. It's the number of seconds it will take to handle all messages in the queue.
# This is used because Twitch delivers messages in "batches", rather than one at a time. So we process the messages over MESSAGE_RATE duration, rather than processing the entire batch at once.
# A smaller number means we go through the message queue faster, but we will run out of messages faster and activity might "stagnate" while waiting for a new batch. 
# A higher number means we go through the queue slower, and messages are more evenly spread out, but delay from the viewers' perspective is higher.
# You can set this to 0 to disable the queue and handle all messages immediately. However, then the wait before another "batch" of messages is more noticeable.
MESSAGE_RATE = 0.5
# MAX_QUEUE_LENGTH limits the number of commands that will be processed in a given "batch" of messages. 
# e.g. if you get a batch of 50 messages, you can choose to only process the first 10 of them and ignore the others.
# This is helpful for games where too many inputs at once can actually hinder the gameplay.
# Setting to ~50 is good for total chaos, ~5-10 is good for 2D platformers
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100 # Maximum number of threads you can process at a time 

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
pyautogui.FAILSAFE = False


##########################################################

# Count down before starting, so you have time to load up the game
countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
    time.sleep(1)

if STREAMING_ON_TWITCH:
    t = TwitchPlays_Connection.Twitch()
    t.twitch_connect(TWITCH_CHANNEL)
else:
    t = TwitchPlays_Connection.YouTube()
    t.youtube_connect(YOUTUBE_CHANNEL_ID, YOUTUBE_STREAM_URL)

def text_to_speech(msg):
        name = f"temp{time.time()}.mp3"
        tts = gTTS(msg)
        tts.save(name)
        time.sleep(1) 
        playsound.playsound(name)
        os.remove(name)

def handle_message(message):
    try:
        msg = message['message'].lower()
        username = message['username'].lower()

        print("Got this message from " + username + ": " + msg)

        # Now that you have a chat message, this is where you add your game logic.
        # Use the "HoldKey(KEYCODE)" function to permanently press and hold down a key.
        # Use the "ReleaseKey(KEYCODE)" function to release a specific keyboard key.
        # Use the "HoldAndReleaseKey(KEYCODE, SECONDS)" function press down a key for X seconds, then release it.
        # Use the pydirectinput library to press or move the mouse

        # I've added some example videogame logic code below:

        ###################################
        # Valorant Key Codes 
        ###################################

        #Drop Gun
        if msg == "drop": 
            text_to_speech("Dropping Gun")
            HoldAndReleaseKey(G, 1)

        if msg == "inspire me":
            flow = inspirobot.flow()  # Generate a flow object
            text_to_speech(flow[0].text)

        #ULT
        if msg == "ult":
            text_to_speech("Using Ultimate")
            HoldAndReleaseKey(X, 1)
            time.sleep(0.5)
            pydirectinput.mouseDown(button="left")
            time.sleep(0.25)
            pydirectinput.mouseUp(button="left")

        # Press the spacebar for 0.7 seconds
        if msg == "jump": 
            text_to_speech("Initiating Jumping Sequence")
            HoldAndReleaseKey(SPACE, 0.7)

        # Press the left mouse button down for 1 second, then release it
        if msg == "shoot": 
            text_to_speech("Shooting your gun")
            pydirectinput.mouseDown(button="left")
            time.sleep(1)
            pydirectinput.mouseUp(button="left")

        if msg == "meow":
            HoldAndReleaseKey(NUMPAD_1, 0.7)

        if msg == "tp":
            HoldAndReleaseKey(NUMPAD_2, 0.7)
        
        if msg == "raze":
            HoldAndReleaseKey(NUMPAD_3, 0.7)
        
        if msg == "laugh":
            HoldAndReleaseKey(NUMPAD_4, 0.7)
        
        if msg == "defuse":
            HoldAndReleaseKey(NUMPAD_5, 0.7)

        if msg == "crouch":
            text_to_speech("Initiating Crouching Sequence")
            HoldAndReleaseKey(LEFT_CONTROL, 5)

        if msg == "vc":
            HoldAndReleaseKey(V, 10)

        if msg == "pistol":
            HoldAndReleaseKey(TWO, 0.7)

        if msg == "reload":
            text_to_speech("Initiating Reloading Sequence")
            HoldAndReleaseKey(R, 0.7)
        
        if msg == "knife":
            HoldAndReleaseKey(THREE, 0.7)
        
        if msg == "use ability 1":
            text_to_speech("Initiating Ability Usage Sequence")
            HoldAndReleaseKey(C, 0.7)
            time.sleep(0.5)
            pydirectinput.mouseDown(button="left")
            time.sleep(0.25)
            pydirectinput.mouseUp(button="left")

        if msg == "use ability 2":
            text_to_speech("Initiating Ability Usage Sequence")
            HoldAndReleaseKey(LEFT_ALT, 0.7)
            time.sleep(0.5)
            pydirectinput.mouseDown(button="left")
            time.sleep(0.25)
            pydirectinput.mouseUp(button="left")

        if msg == "use ability 3":
            text_to_speech("Initiating Ability Usage Sequence")
            HoldAndReleaseKey(E, 0.7)
            time.sleep(0.5)
            pydirectinput.mouseDown(button="left")
            time.sleep(0.25)
            pydirectinput.mouseUp(button="left")

        if msg == "slippery hands":
            text_to_speech("Initiating Slippery Hands Sequence")
            drop_weapon_every_interval(10)

        if msg == "reload paranoia":
            text_to_speech("Initiating reloading paranoia")
            reload_paranoia(5)


        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))


def drop_weapon_every_interval(timer_duration):
    for i in range(10):
        # Sleep for the specified duration
        time.sleep(timer_duration)

        print("Dropping gun")
        HoldAndReleaseKey(G, 0.7)

def reload_paranoia(timer_duration):
    for i in range(20):
        time.sleep(timer_duration)

        pydirectinput.mouseDown(button="left")
        time.sleep(1)
        pydirectinput.mouseUp(button="left")
        HoldAndReleaseKey(R, 0.7)

dropbool = False

while True:
    active_tasks = [t for t in active_tasks if not t.done()]

    #Check for new messages
    new_messages = t.twitch_receive_messages()
    if new_messages:
        message_queue += new_messages; # New messages are added to the back of the queue
        message_queue = message_queue[-MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

    messages_to_handle = []
    if not message_queue:
        # No messages in the queue
        last_time = time.time()
    else:
        # Determine how many messages we should handle now
        r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            # Pop the messages we want off the front of the queue
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time()

    # If user presses Shift+Backspace, automatically end the program
    if keyboard.is_pressed('shift+backspace'):
        exit()
    
    if not messages_to_handle:
        continue
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(thread_pool.submit(handle_message, message))
            else:
                print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')
 