from matplotlib import font_manager, text, pyplot
import matplotlib


def plot_with_labels(positions, labels):
    #to show Japanese texts
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
