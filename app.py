import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


"""
Parafoil Dynamics App
    by Qin Chen, Xinglong Gao
"""

st.text("Welcom")


fig = plt.figure()
ax = fig.gca()
data = np.random.rand(100, 2)
ax.scatter(data[:,0], data[:, 1])

st.pyplot(fig)
