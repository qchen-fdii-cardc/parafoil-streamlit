# app main entry

import streamlit as st


"""
Parafoil Dynamics for Fun
=====================

    by Qin Chen, Xing-long Gao    

Dynamics{@parafoil}
=====================

Parafoil dynamics is fascinating. It is a nonlinear system with a lot of interesting properties.

We start from 4-DOF equations of motion:
"""

st.latex(r"""
\left\{
\begin{aligned}
\dot{x} &= v \cos \omega \\
\dot{y} &= v \sin \omega \\
\dot{\omega} &= u \\
\dot{v} &= -g \sin \gamma - \frac{1}{2m} \rho v^2 S C_D
\end{aligned}
\right.
""")

"""
Current Control{@control}
=====================

The current control strategy is a simple interpolated collocation control strategy. 
The control input is a piecewise linear function of flight angle error. The control input is limited to a maximum value. 
The control input is interpolated from a set of collocation points. 
The collocation points are generated randomly within the maximum control input. The number of collocation points is adjustable.
"""

"""
Wind Model{@wind}
=====================

No wind model applied currently.
"""

st.sidebar.markdown("""
    ## Navigation
    - [Home](#)
    - [Parafoil](#parafoil)
    - [Control](#control)
    - [Wind](#wind)
    """)