import os

from matplotlib import font_manager, text, pyplot
import matplotlib
import numpy as np

from .mds import calculate_positions


def plot_with_labels(positions, labels):
    #to show Japanese sentences
    matplotlib.rcParams['font.family'] = 'IPAexGothic'

    pyplot.subplots_adjust(bottom=0.1)
    pyplot.scatter(positions[:, 0], positions[:, 1], marker = 'o')

    for label, position in zip(labels, positions):
        pyplot.annotate(
            label, xy=position,
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
        )
    pyplot.show()


def plot(path_feature_map):
    features = []
    filenames = []
    for path, feature in path_feature_map.items():
        features.append(feature)

        filename = os.path.basename(path)
        filenames.append(filename)

    features = np.array(features)
    indices = np.random.randint(low=0, high=len(features), size=20)
    features = np.take(features, indices, axis=0)
    filenames = np.take(filenames, indices)

    positions = calculate_positions(features)
    plot_with_labels(positions, filenames)
