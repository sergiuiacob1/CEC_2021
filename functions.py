import numpy as np
import math
from math import sin


class Functions:
    bentCigarRange = [-100, 100]

    @staticmethod
    def bent_cigar(values):
        return values[0]**2+10**6*np.sum(np.array(values[1:])**2)

    deJong1DimRange = [-100, 100]

    @staticmethod
    def deJong1(values):
        '''Function: De Jong 1'''
        s = 0
        for v in values:
            s += v ** 2
        return(s)

    rastriginDimRange = [-100, 100]

    @staticmethod
    def rastrigin(values):
        '''Function: Rastrigin'''
        return np.sum(np.power(values, 2) - 10 * np.cos(2 * math.pi * values)) + 10 * len(values)

    high_conditioned_elliptic_dim_range = [-100, 100]

    @staticmethod
    def high_conditioned_elliptic(values):
        '''Function: High Conditioned Elliptic function'''
        constant = 10**6
        indexes = np.arange(0, len(values))
        indexes = indexes / (len(values) - 1)
        return np.sum(constant ** (indexes) * np.array(values) ** 2)

    # axis-parallel hyper-ellipsoid
    apheDimRange = [-5.12, 5.12]

    @staticmethod
    def aphe(values):
        '''Function: Axis-parallel hyper-ellipsoid'''
        s = 0
        for ii, v in enumerate(values):
            s += (ii + 1) * v ** 2
        return(s)

    # rotated hyper-ellipsoid
    rheDimRange = [-65.536, 65.536]

    @staticmethod
    def rhe(values):
        '''Function: Rotated hyper-ellipsoid'''
        s = 0
        for ii in range(len(values)):
            ps = 0
            for jj in range(ii + 1):
                ps += values[jj]
            s += ps ** 2
        return(s)

    # Moved axis parallel hyper-ellipsoid
    mapheDimRange = [-5.12, 5.12]

    @staticmethod
    def maphe(values):
        '''Function: Moved axis-parallel hyper-ellipsoid'''
        s = 0
        for ii, x in enumerate(values):
            s += 5 * ii * x ** 2
        return(s)

    # Rosenbrock's Valley (DeJong 2)
    rosenbrockDimRange = [-2.048, 2.048]

    @staticmethod
    def rosenbrock(values):
        '''Function: Rosenbrock'''
        s = 0
        for ii in range(len(values) - 1):
            s += 100 * (values[ii + 1] - values[ii]
                        ** 2)**2 + (1 - values[ii])**2
        return(s)

    # Schwefel's Function
    schwefelDimRange = [-500, 500]

    @staticmethod
    def schwefel(values):
        '''Function: Schwefel'''
        s = 0
        for v in values:
            s -= v * sin(math.sqrt(abs(v)))
        return(s)

    # Griewangk's Function
    griewangkDimRange = [-600, 600]
    griewangkDimRange2 = [-50, 50]
    griewangkDimRange3 = [-10, 10]

    @staticmethod
    def griewangk(values):
        '''Function: Griewangk'''
        s = 0
        p = 1
        for ii, v in enumerate(values):
            s += v ** 2
            p *= math.cos(v / math.sqrt(1 + ii))
        s /= 4000
        s = s - p + 1
        return(s)

    # Sum of different powers
    sdpDimRange = [-1, 1]

    @staticmethod
    def sdp(values):
        '''Function: Sum of different powers'''
        s = 0
        for ii, v in enumerate(values):
            s += abs(v) ** (ii + 2)
        return(s)

    # Ackley's Path function
    ackleyDimRange = [-32.768, 32.768]
    ackleyDimRange2 = [-2, 2]

    @staticmethod
    def ackley(values):
        '''Function: Ackley'''
        tau = math.tau
        a = 20
        b = 0.2
        s1 = 0
        s2 = 0
        n = len(values)
        for v in values:
            s1 += v ** 2
            s2 += math.cos(tau * v)
        e1 = -b * math.sqrt(s1 / n)
        e2 = s2 / n
        s = -a * math.exp(e1) - math.exp(e2) + a + math.exp(1)
        return(s)

    # Langermann's function
    langermannDimRange = [0, 10]
    langermannDimRange2 = [-2, 12]  # for better feature framing

    @staticmethod
    def langermann(values):
        '''Function: Langermann'''
        a = [[3, 5, 2, 1, 7], [5, 2, 1, 4, 9]]
        c = [1, 2, 5, 2, 3]
        m = len(c)
        n = len(a)
        l = len(values)
        pi = math.pi
        s = 0
        for ii in range(m):
            s1 = 0
            for jj in range(l):
                s1 += (values[jj] - a[jj % n][ii]) ** 2
            s += c[ii] * math.exp(-s1 / pi) * math.cos(pi * s1)
        return(s)

    # Michalewicz function
    michalewiczDimRange = [0, math.pi]

    @staticmethod
    def michalewicz(values):
        '''Function: Michalewicz'''
        m = 10
        m2 = 2 * m
        pi = math.pi
        s = 0
        for ii, v in enumerate(values):
            s -= math.sin(v) * (math.sin((ii + 1) * v ** 2 / pi)) ** m2
        return(s)
