import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import random

# Set up the page
st.title("Ride Layout Optimisation")

# GitHub repository information
GITHUB_USERNAME = "NotInvalidUsername"
REPO_NAME = "DSA3101_Group8_Project1"
BRANCH_NAME = "alan_bean"  # Change if using a different branch

# Base URL for GitHub content
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH_NAME}"
SIMULATIONS_PATH = "images/B2/simulations"
HEATMAPS_PATH = "images/B2/heatmaps"

def get_image_files(model, num_rides, image_type="simulations"):
    """Get image files from GitHub repository"""
    if image_type == "simulations":
        folder_path = f"{SIMULATIONS_PATH}/{model}/number_rides_{num_rides}"
    else:
        folder_path = f"{HEATMAPS_PATH}/{model}/num_rides_{num_rides}"
    
    # GitHub API URL to list contents
    api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{folder_path}?ref={BRANCH_NAME}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        files = response.json()
        image_files = []
        
        for file in files:
            if file['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Construct raw content URL
                image_url = f"{BASE_URL}/{folder_path}/{file['name']}"
                image_files.append(image_url)
        
        return image_files if image_files else None
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error accessing GitHub: {e}")
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

    st.subheader(":national_park: Let's Explore Different Park Layouts!")

    st.write("Let's explore some of the generated Optimised layouts that the team has worked on. For these models, we had focused our attention on 4 main variables: distancing between popular rides, increasing guest satisfaction, increasing the number of rides taken by a guest and decreasing crowds an area gets.")

    # Create buttons for model selection
    model = st.radio("Select the type of Model for your park", ("Ring Shaped", "Plain", "Large with Lake"))

    # Create slider for number of rides
    num_rides = st.slider("Select the total Number of Rides you would like in the park!", 3, 13, 8)

    # Generate button
    if st.button("Generate Optimised Layout"):
        if model == "Ring Shaped":
            model = "model1"
        elif model == "Plain":
            model = "model2"
        else:
            model = "model3"

        image_files = get_image_files(model, num_rides)

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

    "## :mag: What patterns do we notice?"
    "No **two** layouts seem to have the same optimised positions for the rides. This could indicate factors that are missing within the algorithm. Moreover, it also highlights that there is no one true solution to any optimisation problem."
    "So how do we determine which is the best?"
    "That comes down to what the business would want to achieve. Business goals of individual theme parks would differ from one and other. Be it through picking a layout that maximises revenue or a theme park that maximises guest retention through constantly upgrading and sustainably growing the park to include more rides. The opportunities are endless. Yet one pattern remains constant. As the number of rides increase, there are clusters of less popular rides around some of the more popular rides."
    "This provides opportunities for businesses to make meaning from the layout through theming."
    "Yet given these clusters, how do people ultimately explore a park?"

elif page == "Simulated Heatmaps":
    st.title("Heatmaps")
    "## Let's Explore!:fire::world_map:"
    "Explore how the density of people at a theme park and their relative positions fluctuates depending on layout type and the number of rides."

    model_density = st.radio("Select a model for density exploration", ("Ring Shaped", "Plain", "Large with Lake"))
    num_rides_density = st.slider("Select the total number of rides for density analysis!", 3, 13, 8)

    # Generate button
    if st.button("Generate Density layout"):
        if model_density == "Ring Shaped":
            model_density = "model1"
        elif model_density == "Plain":
            model_density = "model2"
        else:
            model_density = "model3"
        image_files = get_image_files(model_density, num_rides_density, "heatmaps")

        if not image_files:
            st.warning("No images found or failed to fetch data from GitHub.")
        else:
           heatmap_images = [
            img for img in image_files if any(f"heatmap_step_{i*10}" in img for i in range(0, 8))
        ]

            # Display all 7 heatmap images in order
        for step, img_url in enumerate(sorted(heatmap_images), start=0):
            response = requests.get(img_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=f"Heatmap Step {step*10}")
            else:
                st.error(f"Failed to load image: {img_url}")


    st.header("What Patterns Do We Notice?:mag_right:")

    st.write(
        "Without additional information, incentives, or support to guide a guest’s decision-making process, "
        "we observe a **natural normalization** of activity on the park's heatmap—primarily concentrated around popular rides. "
        "This results in **certain areas becoming overcrowded while others remain underutilized**."
    )

    ## How Can We Influence Guest Movement?
    st.subheader("How Can We Influence Guest Movement?:runner:")

    st.write("To create a more balanced distribution of guests, parks can implement a combination of **information, incentives, and support systems**:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Information :information_source:")
        st.write(
            "A **live queue tracker** allows guests to make informed decisions by identifying less crowded rides, "
            "naturally directing them toward underutilized areas."
        )

    with col2:
        st.markdown("### Incentives :restroom:")
        st.write(
            "Strategic placement of **rest zones, water coolers, merchandise, and food stands** can draw guests to "
            "less-visited parts of the park, helping to evenly distribute foot traffic."
        )

    with col3:
        st.markdown("### Support :anchor:")
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

    with st.expander("### 1. Guest Flow and Spreading Out :walking: "):
        st.markdown("""
        Overutilized areas can lead to overcrowding, resulting in longer wait times, restricted movement, and dissatisfaction. Underutilized areas may indicate neglected parts of the park. Optimizing guest flow ensures all areas are well-utilized, minimizing bottlenecks and enhancing the experience.

        **Solution:** Implementing crowd control strategies like dynamic queue management and timed ticketing, the park can reduce congestion and make less crowded areas more appealing. Businesses can also place mascot meets and photospots in areas of underutilisation, pulling potential guests to other parts of the park.
        """)

    with st.expander("### 2. Optimal Placement of Guest Services :information_source:"):
        st.markdown("""
        Guest satisfaction depends on strategically placed services like restrooms, information desks, and emergency stations. If these services are too concentrated in specific areas, guests might experience longer wait times and poorer service.

        **Solution:** **Guest services** should be strategically distributed across the park, with larger rest areas and restrooms placed in quieter sections to encourage exploration and improve accessibility. If these services are placed in a high-density area, a greater staff allocation will be needed to meet the demands and ensure guest standards are met.
        """)

    with st.expander("### 3. Merchandise and Photo Spots :handbag::camera_with_flash:"):
        st.markdown("""
        Merchandise stands are key revenue generators but must be placed strategically. If they are too close to high-traffic areas, they may cause congestion; if in low-traffic zones, they may be overlooked.

        **Solution:** Merchandise locations should be near high-traffic areas but not too close to major attractions. This ensures maximum visibility and maximum foot traffic with guests while minimizing crowding.
        """)

    with st.expander("### 4. Food and Dining Locations :fork_and_knife:"):
        st.markdown("""
        Long food lines can negatively impact the guest experience. Placing food stalls too close to high-traffic areas may create congestion, while placing them in quiet zones may lead to lower sales.

        **Solution:** Restaurants and snack stands should be placed near major rides while also being used strategically to encourage guests to explore less busy areas. Portable food carts or food trucks can serve as a way to activate underutilized zones. Possible placement of restaurants should be near clusters of rides, ensuring high traffic and increasing guest interaction while meeting their needs.
        """)

    with st.expander("### 5. Theming and Atmosphere :flags:"):
        st.markdown("""
        Theming attracts guests to different areas of the park, helping to distribute crowds effectively. A well-designed park uses theming to guide visitors naturally from one section to another.

        **Solution:** **Highly themed zones** should be strategically placed across the park, following the optimized clustering of rides. Between clusters, themed walkways and immersive experiences can help distribute visitors evenly. This would improve the guest's experience, creating a more immersive environment.
        """)

    with st.expander("### 6. Maximizing Revenue :moneybag:"):
        st.markdown("""
        Overcrowded areas may lead to lower guest spending, as visitors might avoid shopping or dining due to long lines. Overcrowded areas may also lead to lower guest satisfaction as they feel uncomfortable.

        **Solution:** A well-balanced layout, supported by real-time data, optimized placement of rides, shops, and photo zones, ensures higher guest satisfaction and increased revenue potential.
        """)


if page == "Limitations & Improvements":
    st.title(":white_check_mark: Limitations & Improvements")
    st.write("This project has several limitations, categorized into guest behavior assumptions, technical constraints, missing agents, data limitations, and hardware constraints. These factors impact the realism and effectiveness of the model.")

    # Creating Tabs for Better Organization
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Guest Behavior", "Technical", "Additional Agents", 
        "Data Limitations", "Grid & Layout", "Hardware","Improvements"
    ])

    with tab1:
        st.subheader("📌 Guest Behavior Limitations")
        st.markdown("""
        - **No fatigue/energy modeling** – Guests do not get tired, which would typically affect movement speed, ride choices, and the need for rest breaks.  
        - **Fixed spending patterns** – Guest spending behavior is static and does not account for personal budgets, promotional offers, or spending fatigue.  
        - **No group dynamics simulation** – Guests move independently, without families or friend groups influencing their choices and paths.  
        - **No time-awareness in decision-making** – Visitors do not adjust behavior based on park closing times, ride operation schedules, or showtimes.  
        - **Limited queue avoidance strategies** – Guests do not actively seek shorter queue times, meaning bottlenecks may not fully reflect real-world patterns.  
        - **Lack of adaptive decision-making** – Guests do not reconsider their routes based on real-time crowd density, wait times, or sudden events (e.g., ride breakdowns).  
        """)

    with tab2:
        st.subheader("⚙️ Technical Constraints")
        st.markdown("""
        - **Limited Genetic Algorithm Performance** – The optimization algorithm has an ≈80% success rate in finding an optimal layout but may get stuck in local optima.  
        - **Fixed grid size (Rectangular 15x15)** – The park layout lacks variability in shape; real parks are irregularly shaped rather than strict grids.  
        - **Simulation step cap (70 steps)** – Guest movement is limited, restricting long-term crowd dynamics analysis.  
        - **Simplified ride interactions** – Guests are assumed to always take a ride if it's available, ignoring factors like ride preference or hesitation.  
        - **Limited pathing algorithm** – The model does not account for real-world navigation obstacles like stairs, slopes, or restricted areas.  
        """)

    with tab3:
        st.subheader("🚧 Missing Park Elements & Agents")
        st.markdown("""
        - **No restrooms, seating areas, or rest zones** – Fatigue-based movement adjustments are not modeled.  
        - **No merchandise or food stalls** – Retail and food outlets, which influence spending and movement, are absent.  
        - **No entertainment zones** – Shows, parades, and character meet-and-greets that create congestion are not considered.  
        - **Lack of signage and wayfinding** – Guests do not navigate using maps or directional signs.  
        - **No weather-based influence** – Rain, extreme heat, or other weather factors do not affect guest movement patterns.  
        """)

    with tab4:
        st.subheader("📊 Data Limitations")
        st.markdown("""
        - **Hardcoded ride capacities** – Ride capacity does not change based on guest demand or real-time factors.  
        - **No historical visitor data integration** – The model lacks real-world attendance trends for validation.  
        - **Lack of seasonality effects** – Peak seasons, holidays, and festivals, which greatly impact park flow, are not considered.  
        - **No guest demographics consideration** – Different age groups (e.g., families with children, teenagers, elderly visitors) are not modeled with distinct behaviors.  
        """)

    with tab5:
        st.subheader("🗺️ Grid & Layout Constraints")
        st.markdown("""
        - **Fixed rectangular grid size (15x15)** – The park layout lacks variability in shape.  
        - **Lack of terrain variation** – No slopes, elevation changes, or obstacles.  
        - **No flexible park expansion system** – Cannot dynamically change layout.  
        """)

    with tab6:
        st.subheader("💻 Hardware Constraints")
        st.markdown("""
        - **Limited processing power** – More complex simulations require significant computational resources.  
        - **Exponential complexity growth** – Scaling the model for larger parks with dynamic visitor behavior would drastically increase processing requirements.  
        """)
    with tab7:
        st.subheader("🔄 Future Improvements")
        st.markdown("""
    To improve the simulation, future iterations could include:  
    - **More dynamic guest decision-making** – Guests should adjust their plans based on queue times, weather, time of day, and external incentives.  
    - **Group behavior modeling** – Visitors should move in groups, influencing ride choices and movement patterns.  
    - **More flexible park layouts** – Allow for non-grid, irregular park designs with variable dimensions.  
    - **Real-time adjustments** – The simulation should allow for ride breakdowns, special events, and other disruptions.  
    - **Larger-scale simulations** – Optimize computational performance to handle more guests and complex decision-making processes.  
    """)





elif page == "Conclusion":
    st.title(":chart_with_upwards_trend: Conclusion")
    st.write("Discover key patterns and business insights.")
    st.markdown("""Balancing guest distribution and strategically placing services, attractions, and revenue-generating assets is key to a theme park’s success. "
    "An optimised layout of rides should ultimately align itself with the business goals and intention at hand allowing parks to create enjoyable guest experiences while maintaining its goals of meeting its business intentions.""")
   
    
    st.markdown("""While the project has demonstrated the potential for **ride layout optimization** in theme parks through simulation-based modeling,  
    it is not without its limitations.  

    **Key constraints**, such as **simplified guest decision-making, lack of adaptive behavior and missing park elements (e.g., rest stops, merchandise),  
    highlights areas where further development is needed. While these factors limit a model’s realism, it does also provide key insights as to where and how
    we can improve a theme park.    

    Possible future iterations could integrate modelling such as **dynamic decision-making, real-time factors,group behavior modeling and additional  
    constraints such as weather** to create a more accurate representation of guest movement.   

    This project provides an  understanding to optimising theme park ride layouts.  
    With further refinements, the model could become a valuable tool for park planners, optimizing guest satisfaction, operational efficiency and achieving business goals.  
    """)

    st.success("With continued improvements, this project could significantly enhance theme park planning and design.") 