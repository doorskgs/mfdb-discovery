import math
import statistics
import math
from collections import defaultdict


def get_float_precision(f: float):
    """
    gets number of decimals for number
    :param f: float
    :return:
    """
    return len(str(f).split('.')[1])


def truncate_float(f, n) -> str:
    """
    :param f: float
    :param n: fixed decimal places to truncate
    :return: truncated, non-rounded float to N digits
    """
    D = get_digits(f)
    trun = str(f)
    strip_right = len(trun) - (D+1+n)

    if strip_right > 0:
        return trun[:-strip_right]
    elif strip_right < 0:
        return trun+''.join(['0']*abs(strip_right))
    return trun


def get_digits(n):
    return int(math.log10(n)) + 1


def cluster1d_fixed(points: list[float | int] | set[float | set]) -> list[set[float]]:
    # get common number of digits:
    common_digits = statistics.mode(map(get_digits, points))
    # get max, min float precision in set:
    min_prec = min(map(get_float_precision, filter(lambda f: get_digits(f) == common_digits, points)))
    #max_prec = max(map(get_float_precision, filter(lambda f: get_digits(f) == common_digits, points)))

    # dynamically determine epsilon for clustering:
    #eps = 10 * math.pow(10, -common_digits - min_prec)

    clusters: dict[str, set] = defaultdict(set)
    for f in points:
        clusters[truncate_float(f, min_prec)].add(f)

    return list(clusters.values())


def cluster1d_eps(points: list[float | int] | set[float | int], eps = 0.0005) -> list[set[float]]:
    """
    Clusters list of floats
    :param points: floats to be clustered
    :param eps: minimum difference for clustering
    :return: list of clusters with items
    """
    clusters = []

    points_sorted = sorted(points)
    curr_point = points_sorted[0]
    curr_cluster: set = {curr_point}

    for point in points_sorted[1:]:
        if point <= curr_point + eps:
            curr_cluster.add(point)
        else:
            clusters.append(curr_cluster)
            curr_cluster = {point}
        curr_point = point

    clusters.append(curr_cluster)

    return clusters

