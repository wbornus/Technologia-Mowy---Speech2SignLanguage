#!/usr/bin/env python3
# coding=utf-8
from dictation.dictation_client import create_audio_stream, print_results
from dictation.service.dictation_settings import DictationSettings
from dictation.service.streaming_recognizer import StreamingRecognizer
from address_provider import AddressProvider
from os.path import join as opjoin
import pyaudio
from scipy.io import wavfile
import numpy as np
import pandas as pd
from dictation.dictation_client import play_gif as play_gif

class DictationArgs:

    def __init__(self, wav_filepath=None):
        if wav_filepath:
            self.wave = opjoin(wav_filepath) # Path to wave file with speech to be recognized. Should be mono, 8kHz or 16kHz.
        else:
            self.wave = None
        ap = AddressProvider()
        self.address = ap.get("dictation")
        self.interim_results = False  # If set - messages with temporal results will be shown.
        self.mic = False  # Use microphone as an audio source (instead of wave file).
        self.no_input_timeout = 5000  # MRCP v2 no input timeout [ms].
        self.recognition_timeout = 15000  # MRCP v2 recognition timeout [ms].
        self.session_id = None  # Session ID to be passed to the service. If not specified, the service will generate a default session ID itself.
        self.single_utterance = False  # If set - the recognizer will detect a single spoken utterance.
        self.speech_complete_timeout = 5000  # MRCP v2 speech complete timeout [ms].
        self.speech_incomplete_timeout = 6000  # MRCP v2 speech incomplete timeout [ms].
        self.time_offsets = False  # If set - the recognizer will return also word time offsets.


def mic_to_directory(directory='./dictation_data/dictation_data.wav', record_time=3):
    RATE = 16000
    CHUNK = 16000 * record_time

    p = pyaudio.PyAudio()

    # stream = p.open(format=pyaudio.paInt16,
    #                 channels=1,
    #                 rate=RATE,
    #                 output=True)  # stream wyjsciowy (odtwarzany na sluchawkach)
    mic_stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    # stream.write(mic_stream.read(CHUNK))  # odtworzenie zapisanych danych
    #    data = audio_file.readframes(CHUNK)
    # dla odczytu z pliku
    data = mic_stream.read(CHUNK)  # wczytanie danych z mikrofonu
    data = np.frombuffer(data, dtype=np.int16)
    wavfile.write(directory, data=data, rate=RATE)

def search_over_phrases(results_str, phrases):
    """
    :param results_str: string recognized from dictation
    :param phrases: phrases to search over
    :return: idx: index of key_phrase for gif to be displayed
    """
    is_found = False
    for idx in range(len(phrases)):
        for phrase in phrases[idx]:
            if results_str == phrase:
                is_found = True
                return idx
    if is_found == False:
        return -1


key_phrases = ['brzuch', 'gardło', 'głowa', 'serce', 'dzień_dobry', 'gorączka', 'grypa_żołądkowa',
               'kardiolog', 'katar', 'neurolog', 'ortopeda', 'przeziębienie', 'lekarz', 'zapalenie_płuc',
               'samopoczucie']

df = pd.read_csv('phrases.csv')

phrases = pd.DataFrame(df).to_numpy()

phrases_clean = []
for row in phrases:
    tmp_row = []
    for column in row:
        if type(column) == str:
            tmp_row.append(column)
        print(type(column))
    phrases_clean.append(tmp_row)

phrases = np.array(phrases_clean)

print("speak: ")
if __name__ == '__main__':


    directory = './dictation_data/dictation_data.wav'

    mic_to_directory()  #recording voice sample
    args = DictationArgs(directory)
    #args = DictationArgs()


    if args.wave is not None or args.mic:
        with create_audio_stream(args) as stream:
            settings = DictationSettings(args)
            recognizer = StreamingRecognizer(args.address, settings)
            print('Recognizing...')
            results = recognizer.recognize(stream)
            print_results(results)
            results_str = results[0]['transcript']
            idx = search_over_phrases(results_str, phrases)
            if idx != -1:
                gif_dir = 'gifs/'+key_phrases[idx]+'gif'
                play_gif(directory)
            else:
                idx = levenshtein_classification(results_str, phrases)



