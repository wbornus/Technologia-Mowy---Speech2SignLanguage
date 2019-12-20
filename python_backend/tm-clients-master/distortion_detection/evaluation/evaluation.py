import eval_utils

if __name__ == '__main__':
    directory = '../../dictation_data/dictation_data.wav'
    eval_utils.predict_and_visualize(directory, frame_length=0.025)