#!/usr/bin/env python3

import speech_recognition as sr
import subprocess
import re
from os import path
import cv2
import face_recognition

mov_file = "data/dan.mov"
mov_file = "data/andrew.mov"
mov_file = "data/seth.mov"
mov_file = "data/sarah.mov"
mov_file = "data/dev.mov"
wav_file = "data/temp.wav"

command = "ffmpeg -i " + mov_file + " -ab 160k -ac 2 -ar 44100 -vn " + wav_file

subprocess.call(command, shell=True)

cap = cv2.VideoCapture(mov_file)
process_this_frame = True;
while(cap.isOpened()):
    print("Reading frame...")
    ret, frame = cap.read()
    small_frame = cv2.resize(frame, (0,0), fx=.25, fy=.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)

    if len(face_locations) != 0:
        print("locations: {}".format(len(face_locations)))
        top, right, bottom, left = face_locations[0]
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
        crop_img = frame[top:bottom, left:right]
        break;

    process_this_frame = ~process_this_frame;

cap.release()
cv2.destroyAllWindows()

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), wav_file)
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")



# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    extract_string = r.recognize_sphinx(audio)
    #extract_string = "so that i never according to my name is dan they still you what are you doing today one measure and it would even want to do with her life courtier aspirations were you be successful whole ally in being engineer i work for no one that won't island engineering friendly soccer thigh length news he funny are no unlawfully and i live in los that i am can hope for now i have lives sometimes there were glasses sometimes i don't think favorite animal is elephants order has spent two theory or through this time for a while and stayed at it a hadn't known anything else is going over"
    print("Sphinx thinks you said " + extract_string)

    match = re.search(r'my name is (\w+)', extract_string)
    # If-statement after search() tests if it succeeded
    if match:                      
        bio = match.group()
        name = match.group(1)
        print('found', bio) ## 'found word:cat'
        print('found', name) ## 'found word:cat'
    else:
        print('did not find')
        bio = "not really sure what (s)he said!"
        name = "unsure"
    cv2.imwrite("data/%s.jpg" % name, crop_img)     # save frame as JPEG file
    cv2.imwrite("data/%sfull.jpg" % name, frame)     # save frame as JPEG file
    with open("people.csv", "a+") as f:
        f.write(match.group(1)
                + ","
                + "data/%s.jpg" % name
                + ","
                + bio
                + "\n");

except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

## recognize speech using Google Speech Recognition
#try:
#    # for testing purposes, we're just using the default API key
#    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#    # instead of `r.recognize_google(audio)`
#    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
#except sr.UnknownValueError:
#    print("Google Speech Recognition could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from Google Speech Recognition service; {0}".format(e))
#
## recognize speech using Google Cloud Speech
#GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
#try:
#    print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
#except sr.UnknownValueError:
#    print("Google Cloud Speech could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from Google Cloud Speech service; {0}".format(e))
#
## recognize speech using Wit.ai
#WIT_AI_KEY = "INSERT WIT.AI API KEY HERE"  # Wit.ai keys are 32-character uppercase alphanumeric strings
#try:
#    print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
#except sr.UnknownValueError:
#    print("Wit.ai could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from Wit.ai service; {0}".format(e))
#
## recognize speech using Microsoft Bing Voice Recognition
#BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
#try:
#    print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
#except sr.UnknownValueError:
#    print("Microsoft Bing Voice Recognition could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
#
## recognize speech using Houndify
#HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE"  # Houndify client IDs are Base64-encoded strings
#HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE"  # Houndify client keys are Base64-encoded strings
#try:
#    print("Houndify thinks you said " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
#except sr.UnknownValueError:
#    print("Houndify could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from Houndify service; {0}".format(e))
#
## recognize speech using IBM Speech to Text
#IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
#IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
#try:
#    print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
#except sr.UnknownValueError:
#    print("IBM Speech to Text could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from IBM Speech to Text service; {0}".format(e))
