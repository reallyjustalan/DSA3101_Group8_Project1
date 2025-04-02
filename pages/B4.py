import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

# Base URL for raw images in your GitHub repository
BASE_URL = "https://raw.githubusercontent.com/NotInvalidUsername/DSA3101_Group8_Project1/main/images/B4/"

# Title of the app
st.title("B4: Disneyland Review Analysis")

# Business Question Section
st.write("""
    ### How can we promptly address high-risk interactions to improve guest experience?
""")

# Function to load image from GitHub
def load_image_from_github(image_name):
    import time
    # Append a "cache buster" query param
    url = BASE_URL + image_name + f"?nocache={int(time.time())}"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


# Display the Hierarchical Model Image
st.write("""
    ### Hierarchical Model
    The branches in the hierarchical model are colored according to the similarity between topics. In the model
    below, we have identified 4 different clusters amongst the identified topics. 
""")

# Hierarchical Model image
try:
    model_image = load_image_from_github("hierarchical_clustering.png")
    st.image(model_image, caption="Hierarchical Model", use_container_width=True)
except Exception as e:
    st.error(f"Error loading hierarchical_clustering.png: {e}")

# Topic Modeling & Word Clouds Section
st.write("""
    ### Word Clouds of Topic Clusters:
    After clustering the topics using the hierarchical model, we generated word clouds based on the topic 
    representations for each cluster. By analyzing the reviews that contribute to each cluster, we identified 
    key issues raised by reviewers. 
""")

# Word Cloud for Cluster 1
st.write("#### Cluster 1: Customer Experience")
try:
    image_cluster_1 = load_image_from_github("cluster_1.png")
    st.image(image_cluster_1, caption="Word Cloud Cluster 1", use_container_width=True)
    st.markdown("##### Key Issues:")
    st.markdown("""
    - Overcrowding, high food prices, and long wait times.
    - Negative interactions with different cultures at Hong Kong Disneyland.
    - Disability-related accessibility issues.
    - Lack of prior notice for ride closures.
    """)
except Exception as e:
    st.error(f"Error loading cluster_1.png: {e}")

# Word Cloud for Cluster 2
st.write("#### Cluster 2: Ticket and Refund Issues")
try:
    image_cluster_2 = load_image_from_github("cluster_2.png")
    st.image(image_cluster_2, caption="Word Cloud Cluster 2", use_container_width=True)
    st.markdown("##### Key Insights:")
    st.markdown("""
    - FastPass importance for improving guest experience.
    - Complaints about slow refunds and confusing ticketing policies.
    """)
except Exception as e:
    st.error(f"Error loading cluster_2.png: {e}")

# Word Cloud for Cluster 3
st.write("#### Cluster 3: Staff Response")
try:
    image_cluster_3 = load_image_from_github("cluster_3.png")
    st.image(image_cluster_3, caption="Word Cloud Cluster 3", use_container_width=True)
    st.markdown("##### Key Issues:")
    st.markdown("""
    - Overly strict security staff.
    - Inconsistent staff behavior and service quality.
    """)
except Exception as e:
    st.error(f"Error loading cluster_3.png: {e}")

# Word Cloud for Cluster 4
st.write("#### Cluster 4: Park Environment and Smoking")
try:
    image_cluster_4 = load_image_from_github("cluster_4.png")
    st.image(image_cluster_4, caption="Word Cloud Cluster 4", use_container_width=True)
    st.markdown("##### Key Issues:")
    st.markdown("""
    - Smoking issues, especially at Disneyland Paris.
    - Lack of designated smoking areas.
    - Lack of enforcement of smoking policies.
    """)
except Exception as e:
    st.error(f"Error loading cluster_4.png: {e}")

