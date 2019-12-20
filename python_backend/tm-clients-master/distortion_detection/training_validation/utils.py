import numpy as np

def validate(data, labels,  model_clean, model_dist):
    """

    :param data: data tensor
    :param labels: corresponding label for each data tensor (boolean) 0 - clean, 1 - distorted
    :param model_clean:
    :param model_dist:
    :return: acuracy of prediction (list)
    """
    scores_clean = []
    scores_dist = []
    pred_vector = []
    correct_preds = 0
    scores_subtraction = []
    for data_frame, label in zip(data, labels):
        data_frame = np.expand_dims(data_frame, axis=1)
        score_clean = model_clean.score(data_frame)
        score_dist = model_dist.score(data_frame)
        if score_clean > score_dist:
            prediction = False
        else:
            prediction = True

        if prediction == label:
            correct_preds += 1

    # print('labels:', labels)
    # print('prec_vector:', pred_vector)

    return correct_preds / len(data)