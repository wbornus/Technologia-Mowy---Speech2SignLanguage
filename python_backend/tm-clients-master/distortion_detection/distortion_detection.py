import pickle
import numpy as np
from scipy.io import wavfile


def is_distorted(file_directory='./dictation_data/dictation_data.wav', frame_length=0.100):
    """
    function detecting distiortion in speech signal
    :param data: data chunk to verify - Mono track vector
    :param frame_length: time length of individual sample (seconds)
    :return: boolean: True - distortion occures in signal, False - no distortion in signal
    """
    fs, data = wavfile.read(file_directory)
    model_clean = pickle.load(open('./distortion_detection/training_validation/models/model_clean.sav', 'rb'))
    model_dist = pickle.load(open('./distortion_detection/training_validation/models/model_dist.sav', 'rb'))

    n_samples = int(frame_length * fs // 1)
    zero_padd_len = int(len(data) % n_samples)
    zero_padd = np.zeros(zero_padd_len, dtype=float)
    long_data = np.concatenate((data.astype(np.float), zero_padd), axis=0)   #making sure the signal does't go
    long_data_normalized = long_data / max(abs(long_data))                     #out of range in the loop below
    dist_arr = []
    for sample_idx in range(int(len(long_data_normalized) // n_samples) - 1):
        data_frame = long_data_normalized[sample_idx * n_samples: (sample_idx + 1) * n_samples]  # sample to classify
        data_frame = np.expand_dims(data_frame, axis=1)

        clean_score = model_clean.score(data_frame)
        dist_score = model_dist.score(data_frame)

        if dist_score > clean_score:
            dist_arr.append(True)
        else:
            dist_arr.append(False)

    if sum(dist_arr) > 0.25*len(dist_arr):
        return True
    else:
        return False
