import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import KFold
import utils
import pickle

data = np.load('../data_preprocessing/train_data.npz', allow_pickle=True)

clean_data, dist_data = data['clean_data'], data['dist_data']


clean_labels = np.zeros(len(clean_data), dtype=bool)
dist_labels = np.ones(len(dist_data), dtype=bool)

random_state = 1
acc_vector = []
x_valid = KFold(n_splits = 5)

model_clean_list = []
model_dist_list = []

for train_idxs, test_idxs in x_valid.split(clean_data):

    train_clean_data = clean_data[train_idxs]
    X_clean = np.concatenate((clean_data[:]), axis=0)
    X_clean = np.expand_dims(X_clean, axis=1)
    X_dist = np.concatenate((dist_data[:]), axis=0)
    X_dist = np.expand_dims(X_dist, axis=1)
    train_dist_data = dist_data[train_idxs]
    valid_data = np.concatenate((clean_data[test_idxs], dist_data[test_idxs]), axis=0)
    valid_labels = np.concatenate((clean_labels[test_idxs], dist_labels[test_idxs]), axis=0)

    model_clean = GaussianMixture(n_components=11, covariance_type='diag',
                                  max_iter=10, n_init=1, random_state=random_state,
                                    tol=5*1e-2)
    model_dist = GaussianMixture(n_components=11, covariance_type='diag',
                                 max_iter=10, n_init=1, random_state=random_state,
                                    tol=5*1e-2)

    model_clean.fit(X_clean)
    model_dist.fit(X_dist)

    model_clean_list.append(model_clean)
    model_dist_list.append(model_dist)

    acc = utils.validate(valid_data, valid_labels, model_clean, model_dist)
    acc_vector.append(acc)
    print('%0.4f' % acc)

print('mean_acc: %0.4f' % np.mean(acc_vector))

best_model_idx = np.argmax(acc_vector)
pickle.dump(model_clean_list[best_model_idx], open('./models/model_clean.sav', 'wb'))
pickle.dump(model_dist_list[best_model_idx], open('./models/model_dist.sav', 'wb'))



