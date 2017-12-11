#!/usr/bin/env python3

import speech_recognition as sr
from os import path
import time
import json
import os
import sys


def transcribe(speech_filepath, asr_system, settings, save_transcription=True):
    #print(speech_filepath)
    #sys.stdout.buffer.write(speech_filepath.encode('utf8'))
    '''
    print('speech_filepath: {0}'.format(speech_filepath))
    s='asr_system: {1}\tspeech_filepath: {0}'.format(speech_filepath,asr_system)
    print('asr_system: {1}\tspeech_filepath: {0}'.format(speech_filepath,asr_system))
    #sys.stdout.buffer.write(TestText2)

    #if 'A11BTJ8VWYCZFW_11187_TAKE_OUT_THE_LEDGE_ON_THE_BOTTOM_RIGHT_CORNER_OR_CROP_IT_SO' in speech_filepath: 1/0
    '''
    transcription_filepath_base = '.'.join(speech_filepath.split('.')[:-1]) + '_'  + asr_system
    transcription_filepath_text = transcription_filepath_base  + '.txt'
    transcription_filepath_json = transcription_filepath_base  + '.json'
    #if settings.getboolean('general','overwrite_transcriptions'): print('true')
    if not settings.getboolean('general','overwrite_transcriptions') and os.path.isfile(transcription_filepath_text):
        #print('Skipped speech file {0} because the file {1} already exists.'.format(speech_filepath,transcription_filepath_text))
        print('Change the setting `overwrite_transcriptions` to True if you want to overwrite existing transcriptions')
        return open(transcription_filepath_text, 'r').read()
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(speech_filepath) as source:
        audio = r.record(source)  # read the entire audio file

    '''
    # recognize speech using Sphinx
    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    '''
    transcription = ''
    asr_could_not_be_reached = False
    asr_timestamp_started = time.time()
    if asr_system == 'google':
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            transcription = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            asr_could_not_be_reached = True

    elif asr_system == 'googlecloud':
        # recognize speech using Google Cloud Speech
        GOOGLE_CLOUD_SPEECH_CREDENTIALS_filepath = settings.get('credentials','google_cloud_speech_credentials_filepath')
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = open(GOOGLE_CLOUD_SPEECH_CREDENTIALS_filepath, 'r').read()
        #json.loads(credentials_json)
        try:
            transcription = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
            #print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))
            asr_could_not_be_reached = True



    # recognize speech using Wit.ai
    elif asr_system == 'wit':
        WIT_AI_KEY = settings.get('credentials','wit_ai_key')
        print("Calling the Wit.ai API")
        try:
            transcription = r.recognize_wit(audio, key=WIT_AI_KEY)
            #print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))
            asr_could_not_be_reached = True

    # recognize speech using Microsoft Bing Voice Recognition
    elif asr_system == 'microsoft':
        BING_KEY = settings.get('credentials','bing_key')
        print('Calling the Microsoft Bing Voice Recognition API')
        try:
            transcription =  r.recognize_bing(audio, key=BING_KEY)
            #print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
        except sr.UnknownValueError:
            print("Microsoft Bing Voice Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
            asr_could_not_be_reached = True


    elif asr_system == 'houndify':
        # recognize speech using Houndify
        HOUNDIFY_CLIENT_ID = settings.get('credentials','houndify_client_id')
        HOUNDIFY_CLIENT_KEY = settings.get('credentials','houndify_client_key')

        print("Calling the Houndify API")
        try:
            transcription = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
            #print("Houndify thinks you said " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
        except sr.UnknownValueError:
            print("Houndify could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Houndify service; {0}".format(e))
            asr_could_not_be_reached = True

    # recognize speech using IBM Speech to Text
    elif asr_system == 'ibm':
        IBM_USERNAME = settings.get('credentials','ibm_username')
        IBM_PASSWORD = settings.get('credentials','ibm_password')
        try:
            transcription = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
            #print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
        except sr.UnknownValueError:
            print("IBM Speech to Text could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from IBM Speech to Text service; {0}".format(e))
            asr_could_not_be_reached = True

    else: raise ValueError("Invalid asr_system. asr_system = {0}".format(asr_system))

    asr_timestamp_ended = time.time()
    asr_time_elapsed = asr_timestamp_ended - asr_timestamp_started
    print('asr_time_elapsed: {0:.3f} seconds'.format(asr_time_elapsed))
    #time.sleep(2)   # Delay in seconds
    #if len(transcription) == 0 and asr_could_not_be_reached: return transcription

    if save_transcription:
        #print('Transcription saved in {0} and {1}'.format(transcription_filepath_text,transcription_filepath_json))
        open(transcription_filepath_text,'w').write(transcription)

    print('transcription: {0}'.format(transcription))
    results = {}
    results['transcription'] = transcription
    results['asr_time_elapsed'] = asr_time_elapsed
    results['asr_timestamp_ended'] = asr_timestamp_ended
    results['asr_timestamp_started'] = asr_timestamp_started


    json.dump(results, open(transcription_filepath_json, 'w'), indent = 4, sort_keys=True)

    return transcription



