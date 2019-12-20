import numpy as np
import pickle


def get_mixture_params(model_type='dist'):
    model = pickle.load(open('../models/model_' + model_type + '.sav', 'rb'))
    weights = model.weights_
    means = model.means_
    std_devs = []
    for i in range(model.covariances_.shape[0]):
        std_devs.append(np.sqrt(model.covariances_[i, 0]))
        n_mixtures = model.covariances_.shape[0]

    return weights, means, std_devs, n_mixtures


def visualize_density():
    import scipy.stats as stats
    import matplotlib.pyplot as plt

    model_clean_params = get_mixture_params(model_type='clean')
    model_dist_params = get_mixture_params(model_type='dist')
    field = np.linspace(-1.2, 1.2, 1000)

    gaussian_mixture_clean = np.zeros(len(field))
    gaussian_mixture_dist = np.zeros(len(field))

    for it in range(len(model_clean_params[0])):
        tmp_clean = (model_clean_params[0][it]*stats.norm.pdf(field,
                                        model_clean_params[1][it], model_clean_params[2][it]))
        gaussian_mixture_clean += tmp_clean

        tmp_dist = (model_dist_params[0][it] * stats.norm.pdf(field,
                                        model_dist_params[1][it], model_dist_params[2][it]))
        gaussian_mixture_clean += tmp_clean
        gaussian_mixture_dist += tmp_dist

    if max(gaussian_mixture_clean) >= max(gaussian_mixture_dist):
        max_peak = max(gaussian_mixture_clean)
    else:
        max_peak = max(gaussian_mixture_dist)

    plt.subplot(2, 1, 1)
    plt.title('Gaussian Mixtures Probability Density\nmodel_type: clean')
    plt.plot(field, gaussian_mixture_clean)
    plt.ylim([0, max_peak + 2])
    plt.subplot(2, 1, 2)
    plt.title('Gaussian Mixtures Probability Density\nmodel_type: dist')
    plt.plot(field, gaussian_mixture_dist)
    plt.ylim([0, max_peak + 2])
    plt.show()


if __name__ == '__main__':
    visualize_density()


