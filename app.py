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

d_omega_deg = st.slider("Maximum control input (°/s)", 5.0, 20.0, 10.0, 1.0)
omega_0_deg = st.slider("Initial flight angle (°)", -180.0, 180.0, -15.0, 5.0)
n_collocation_points = st.slider("Number of collocation points", 5, 100, 25, 1)

p = Parafoil(450, 450, 9.0, 7.0, 1200.0, np.deg2rad(omega_0_deg))

# p.strategy = HomingStrategy(0.1)
d_omega = np.deg2rad(d_omega_deg)
# p.strategy = RandomCollocationStrategy(d_omega, 10)
p.strategy = FitCollocationStrategy(*max_rand_vec(d_omega, n_collocation_points))
# p.strategy = HomingStrategy(d_omega)

h = p.simulate(500)

fig = plt.figure()
ax = fig.gca()

ax.scatter([h(t)[0][0] for t in h.time_range], [h(t)[0][1] for t in h.time_range], s=1)
ax.scatter(h(0)[0][0], h(0)[0][1], s=50, c='g')

ax.scatter([0], [0], s=50, c='r', marker='x')

st.pyplot(fig)
