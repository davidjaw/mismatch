import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.figure as fig
import matplotlib.axes as ax
import matplotlib.pyplot as plt


def sum_a2b(a, b, g_list, g_size, random_index):
    result = np.zeros(shape=g_size)
    for i in range(a, b):
        for j in range(g_size):
            result[j] += g_list[i, random_index[i, j]]
    return result


def get_distribution_description(name, dis):
    return f'{name} ($\mu=${dis.mean():.3f}, $\sigma=${dis.std() * 300:.3f}%)'


def main(args):
    np.random.seed(9527 + 7)

    level = 16
    # 讀取參數
    mu, sigma, size = 1, args.g_sigma, args.g_size

    gaussian_list = [np.random.normal(mu, sigma / 3, size) for _ in range(level)]
    gaussian_list = np.asarray(gaussian_list)
    # create a figure and axes
    figure = fig.Figure()
    axes = [[ax.Axes(figure, [0, 0, 1, 1]) for j in range(4)] for i in range(3)]
    for i in range(3):
        for j in range(4):
            figure.add_axes(axes[i][j])

    # plot the histograms
    for i in range(3):
        for j in range(4):
            axes[i][j].hist(gaussian_list[i], bins=100)

    # add a title to the figure
    figure.suptitle('List of histograms')
    # save the plot to a file
    figure.savefig('histograms.png')
    
    # get random index of each gaussian
    random_index = np.random.randint(0, size, [level, size])

    # get p_max
    p_max = sum_a2b(0, args.max_code, gaussian_list, args.g_size, random_index)
    # create a figure and axes for the p_max histogram
    figure_pmax = fig.Figure()
    axes_pmax = ax.Axes(figure_pmax, [0, 0, 1, 1])
    figure_pmax.add_axes(axes_pmax)
    # plot the p_max histogram
    axes_pmax.hist(p_max, bins=100)
    # add a title to the figure
    figure_pmax.suptitle(get_distribution_description('p_max', p_max))
    # save the plot to a file
    figure_pmax.savefig('p_max_histogram.png')
    
    # get n_max
    n_max = sum_a2b(args.max_code, level, gaussian_list, args.g_size, random_index)
    # create a figure and axes for the n_max histogram
    figure_nmax = fig.Figure()
    axes_nmax = ax.Axes(figure_nmax, [0, 0, 1, 1])
    figure_nmax.add_axes(axes_nmax)
    # plot the n_max histogram
    axes_nmax.hist(n_max, bins=100)
    # add a title to the figure
    figure_nmax.suptitle(get_distribution_description('n_max', n_max))
    # save the plot to a file
    figure_nmax.savefig('n_max_histogram.png')

    total_max = p_max - n_max

    p_min = sum_a2b(0, args.min_code, gaussian_list, args.g_size, random_index)
    # create a figure and axes for the p_min histogram
    figure_pmin = fig.Figure()
    axes_pmin = ax.Axes(figure_pmin, [0, 0, 1, 1])
    figure_pmin.add_axes(axes_pmin)
    # plot the p_min histogram
    axes_pmin.hist(p_min, bins=100)
    # add a title to the figure
    figure_pmin.suptitle(get_distribution_description('p_min', p_min))
    # save the plot to a file
    figure_pmin.savefig('p_min_histogram.png')
    
    # get n_min
    n_min = sum_a2b(args.min_code, level, gaussian_list, args.g_size, random_index)
    # create a figure and axes for the n_min histogram
    figure_nmin = fig.Figure()
    axes_nmin = ax.Axes(figure_nmin, [0, 0, 1, 1])
    figure_nmin.add_axes(axes_nmin)
    # plot the n_min histogram
    axes_nmin.hist(n_min, bins=100)
    # add a title to the figure
    figure_nmin.suptitle(get_distribution_description('n_min', n_min))
    # save the plot to a file
    figure_pmin.savefig('n_min_histogram.png')

    total_min = p_min - n_min

    total_mismatch = total_max + total_min
    total_mismatch /= 12

    # create a figure and axes for the total maximum histogram
    figure_max = fig.Figure()
    axes_max = ax.Axes(figure_max, [0, 0, 1, 1])
    figure_max.add_axes(axes_max)
    # plot the total maximum histogram
    axes_max.hist(total_max, bins=100)
    # add a title to the figure
    axes_max.set_title(f'total maximum ($\mu$={total_max.mean():.3f}, $\sigma$={total_max.std() * 300:.3f}%)')
    # save the plot to a file
    figure_max.savefig('total_max_histogram.png')

    # create a figure and axes for the total minimum histogram
    figure_min = fig.Figure()
    axes_min = ax.Axes(figure_min, [0, 0, 1, 1])
    figure_min.add_axes(axes_min)
    # plot the total minimum histogram
    axes_min.hist(total_min, bins=100)
    # add a title to the figure
    axes_min.set_title(f'total minimum ($\mu$={total_min.mean():.3f}, $\sigma$={total_min.std() * 300:.3f}%)')
    # save the plot to a file
    figure_min.savefig('total_min_histogram.png')

    # create a figure and axes for the total mismatch histogram
    figure_mismatch = fig.Figure()
    axes_mismatch = ax.Axes(figure_mismatch, [0, 0, 1, 1])
    figure_mismatch.add_axes(axes_mismatch)
    # plot the total mismatch histogram
    axes_mismatch.hist(total_mismatch, bins=100)
    # add a title to the figure
    axes_mismatch.set_title(f'total mismatch ($\mu$={total_mismatch.mean():.3f}, $\sigma$={total_mismatch.std() * 300:.3f}%)')
    # save the plot to a file
    figure_mismatch.savefig('total_mismatch_histogram.png')


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_code', default=14, type=int, help='max code')
    parser.add_argument('--min_code', default=2, type=int, help='min code')
    parser.add_argument('--g_size', default=10000, type=int, help='how many samples to produce')
    parser.add_argument('--g_sigma', type=float, help='sigma to test')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arg())
