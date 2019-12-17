#!/usr/bin/python3
from argparse import ArgumentParser
from audio_source import AudioStream
from mic_source import MicrophoneStream
from service.dictation_settings import DictationSettings
from service.streaming_recognizer import StreamingRecognizer
from DICTATION_CLIENT_VERSION import DICTATION_CLIENT_VERSION
import pyaudio
import numpy as np
from scipy.io import wavfile
import Levenshtein


def print_results(results):
    for res in results:
        print("{}".format(res['transcript']))
        words = res['transcript'].split()
        ali = res['alignment']
        if len(words) == len(ali):
            for i in range(0, len(words)):
                time = ali[i]
                if len(time) > 0:
                    print("{} [{}.{:02d} - {}.{:02d}]".format(words[i], time[0].seconds, int(time[0].nanos / 10000000),
                                                          time[1].seconds, int(time[1].nanos / 10000000)))


def return_results(results):
    for res in results:
        print("{}".format(res['transcript']))
        words = res['transcript'].split()
        ali = res['alignment']
        if len(words) == len(ali):
            for i in range(0, len(words)):
                time = ali[i]
                if len(time) > 0:
                    return ("{} [{}.{:02d} - {}.{:02d}]".format(words[i], time[0].seconds, int(time[0].nanos / 10000000),
                                                          time[1].seconds, int(time[1].nanos / 10000000)))


def get_phrases(directory = './phrases/phrases.csv'):
    import pandas as pd
    import numpy as np
    df = pd.read_csv('./phrases/phrases.csv', header=None)

    phrases = pd.DataFrame(df).to_numpy()

    phrases_clean = []
    for row in phrases:
        tmp_row = []
        for column in row:
            if type(column) == str:
                tmp_row.append(column)
            # print(type(column))
        phrases_clean.append(tmp_row)
    phrases = np.array(phrases_clean)

    return phrases

def play_gif(directory):
    import pyglet
    # pick an animated gif file you have in the working directory
    ag_file = directory
    animation = pyglet.resource.animation(ag_file)
    sprite = pyglet.sprite.Sprite(animation)
    # create a window and set it to the image size
    win = pyglet.window.Window(width=sprite.width, height=sprite.height)
    # set window background color = r, g, b, alpha
    # each value goes from 0.0 to 1.0
    green = 0, 1, 0, 1
    pyglet.gl.glClearColor(*green)
    @win.event
    def on_draw():
        win.clear()
        sprite.draw()
    pyglet.app.run()


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

def levenshtein_classification(results_str, phrases):
    """
    :param results_str: result of speech recognition
    :param phrases: phrases to calculate levenshtein distance
    :return: idx of key phrase
    """
    #function yet to be implemented!

    is_found = False
    dist_arr = []
    for idx in range(len(phrases)):
        tmp_arr = []
        for phrase in phrases[idx]:
            tmp_arr.append(Levenshtein.distance(results_str, phrase))
        dist_arr.append(tmp_arr)
    dist_arr = np.array(dist_arr)
    idx = np.argmin(dist_arr)
    print(idx)
    return idx


def mic_to_directory(file_directory='./dictation_data/dictation_data.wav', record_time=3):
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
    wavfile.write(file_directory, data=data, rate=RATE)


def create_audio_stream(args):
    # create wave file stream
    if args.wave is not None:
        return AudioStream(args.wave)

    # create microphone stream
    if args.mic:
        rate = 16000  # [Hz]
        chunk = int(rate / 10)  # [100 ms]
        return MicrophoneStream(rate, chunk)

    # default
    raise ValueError("Unknown media source to create")


if __name__ == '__main__':
    print("Dictation ASR gRPC client " + DICTATION_CLIENT_VERSION)

    parser = ArgumentParser()
    parser.add_argument("--service-address", dest="address", required=True,
                        help="IP address and port (address:port) of a service the client will connect to.", type=str)
    parser.add_argument("--wave-path", dest="wave",
                        help="Path to wave file with speech to be recognized. Should be mono, 8kHz or 16kHz.")
    parser.add_argument("--mic", help="Use microphone as an audio source (instead of wave file).", action='store_true')
    parser.add_argument("--session-id",
                        help="Session ID to be passed to the service. If not specified, the service will generate a default session ID itself.",
                        default="", type=str)
    # request configuration section
    parser.add_argument("--max-alternatives", help="Maximum number of recognition hypotheses to be returned.",
                        default=1, type=int)
    parser.add_argument("--time-offsets", help="If set - the recognizer will return also word time offsets.",
                        action="store_true", default=False)
    parser.add_argument("--single-utterance", help="If set - the recognizer will detect a single spoken utterance.",
                        action="store_true", default=False)
    parser.add_argument("--interim-results", help="If set - messages with temporal results will be shown.",
                        action="store_true", default=False)
    # timeouts
    parser.add_argument("--no-input-timeout", help="MRCP v2 no input timeout [ms].", default=5000, type=int)
    parser.add_argument("--speech-complete-timeout", help="MRCP v2 speech complete timeout [ms].", default=2000,
                        type=int)
    parser.add_argument("--speech-incomplete-timeout", help="MRCP v2 speech incomplete timeout [ms].", default=4000,
                        type=int)
    parser.add_argument("--recognition-timeout", help="MRCP v2 recognition timeout [ms].", default=10000, type=int)

    # Stream audio to the ASR engine and print all hypotheses to standard output
    args = parser.parse_args()

    if args.wave is not None or args.mic:
        with create_audio_stream(args) as stream:
            settings = DictationSettings(args)
            recognizer = StreamingRecognizer(args.address, settings)

            print('Recognizing...')
            results = recognizer.recognize(stream)
            print_results(results)
