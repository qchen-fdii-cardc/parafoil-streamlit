from typing import Iterable
import numpy as np


def to_mpi_pi(angle: float) -> float:
    """Returns the angle in the range [-pi,pi]

    Parameters
    ----------
    angle : float
      Angle in radians

    Returns
    -------
    float
      The angle in the range [-pi, pi]
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi


def max_rand_vec(max_value: float, n: int) -> tuple[float, Iterable]:
    """Generate a random vector of length n with values in [-max_value, max_value]."""
    assert (max_value > 0)

    return np.abs(max_value), np.random.rand(n) * max_value * 2 - max_value
