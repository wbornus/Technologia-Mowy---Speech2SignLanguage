#!/usr/bin/env python3
# coding=utf-8
from dictation.dictation_client import create_audio_stream, print_results
from dictation.service.dictation_settings import DictationSettings
from dictation.service.streaming_recognizer import StreamingRecognizer
from address_provider import AddressProvider
from os.path import join as opjoin
from dictation.dictation_client import play_gif, mic_to_directory, search_over_phrases
from dictation.dictation_client import levenshtein_classification, get_phrases
import distortion_detection.distortion_detection as dd
import time

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



def record():
    key_phrases = ['brzuch', 'gardło', 'głowa', 'serce', 'dzień_dobry', 'gorączka', 'grypa',
               'kardiolog', 'katar', 'neurolog', 'ortopeda', 'przeziębienie', 'lekarz', 'zapalenie_płuc',
               'samopoczucie']

    gif_dir = 'err.gif'
    phrases = get_phrases()
    print(phrases)
    print("speak: ")
    if __name__ == '__main__':

        directory = 'dictation_data/dictation_data.wav'

        while True:
            mic_to_directory(file_directory=directory)  # recording voice sample
            args = DictationArgs(directory)
            mazzny_condition = dd.is_distorted(file_directory=directory)
            if not mazzny_condition:
                break
            else:
                print('Please speak more quietly or try moving away from the microphone')
                time.sleep(3)
                print('speak: ')

        if args.wave is not None or args.mic:
            with create_audio_stream(args) as stream:
                settings = DictationSettings(args)
                recognizer = StreamingRecognizer(args.address, settings)
                print('Recognizing...')
                results = recognizer.recognize(stream)
                print_results(results)
                results_str = results[0]['transcript']

                idx = search_over_phrases(results_str, phrases)
                print(idx)
                print(key_phrases[idx])
                if idx != -1:
                    gif_dir = 'gifs/' + key_phrases[idx] + '.gif'
                    # gif_dir = 'gifs/500x500_sample(brak).gif'
                    print(gif_dir)
                    play_gif(gif_dir)
                elif idx == -1:
                    idx = levenshtein_classification(results_str, phrases)
                    print(key_phrases[idx])
                    gif_dir = 'gifs/' + key_phrases[idx] + '.gif'
                    # gif_dir = 'gifs/500x500_sample(brak).gif'
                    print(gif_dir)
                    #play_gif(gif_dir)

    return gif_dir

