# This is a class for controlling the parafoil.
# t is the current time.
# y is the current state.
# winx and winy are the current position of the mouse.
# u is the output control.

import numpy as np


class ControlStrategy:
    def __init__(self, max_domega: float) -> None:
        self.max_domega = max_domega
        self._parafoil = None

    def __call__(self, input: np.ndarray) -> float:
        return self.control(input)

    def control(self, input: np.ndarray) -> float:
        """
        Get control value, now it's float, possible np.ndarray[float] in future.
        """
        return max(min(self._control_from_input(input), self.max_domega), -self.max_domega)

    def _control_from_input(self, input: np.ndarray) -> float:
        raise NotImplementedError(
            "This function should be implement in class that inherit ControlStrategy.")

    @property
    def parafoil(self):
        assert (self._parafoil is not None)
        return self._parafoil

    def set_parafoil(self, p):
        self._parafoil = p
