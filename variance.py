#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division


def variance(x):
    """
    Compute the sample variance of the elements in x[1..n] using Welford's
    recurrence formula:

    Initialize M_1 = x_1 and S_1 = 0.

    For subsequent x's, use the recurrence formulas

    M_k = M_{k-1} + (x_k - M_{k-1}) / k
    S_k = S_{k-1} + (x_k - M_{k-1}) * (x_k - M_k).

    For 2 ≤ k ≤ n, the k-th estimate of the variance is s^2 = S_k/(k - 1).

    Source: http://www.johndcook.com/standard_deviation.html

    >>> variance([1, 1])
    (1.0, 0.0)
    >>> variance([1, 2])
    (1.5, 0.5)
    >>> variance([1, 2, 3])
    (2.0, 1.0)
    >>> variance([1e10, 1, -1e10])
    (0.33333301544189453, 9.999999999999998e+19)
    """
    assert(len(x) >= 2)

    mean = x[0]  # the mean of x[1..1]
    var = 0      # the variance of x[1..1]

    n = len(x)

    for i in range(1, n):
        new_mean = mean + (x[i] - mean) / (i + 1)
        new_var = var + (x[i] - mean) * (x[i] - new_mean)

        mean = new_mean
        var = new_var

    return (mean, var/(n-1))
