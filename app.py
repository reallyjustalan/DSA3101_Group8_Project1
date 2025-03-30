# app.py (main file)
import streamlit as st
from subquestion1 import plot_1, insights_1  # Each teammate's code lives in separate files
from subquestion2 import plot_2, insights_2
# ... (up to subquestion10)

st.title("Our Project Dashboard")
tab1, tab2, ... = st.tabs(["SubQ1", "SubQ2", ...])  # Each tab = one subquestion

with tab1:
    plot_1()  # Teammate 1's code
    insights_1()
with tab2:
    plot_2()  # Teammate 2's code
    # ...
