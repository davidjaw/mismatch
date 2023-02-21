import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
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
    # show generated his
    fig = plt.figure()
    axs = []
    for i in range(3):
        for j in range(4):
            ax = fig.add_subplot(3, 4, i * 4 + j + 1)
            if len(axs) < i + 1:
                axs.append([])
            axs[i].append(ax)
    for i in range(3):
        for j in range(4):
            axs[i][j].hist(gaussian_list[i], bins=100)
    fig.suptitle('List of histograms')
    fig.tight_layout()
    fig.savefig('Gaussians.png', dpi=300)

    # get random index of each gaussian
    random_index = np.random.randint(0, size, [level, size])

    # get p_max
    p_max = sum_a2b(0, args.max_code, gaussian_list, args.g_size, random_index)
    # show generated his
    fig = plt.figure()
    axs = fig.add_subplot(1, 1, 1)
    axs.hist(p_max, bins=100)
    fig.suptitle(get_distribution_description('p_max', p_max))
    fig.savefig('p_max.png', dpi=300)
    # get n_max
    n_max = sum_a2b(args.max_code, level, gaussian_list, args.g_size, random_index)
    # show generated his
    fig = plt.figure()
    axs = fig.add_subplot(1, 1, 1)
    axs.hist(n_max, bins=100)
    fig.suptitle(get_distribution_description('n_max', n_max))
    fig.savefig('n_max')

    total_max = p_max - n_max

    p_min = sum_a2b(0, args.min_code, gaussian_list, args.g_size, random_index)
    # show generated his
    fig = plt.figure()
    axs = fig.add_subplot(1, 1, 1)
    axs.hist(p_min, bins=100)
    fig.suptitle(get_distribution_description('p_min', p_min))
    fig.savefig('p_min.png', dpi=300)

    # get n_min
    n_min = sum_a2b(args.min_code, level, gaussian_list, args.g_size, random_index)
    # show generated his
    fig = plt.figure()
    axs = fig.add_subplot(1, 1, 1)
    axs.hist(n_min, bins=100)
    fig.suptitle(get_distribution_description('n_min', n_min))
    fig.savefig('n_min.png', dpi=300)

    total_min = p_min - n_min

    total_mismatch = total_max + total_min
    total_mismatch /= 12

    fig = plt.figure()
    axs = [fig.add_subplot(3, 1, i + 1) for i in range(3)]
    axs[0].hist(total_max, bins=100)
    axs[0].set_title(f'total maximum ($\mu$={total_max.mean():.3f}, $\sigma$={total_max.std() * 300:.3f}%)')
    axs[1].hist(total_min, bins=100)
    axs[1].set_title(f'total minimum ($\mu$={total_min.mean():.3f}, $\sigma$={total_min.std() * 300:.3f}%)')
    axs[2].hist(total_mismatch, bins=100)
    axs[2].set_title(f'total mismatch ($\mu$={total_mismatch.mean():.3f}, $\sigma$={total_mismatch.std() * 300:.3f}%)')
    fig.tight_layout()
    fig.savefig('total_mismatch.png', dpi=300)


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_code', default=14, type=int, help='max code')
    parser.add_argument('--min_code', default=2, type=int, help='min code')
    parser.add_argument('--g_size', default=10000, type=int, help='how many samples to produce')
    parser.add_argument('--g_sigma', default=.03, type=float, help='sigma to test')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arg())
