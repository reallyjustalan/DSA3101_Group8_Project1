import streamlit as st
import random
import requests
from PIL import Image
from io import BytesIO

# Set up the page
st.title("Ride layout Optimisation")

GITHUB_USERNAME = "your-username"
REPO_NAME = "your-repo"
BRANCH_NAME = "main"  # Change if using a different branch

# Base URL for raw GitHub content
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/simulations"
GITHUB_API_URL2 = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/heatmaps"

def get_image_files(model, num_rides,GITHUB_API_URL):
    folder_path = f"{GITHUB_API_URL}/{model}/number_rides_{num_rides}"
    response = requests.get(folder_path)

    if response.status_code == 200:
        files = response.json()
        image_files = [
            f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH_NAME}/simulations/{model}/number_rides_{num_rides}/{file['name']}"
            for file in files if file['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
        ]
        return image_files
    else:
        return None

 # Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["Home", "Optimised Park layouts","Simulated Heatmaps", "Business Insights","Limitations & Improvements","Conclusion"]
)

# Define content for each page
if page == "Home":
    st.title("Home Page")
    st.write("Welcome to the Theme Park Optimization Dashboard!")
    "When working on a theme park, a key question must be asked: 'How do we best optimise the layout of a park to increase guest satisfaction and revenue?' In this page, we will be exploring factors that should be taken into consideration while designing a theme park. Features such as park size, layouts and the number of key rides are important information while designing a theme park."
    "This investigation will be split into 5 parts: Optimised Park Layouts, Simulated Heatmaps, Business Insights, Limitations & Improvements, Conclusion."

elif page == "Optimised Park layouts":
    st.title("Optimised Park Layouts")
    st.write("Explore different park layouts.")
    "Let's explore some of the generated Optimised layouts that the team has worked on. For these models, we had focused our attention on 4 main variables: distancing between popular rides, increasing guest satisfaction, increasing the number of rides taken by a guest and decreasing crowds an area gets."

    # Create buttons for model selection
    model = st.radio("Select the type of Model for your park", ("model1", "model2", "model3"))

    # Create slider for number of rides
    num_rides = st.slider("Select the total Number of Rides you would like in the park!", 3, 13, 8)

    # Generate button
    if st.button("Generate Optimised Layout"):
        image_files = get_image_files(model, num_rides, GITHUB_API_URL)

        if not image_files:
            st.warning("No images found or failed to fetch data from GitHub.")
        else:
            # Select a random image
            selected_image_url = random.choice(image_files)

            # Fetch and display the image
            response = requests.get(selected_image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=f"Model: {model} | Rides: {num_rides}")
                st.success(f"Successfully loaded image from: {selected_image_url}")
            else:
                st.error(f"Failed to load image from GitHub: {selected_image_url}")

    "## What patterns do we notice?"
    "No two layouts seem to have the same optimised positions for the rides. This could indicate factors that are missing within the algorithm. Moreover, it also highlights that there is no one true solution to any optimisation problem."
    "So how do we determine which is the best?"
    "That comes down to what the business would want to achieve. Business goals of individual theme parks would differ from one and other. Be it through picking a layout that maximises revenue or a theme park that maximises guest retention through constantly upgrading and sustainably growing the park to include more rides. The opportunities are endless. Yet one pattern remains constant. As the number of rides increase, there are clusters of less popular rides around some of the more popular rides."
    "This provides opportunities for businesses to make meaning from the layout through theming."
    "Yet given these clusters, how do people ultimately explore a park?"

elif page == "Simulated Heatmaps":
    st.title("Heatmaps")
    "## Explore"
    "Explore how the density of people at a theme park and their relative positions fluctuates depending on layout type and the number of rides."

    model_density = st.radio("Select a model for density exploration", ("model1", "model2", "model3"))
    num_rides_density = st.slider("Select the total number of rides for density analysis!", 3, 13, 8)

    # Generate button
    if st.button("Generate Density layout"):
        image_files = get_image_files(model_density, num_rides_density, GITHUB_API_URL2)

        if not image_files:
            st.warning("No images found or failed to fetch data from GitHub.")
        else:
           heatmap_images = [
            img for img in image_files if any(f"heatmap_step_{i}" in img for i in range(1, 8))
        ]

        if len(heatmap_images) < 7:
            st.warning("Not enough sequential heatmap images found.")
        else:
            # Display all 7 heatmap images in order
            for step, img_url in enumerate(sorted(heatmap_images), start=1):
                response = requests.get(img_url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    st.image(image, caption=f"Heatmap Step {step}")
                else:
                    st.error(f"Failed to load image: {img_url}")
    #     if st.button("Generate Random Image"):
    # # Construct the path based on selections
    # folder_path = os.path.join("simulations", model, f"num_rides{num_rides}")
    
    # # Check if the directory exists
    # if not os.path.exists(folder_path):
    #     st.error(f"Directory not found: {folder_path}")
    # else:
    #     # Get all image files in the directory
    #     image_files = [f for f in os.listdir(folder_path) 
    #                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
    #     if not image_files:
    #         st.warning(f"No images found in {folder_path}")
    #     else:
    #         # Select a random image
    #         selected_image = random.choice(image_files)
    #         image_path = os.path.join(folder_path, selected_image)
            
    #         # Display the image
    #         try:
    #             image = Image.open(image_path)
    #             st.image(image, caption=f"Model: {model} | Rides: {num_rides} | Image: {selected_image}")
    #         except Exception as e:
    #             st.error(f"Error loading image: {e}")

    st.header("What Patterns Do We Notice?")

    st.write(
        "Without additional information, incentives, or support to guide a guest’s decision-making process, "
        "we observe a **natural normalization** of activity on the park's heatmap—primarily concentrated around popular rides. "
        "This results in **certain areas becoming overcrowded while others remain underutilized**."
    )

    ## How Can We Influence Guest Movement?
    st.subheader("How Can We Influence Guest Movement?")

    st.write("To create a more balanced distribution of guests, parks can implement a combination of **information, incentives, and support systems**:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Information")
        st.write(
            "A **live queue tracker** allows guests to make informed decisions by identifying less crowded rides, "
            "naturally directing them toward underutilized areas."
        )

    with col2:
        st.markdown("### Incentives")
        st.write(
            "Strategic placement of **rest zones, water coolers, merchandise, and food stands** can draw guests to "
            "less-visited parts of the park, helping to evenly distribute foot traffic."
        )

    with col3:
        st.markdown("### Support")
        st.write(
            "**Information kiosks and interactive guides** can assist guests in navigating the park, recommending "
            "alternative attractions, and ensuring a smoother guest flow."
        )

    st.write("By integrating these strategies, theme parks can enhance the overall guest experience while optimizing park-wide efficiency.")



elif page == "Business Insights":
    st.title("Insights")
    st.write("Discover key patterns and business insights.")
    st.markdown("## What does this mean from a business perspective?")

    st.markdown("""
    From a business standpoint, this visualisation provides insight to both possible challenges and opportunities. Here’s how it translates into important decisions for a theme park:
    """)

    with st.expander("### 1. Guest Flow and Spreading Out"):
        st.markdown("""
        Overutilized areas can lead to overcrowding, resulting in longer wait times, restricted movement, and dissatisfaction. Underutilized areas may indicate neglected parts of the park. Optimizing guest flow ensures all areas are well-utilized, minimizing bottlenecks and enhancing the experience.

        **Solution:** Implementing crowd control strategies like dynamic queue management and timed ticketing, the park can reduce congestion and make less crowded areas more appealing. Businesses can also place mascot meets and photospots in areas of underutilisation, pulling potential guests to other parts of the park.
        """)

    with st.expander("### 2. Optimal Placement of Guest Services"):
        st.markdown("""
        Guest satisfaction depends on strategically placed services like restrooms, information desks, and emergency stations. If these services are too concentrated in specific areas, guests might experience longer wait times and poorer service.

        **Solution:** **Guest services** should be strategically distributed across the park, with larger rest areas and restrooms placed in quieter sections to encourage exploration and improve accessibility. If these services are placed in a high-density area, a greater staff allocation will be needed to meet the demands and ensure guest standards are met.
        """)

    with st.expander("### 3. Merchandise and Photo Spots"):
        st.markdown("""
        Merchandise stands are key revenue generators but must be placed strategically. If they are too close to high-traffic areas, they may cause congestion; if in low-traffic zones, they may be overlooked.

        **Solution:** Merchandise locations should be near high-traffic areas but not too close to major attractions. This ensures maximum visibility and maximum foot traffic with guests while minimizing crowding.
        """)

    with st.expander("### 4. Food and Dining Locations"):
        st.markdown("""
        Long food lines can negatively impact the guest experience. Placing food stalls too close to high-traffic areas may create congestion, while placing them in quiet zones may lead to lower sales.

        **Solution:** Restaurants and snack stands should be placed near major rides while also being used strategically to encourage guests to explore less busy areas. Portable food carts or food trucks can serve as a way to activate underutilized zones. Possible placement of restaurants should be near clusters of rides, ensuring high traffic and increasing guest interaction while meeting their needs.
        """)

    with st.expander("### 5. Theming and Atmosphere"):
        st.markdown("""
        Theming attracts guests to different areas of the park, helping to distribute crowds effectively. A well-designed park uses theming to guide visitors naturally from one section to another.

        **Solution:** **Highly themed zones** should be strategically placed across the park, following the optimized clustering of rides. Between clusters, themed walkways and immersive experiences can help distribute visitors evenly. This would improve the guest's experience, creating a more immersive environment.
        """)

    with st.expander("### 6. Maximizing Revenue"):
        st.markdown("""
        Overcrowded areas may lead to lower guest spending, as visitors might avoid shopping or dining due to long lines. Overcrowded areas may also lead to lower guest satisfaction as they feel uncomfortable.

        **Solution:** A well-balanced layout, supported by real-time data, optimized placement of rides, shops, and photo zones, ensures higher guest satisfaction and increased revenue potential.
        """)

elif page == "Limitations & Improvements":
    st.title("Limitations")
    st.write("Throughout this project there have been limitations to the coding and discovery")

elif page == "Conclusion":
    st.title("Conclusion")
    st.write("Discover key patterns and business insights.")
    st.markdown("""
Balancing guest distribution and strategically placing services, attractions, and revenue-generating assets is key to a theme park’s success. An optimised layout of rides should ultimately align itself with the business goals and intention at hand allowing parks to create enjoyable guest experiences while maintaining its goals of meeting its business intentions allwoing it to be worthwhile.
""")



# "## Explore"
# "Explore some of the generated Optimised layouts that the team has worked on. For these models, we had focused our attention on 4 main variables: distancing between popular rides, increasing guest satisfaction, increasing the number of rides taken by a guest and decreasing crowds an area gets."

# # Get the user's Downloads folder path
# downloads_path = os.path.expanduser("~\Downloads")
# simulations_path = os.path.join(downloads_path, "simulations")


# # Create buttons for model selection
# model = st.radio("Select the type of Model for your park", ("model1", "model2", "model3"))

# # Create slider for number of rides
# num_rides = st.slider("Select the total Number of Rides you would like in the park!", 3, 13, 8)

# # Generate button
# if st.button("Generate Optimised layout"):
#     # Construct the path based on selections
#     folder_path = os.path.join(simulations_path, model, f"number_rides_{num_rides}")
    
#     # Check if the directory exists
#     if not os.path.exists(folder_path):
#         st.error(f"Directory not found: {folder_path}")
#         st.info(f"Expected path: {folder_path}")
#     else:
#         # Get all image files in the directory
#         image_files = [f for f in os.listdir(folder_path) 
#                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
#         if not image_files:
#             st.warning(f"No images found in {folder_path}")
#         else:
#             # Select a random image
#             selected_image = random.choice(image_files)
#             image_path = os.path.join(folder_path, selected_image)
            
#             # Display the image
#             try:
#                 image = Image.open(image_path)
#                 st.image(image, caption=f"Model: {model} | Rides: {num_rides} | Image: {selected_image}")
#                 st.success(f"Successfully loaded image from: {image_path}")
#             except Exception as e:
#                 st.error(f"Error loading image: {e}")

# "## What patterns do we notice?"
# "No two layouts seem to have the same optimised positions for the rides. This could indicate factors that are missing within the algorithm. Moreover, it also highlights that there is no one true solution to any optimisation problem."
# "So how do we determine which is the best?"
# "That comes down to what the business would want to achieve. Business goals of individual theme parks would differ from one and other. Be it through picking a layout that maximises revenue or a theme park that maximises guest retention through constantly upgrading and sustainably growing the park to include more rides. The opportunities are endless. Yet one pattern remains constant. As the number of rides increase, there are clusters of less popular rides around some of the more popular rides."
# "This provides opportunities for businesses to make meaning from the layout through theming."
# "Yet given these clusters, how do people ultimately explore a park?"

# "## Explore"
# "Explore how the density of people at a theme park and their relative positions fluctuates depending on layout type and the number of rides."

# model_density = st.radio("Select a model for density exploration", ("model1", "model2", "model3"))
# num_rides_density = st.slider("Select the total number of rides for density analysis!", 3, 13, 8)

# # Generate button
# if st.button("Generate Density layout"):
#     print("under construction")


# st.header("What Patterns Do We Notice?")

# st.write(
#     "Without additional information, incentives, or support to guide a guest’s decision-making process, "
#     "we observe a **natural normalization** of activity on the park's heatmap—primarily concentrated around popular rides. "
#     "This results in **certain areas becoming overcrowded while others remain underutilized**."
# )

# ## How Can We Influence Guest Movement?
# st.subheader("How Can We Influence Guest Movement?")

# st.write("To create a more balanced distribution of guests, parks can implement a combination of **information, incentives, and support systems**:")

# st.markdown("### Information")
# st.write("A **live queue tracker** allows guests to make informed decisions by identifying less crowded rides, naturally directing them toward underutilized areas.")

# st.markdown("### Incentives")
# st.write(
#     "Strategic placement of **rest zones, water coolers, merchandise, and food stands** can draw guests to less-visited parts of the park, "
#     "helping to evenly distribute foot traffic."
# )

# st.markdown("### Support")
# st.write(
#     "**Information kiosks and interactive guides** can assist guests in navigating the park, recommending alternative attractions, "
#     "and ensuring a smoother guest flow."
# )

# st.write("By integrating these strategies, theme parks can enhance the overall guest experience while optimizing park-wide efficiency.")

# st.markdown("## What does this mean from a business perspective?")

# st.markdown("""
# From a business standpoint, this visualisation provides insight to both possible challenges and opportunities. Here’s how it translates into important decisions for a theme park:
# """)

# st.markdown("### 1. Guest Flow and Spreading Out")
# st.markdown("""
# Overutilized areas can lead to overcrowding, resulting in longer wait times, restricted movement, and dissatisfaction. Underutilized areas may indicate neglected parts of the park. Optimizing guest flow ensures all areas are well-utilized, minimizing bottlenecks and enhancing the experience.

# **Solution:** Implementing crowd control strategies like dynamic queue management and timed ticketing, the park can reduce congestion and make less crowded areas more appealing. Businesses can also place mascot meets and photospots in areas of underutilisation, pulling potential guests to other parts of the park.
# """)

# st.markdown("### 2. Optimal Placement of Guest Services")
# st.markdown("""
# Guest satisfaction depends on strategically placed services like restrooms, information desks, and emergency stations. If these services are too concentrated in specific areas, guests might experience longer wait times and poorer service.

# **Solution:** **Guest services** should be strategically distributed across the park, with larger rest areas and restrooms placed in quieter sections to encourage exploration and improve accessibility. If these servcies are placed in a high density area, a greater staff allocation will be needed to meet the demands and ensure guest standards are met.
# """)

# st.markdown("### 3. Merchandise and Photo Spots")
# st.markdown("""
# Merchandise stands are key revenue generators but must be placed strategically. If they are too close to high-traffic areas, they may cause congestion; if in low-traffic zones, they may be overlooked.

# **Solution:** Merchandise locations should be near high traffic areas but not too close to major attractions. This ensures maximum visibility and maximum foot traffic with guests while minimising crowd. 
# """)

# st.markdown("### 4. Food and Dining Locations")
# st.markdown("""
# Long food lines can negatively impact the guest experience. Placing food stalls too close to high-traffic areas may create congestion, while placing them in quiet zones may lead to lower sales.

# **Solution:** Restaurants and snack stands should be placed near major rides while also being used strategically to encourage guests to explore less busy areas. Portable food carts or food trucks can serve as a way to activate underutilized zones. Possible placement of restruants should be placed near clusters of rides, ensuring high traffic and increasing guest interaction and meeting their needs.
# """)

# st.markdown("### 5. Theming and Atmosphere")
# st.markdown("""
# Theming attracts guests to different areas of the park, helping to distribute crowds effectively. A well-designed park uses theming to guide visitors naturally from one section to another.

# **Solution:** **Highly themed zones** should be strategically placed across the park, following the optimised clustering of rides. Between clusters, themed walkways and immersive experiences can help distribute visitors evenly. This would improve the guest's experience creating a more immersive experience.
# """)

# st.markdown("### 6. Maximizing Revenue")
# st.markdown("""
# Overcrowded areas may lead to lower guest spending, as visitors might avoid shopping or dining due to long lines. Overcrowded areas may also lead to lower guest satisfaction as they feel uncomfortable. 

# **Solution:** A well-balanced layout, supported by real-time data, optimised placement of rides, shops and photo zones, ensures higher guest satisfaction and increased revenue potential.
# """)

# st.markdown("## Conclusion")
# st.markdown("""
# Balancing guest distribution and strategically placing services, attractions, and revenue-generating assets is key to a theme park’s success. An optimised layout of rides should ultimately align itself with the business goals and intention at hand allowing parks to create enjoyable guest experiences while maintaining its goals of meeting its business intentions allwoing it to be worthwhile.
# """)

