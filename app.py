import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from parafoil.collocation import FitCollocationStrategy
from parafoil.parafoil import Parafoil
from parafoil.utils import max_rand_vec

"""
Parafoil Dynamics for Fun
=====================

    by Qin Chen, Xing-long Gao
"""


if st.button("Flight a parafoil!"):
    p = Parafoil(450, 450, 9.0, 7.0, 1200.0, np.deg2rad(-15.0))

    # p.strategy = HomingStrategy(0.1)
    d_omega = np.deg2rad(10.0)
    # p.strategy = RandomCollocationStrategy(d_omega, 10)
    p.strategy = FitCollocationStrategy(*max_rand_vec(d_omega, 25))
    # p.strategy = HomingStrategy(d_omega)

    h = p.simulate(500)

    fig = plt.figure()
    ax = fig.gca()

    ax.scatter([h(t)[0][0] for t in h.time_range], [h(t)[0][1] for t in h.time_range], s=1)
    ax.scatter(h(0)[0][0], h(0)[0][1], s=50, c='g')

    ax.scatter([0], [0], s=10, c='r', marker='x')

    st.pyplot(fig)
