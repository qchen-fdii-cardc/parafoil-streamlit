from parafoil.utils import max_rand_vec
from typing import Iterable
import numpy as np
from parafoil.parafoil import Parafoil
from parafoil.control import ControlStrategy

import scipy.interpolate as itp


class CollocationStrategy(ControlStrategy):
    def __init__(self, max_domega: float, collocation_points: Iterable) -> None:
        super().__init__(max_domega)
        self.collocation_points = np.asarray(collocation_points)
        self.parafoil: Parafoil
        self.n = len(self.collocation_points)

    @property
    def tp(self):
        if not "_tp" in self.__dict__:
            self._tp = np.linspace(0, self.parafoil.t_max, self.n)
        return self._tp

    def _control_from_input(self, input: np.ndarray) -> float:
        [t, xt, yt, omega, dt, winx, winy] = input
        if self.parafoil is None:
            raise ValueError("Parafoil not set")
        dt = np.abs(self.tp - t)
        i = np.argmin(dt)
        return self.collocation_points[i]


class FitCollocationStrategy(CollocationStrategy):
    def _fit(self, t) -> float:
        if not '_fit_curve' in self.__dict__:
            self._fit_curve = itp.CubicSpline(self.tp, self.collocation_points)
        return self._fit_curve(t).tolist()

    def _control_from_input(self, input: np.ndarray) -> float:
        [t, xt, yt, omega, dt, winx, winy] = input
        return self._fit(t)


class RandomCollocationStrategy(CollocationStrategy):
    def __init__(self, max_domega: float, n: int) -> None:
        d = np.abs(max_domega)
        super(RandomCollocationStrategy, self).__init__(
            *max_rand_vec(max_domega, n))
