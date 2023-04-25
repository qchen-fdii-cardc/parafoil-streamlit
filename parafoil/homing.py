import numpy as np
from parafoil.parafoil import Parafoil
from parafoil.control import ControlStrategy
from parafoil.utils import to_mpi_pi


class HomingStrategy(ControlStrategy):
    def _control_from_input(self, input: np.ndarray) -> float:
        [t, xt, yt, omega, dt, winx, winy] = input

        self.parafoil: Parafoil
        if self.parafoil is None:
            raise ValueError("Parafoil not set")
        if dt >= 1.1 * np.sqrt(xt*xt + yt*yt)/self.parafoil.v:
            return self.max_domega
        else:
            return to_mpi_pi(np.arctan2(-yt, -xt) - to_mpi_pi(omega))
