import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import pickle

def predict_and_visualize(directory, frame_length = 0.100):
    model_clean = pickle.load(open('../training_validation/models/model_clean.sav', 'rb'))
    model_dist = pickle.load(open('../training_validation/models/model_dist.sav', 'rb'))

    fs, data = wavfile.read(directory)
    n_samples = int(frame_length*fs // 1)
    zero_padd_len = int(len(data) % n_samples)
    zero_padd = np.zeros(zero_padd_len, dtype=float)
    long_data = np.concatenate((data.astype(np.float), zero_padd), axis=0)
    long_data_normalized = long_data / max(abs(long_data))

    for sample_idx in range(int(len(long_data_normalized) // n_samples) - 1):

        t = np.linspace(sample_idx * n_samples / fs, (sample_idx + 1) * n_samples / fs, n_samples) #time linspace
        data_frame = long_data_normalized[sample_idx*n_samples: (sample_idx + 1)*n_samples] #sample to classify
        data_frame = np.expand_dims(data_frame, axis=1)

        clean_score = model_clean.score(data_frame)
        dist_score = model_dist.score(data_frame)

        if clean_score > dist_score:
            plt.plot(t, long_data[sample_idx*n_samples: (sample_idx + 1)*n_samples], 'g')
        else:
            plt.plot(t, long_data[sample_idx*n_samples: (sample_idx + 1)*n_samples], 'r')
    plt.ylim([(-1)*(2**15), 2**15])
    plt.show()

