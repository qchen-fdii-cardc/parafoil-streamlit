import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from parafoil.collocation import FitCollocationStrategy
from parafoil.parafoil import Parafoil
from parafoil.utils import max_rand_vec


st.sidebar.markdown("""
    ## Navigation
    - [Home](#)
    - [Parafoil](#parafoil)
    - [Control](#control)
    - [Wind](#wind)
    """)

d_omega_deg = st.slider("Maximum control input (°/s)", 5.0, 20.0, 10.0, 1.0)
omega_0_deg = st.slider("Initial flight angle (°)", -180.0, 180.0, -15.0, 5.0)
n_collocation_points = st.slider("Number of collocation points", 5, 100, 25, 1)

if st.button("Have a go!"):
    p = Parafoil(450, 450, 9.0, 7.0, 1200.0, np.deg2rad(omega_0_deg))

    d_omega = np.deg2rad(d_omega_deg)
    p.strategy = FitCollocationStrategy(*max_rand_vec(d_omega, n_collocation_points))

    h = p.simulate(500)

    # tab_xy, tab_omega = st.tabs(["Trajectory", "Flight angle"])

    tab_xy, tab_omega = st.columns(2)
    with tab_xy:
        fig = plt.figure()
        ax = fig.gca()

        ax.scatter(h.y[:, 0], h.y[:, 1], s=1)
        ax.scatter(h(0)[0][0], h(0)[0][1], s=50, c='g')

        ax.scatter([0], [0], s=50, c='r', marker='x')

        ax.set_xlabel('x(m)')
        ax.set_ylabel('y(m)')

        ax.axis("equal")
        ax.grid(True)

        st.pyplot(fig)

    with tab_omega:
        fig = plt.figure()
        axs = fig.subplots(nrows=2, ncols=1,sharex=True)

        axs[0].plot(h.time, np.rad2deg(h.y[:, 2]))
        axs[0].set_ylabel(r'$\omega(^\circ)$')
        axs[0].grid(True)
        axs[1].plot(h.time, np.rad2deg(h.u))
        axs[1].set_ylabel(r'$\dot{\omega}(^\circ/s)$')
        axs[1].grid(True)
        axs[1].set_xlabel('t(s)')

        st.pyplot(fig)
