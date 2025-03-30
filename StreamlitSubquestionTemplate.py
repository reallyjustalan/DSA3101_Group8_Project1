# Rename file as subquestion_streamlit.py eg A1_streamlit.py
import streamlit as st
import matplotlib.pyplot as plt # and other necessary libraries

def plot_1():
    fig, ax = plt.subplots()
    ax.plot(...)  # Your existing plotting code
    st.pyplot(fig)  # Streamlit-specific

def insights_1():
    st.header("Key Insights")
    st.write("Your text here...")
