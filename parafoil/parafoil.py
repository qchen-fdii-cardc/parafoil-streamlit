from collections import defaultdict
from typing import Tuple, Iterable
import numpy as np
from parafoil.control import ControlStrategy
from scipy.integrate import solve_ivp
import time
import matplotlib.pyplot as plt

from parafoil.windmodel import WindModel


class Trajectory:
    def __init__(self) -> None:
        self.hist = defaultdict()

    def append(self, t, y, dydt, height, u):
        self.hist[t] = (y, dydt, height, u)

    def __call__(self, t: float) -> Tuple[np.ndarray, np.ndarray, float, float]:
        return self.hist[t]

    @property
    def time_range(self) -> Iterable:
        return self.hist.keys()

    def show(self):
        time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        plt.figure()
        plt.plot([self(t)[0][0] for t in self.time_range], [self(t)[0][1]
                                                            for t in self.time_range])
        plt.xlabel("x(m)")
        plt.ylabel("y(m)")
        plt.grid(True)
        plt.tight_layout()
        plt.gca().set_aspect('equal')
        plt.savefig(f"results/{time_str}-trajectory.png", dpi=600)

        # plt.clf()
        # plt.plot([self(t)[1][0] for t in self.time_range], [self(t)[1][1]
        #                                                     for t in self.time_range])
        # plt.xlabel(r"$v_x$(m/s)")
        # plt.ylabel(r"$v_y$(m/s)")
        # plt.grid(True)
        # plt.gca().set_aspect('equal')
        # plt.tight_layout()

        # plt.savefig(f"results/{time_str}-vx-vs-vy.png", dpi=600)

        plt.clf()
        plt.subplot(211)
        plt.plot(self.time_range, [self(t)[1][0] for t in self.time_range])
        plt.xlabel(r"t(s)")
        plt.ylabel(r"$v_x$(m/s)")
        plt.grid(True)
        plt.tight_layout()

        plt.subplot(212)
        plt.plot(self.time_range, [self(t)[1][1]
                                   for t in self.time_range])
        plt.xlabel(r"t(s)")
        plt.ylabel(r"$v_y$(m/s)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"results/{time_str}-vx-vy.png", dpi=600)

        plt.clf()
        plt.subplot(211)
        plt.plot(self.time_range, [np.rad2deg(self(t)[0][2])
                 for t in self.time_range])
        plt.xlabel('t(s)')
        plt.ylabel(r'$\omega(^\circ)$')
        plt.grid(True)

        plt.subplot(212)
        plt.plot(self.time_range, [np.rad2deg(self(t)[3])
                 for t in self.time_range])
        plt.xlabel('t(s)')
        plt.ylabel(r'$\dot{\omega}(^\circ/s)$')
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(f"results/{time_str}-omega.png", dpi=600)


class Parafoil:
    def __init__(self, x0, y0, v0, vz, h0, omega0) -> None:
        """
        Args:
            x0 (float): initial x position
            y0 (float): initial y position
            v0 (float): initial velocity
            vz (float): vertical velocity
            h0 (float): initial height
            omega0 (float): initial angle of attack
        """
        self.x = x0
        self.y = y0
        self.v = v0
        self.h = h0
        self.vz = vz
        self.t_max = h0 / vz
        self.omega = omega0

        # control strategy and wind model
        self.wind_model = WindModel()
        self.control_strategy = ControlStrategy(0.1)
        self.control_strategy.set_parafoil(self)

        # state variables
        self.t: float = 0
        self.state: np.ndarray = np.array([x0, y0, omega0])

    @property
    def height(self) -> float:
        return self.h - self.vz * self.t

    @property
    def dydt(self) -> np.ndarray:
        return self.ode_func(self.t, self.state)

    @property
    def u(self) -> float:
        return self.get_control(self.t, self.state)

    @property
    def strategy(self) -> ControlStrategy:
        return self.control_strategy

    @strategy.setter
    def strategy(self, value: ControlStrategy):
        self.control_strategy = value
        self.control_strategy.set_parafoil(self)

    @property
    def y0(self) -> np.ndarray:
        """
        Initial state vector

        Returns:
            np.ndarray: [x, y, omega]
        """
        return np.asarray([self.x, self.y, self.omega])

    def ode_func(self, t, y) -> np.ndarray:
        v = self.v
        [xt, yt, omega] = y
        winx, winy = self.wind_model.wind_vector(t, self.h-self.vz*t, xt, yt)

        u = self.get_control(t, y)

        dydt = (v * np.cos(omega) + winx, v * np.sin(omega) + winy, u)

        # return np.asarray(dydt)
        return np.hstack(dydt)

    def get_control(self, t, y) -> float:
        [xt, yt, omega] = y
        dt = self.t_max - t
        winx, winy = self.wind_model.wind_vector(t, self.h-self.vz*t, xt, yt)
        u = self.control_strategy.control(
            np.asarray([t, xt, yt, omega, dt, winx, winy]))
        return u

    def reset(self):
        """
        Reset the parafoil to the initial state
        """
        self.t = 0
        self.state = self.y0

    def step(self, dt: float) -> None:
        sol = solve_ivp(self.ode_func, [self.t, self.t+dt], self.state,
                        t_eval=[self.t+dt], rtol=1e-6, atol=1e-6)
        self.t += dt
        self.state = sol.y[:, -1]

    def simulate(self, n=1000) -> Trajectory:
        self.reset()
        h = Trajectory()
        t_span = [0, self.t_max]
        t_eval = np.linspace(0, self.t_max, n)
        sol = solve_ivp(self.ode_func, t_span, self.y0,
                        t_eval=t_eval, rtol=1e-6, atol=1e-6)

        for i, ti in enumerate(sol.t):
            self.t = sol.t[i]
            self.state = sol.y[:, i]
            h.append(self.t, self.state, self.dydt, self.height, self.u)

        self.reset()

        return h
