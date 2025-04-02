import umap
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import numpy as np
from ast import literal_eval
import pandas as  pd
import streamlit as st

# Add this to your imports at the top of your file
# Add a new tab for the UMAP visualization
tab1, tab2, tab3, tab4 = st.tabs(["Correlation Analysis", "Examples of Reviews", "UMAP Visualization", "Raw Data"])

# Update your load_data function to include the embeddings
@st.cache_data
def load_data():
    df_coded = pd.read_csv("data/A1/DisneylandReviews_Coded.csv")
    df_sample = pd.read_csv("data/A1/DisneylandReviews_Sample.csv")
    df_embeddings = pd.read_csv("data/A1/DisneylandReviews_Embedded.csv")
    df_sample = df_sample.rename(columns={'Review_ID': "review_id"})

    # Try to load embeddings from the new progress file
    try:
        # Keep only review_id and embedding columns
        df_embeddings = df_embeddings[['review_id', 'embedding']]
        # Merge with other data
        df_coded = pd.merge(df_coded, df_embeddings, on="review_id", how="left")
    except:
        st.warning("Embeddings file not found. UMAP visualization will not be available.")
    
    # Rest of your existing load_data function...
    # Merge datasets
    merged_df = pd.merge(df_sample, df_coded, on="review_id")
    merged_df["touchpoint_sentiment"] = merged_df["touchpoint"] + "_" + merged_df["sentiment"]
    
    # Create pivot table
    df_pivot = (
        merged_df.groupby(["review_id", "touchpoint_sentiment"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    
    # Add review info
    review_info = merged_df[["review_id", "Rating", "Branch", "Review_Text"]].drop_duplicates(subset=["review_id"])
    df_analysis = pd.merge(df_pivot, review_info, on="review_id", how="left")
    
    return df_analysis, merged_df

# Get the dataframes from the load_data function
df_analysis, merged_df = load_data()

# Add this new code for the UMAP visualization tab
with tab3:
    st.header("UMAP Visualization of Review Embeddings")
    
    # Function to convert embedding string to numpy array
    def parse_embedding(embedding):
        if pd.isna(embedding):
            return None
        try:
            # Handle string format from embedding_str column
            return np.array(literal_eval(embedding))
        except:
            return None
    
    # Function to prepare data for UMAP
    def prepare_umap_data(merged_df):
        # Get unique reviews with their embeddings
        unique_reviews = merged_df[["review_id", "Rating", "embedding_str"]].drop_duplicates()
        
        # Parse the embeddings
        unique_reviews["embedding_array"] = unique_reviews["embedding_str"].apply(parse_embedding)
        
        # Drop rows with missing embeddings
        valid_reviews = unique_reviews.dropna(subset=["embedding_array"])
        
        if len(valid_reviews) < 10:
            st.error("Not enough valid embeddings found for UMAP visualization.")
            return None
            
        # Extract embeddings into a numpy array
        embeddings = np.stack(valid_reviews["embedding_array"].values)
        
        return valid_reviews, embeddings
    
    # Check if embeddings are available
    if "embedding_str" in merged_df.columns:
        with st.spinner("Preparing UMAP visualization..."):
            # Prepare data
            umap_data = prepare_umap_data(merged_df)
            
            if umap_data is not None:
                valid_reviews, embeddings = umap_data
                
                # UMAP parameters
                n_neighbors = st.slider("Number of neighbors for UMAP", 5, 50, 15)
                min_dist = st.slider("Minimum distance for UMAP", 0.0, 1.0, 0.1, 0.05)
                
                # Reduce dimensionality with UMAP
                reducer = umap.UMAP(
                    n_neighbors=n_neighbors,
                    min_dist=min_dist,
                    n_components=2,
                    random_state=42
                )
                
                embedding_2d = reducer.fit_transform(embeddings)
                
                # Add UMAP coordinates to dataframe
                valid_reviews["umap_x"] = embedding_2d[:, 0]
                valid_reviews["umap_y"] = embedding_2d[:, 1]
                
                # Get touchpoint data for each review
                touchpoint_data = {}
                for review_id in valid_reviews["review_id"]:
                    # Get touchpoints for this review
                    review_touchpoints = merged_df[merged_df["review_id"] == review_id]["touchpoint"].tolist()
                    touchpoint_data[review_id] = ", ".join(set(review_touchpoints))
                
                valid_reviews["touchpoints"] = valid_reviews["review_id"].map(touchpoint_data)
                
                # Create a hover data dictionary with review info
                hover_data = {}
                for review_id in valid_reviews["review_id"]:
                    review_info = merged_df[merged_df["review_id"] == review_id]
                    review_text = review_info["Review_Text"].iloc[0] if not review_info.empty else ""
                    hover_data[review_id] = review_text[:200] + "..." if len(review_text) > 200 else review_text
                
                valid_reviews["hover_text"] = valid_reviews["review_id"].map(hover_data)
                
                # Get sentiment data
                sentiment_data = {}
                for review_id in valid_reviews["review_id"]:
                    # Get sentiments for this review
                    review_sentiments = merged_df[merged_df["review_id"] == review_id]["sentiment"].tolist()
                    # Count sentiments
                    sentiment_counts = {
                        "positive": review_sentiments.count("positive"),
                        "negative": review_sentiments.count("negative"),
                        "neutral": review_sentiments.count("neutral")
                    }
                    # Determine dominant sentiment
                    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
                    sentiment_data[review_id] = dominant_sentiment
                
                valid_reviews["dominant_sentiment"] = valid_reviews["review_id"].map(sentiment_data)
                
                # Create interactive plot with Plotly
                st.subheader("2D Projection of Review Embeddings")
                
                # Filter options
                filter_options = st.multiselect(
                    "Filter by touchpoint (select multiple):",
                    options=touchpoint_descriptions.keys(),
                    default=[]
                )
                
                # Filter the data if touchpoints are selected
                if filter_options:
                    filtered_reviews = valid_reviews[valid_reviews["touchpoints"].apply(
                        lambda x: any(tp in x for tp in filter_options)
                    )]
                else:
                    filtered_reviews = valid_reviews
                
                if len(filtered_reviews) > 0:
                    # Create the plot
                    fig = px.scatter(
                        filtered_reviews,
                        x="umap_x",
                        y="umap_y",
                        color="Rating",
                        color_continuous_scale="RdYlGn",
                        range_color=[1, 5],
                        hover_name="review_id",
                        hover_data=["Rating", "touchpoints", "hover_text"],
                        labels={"umap_x": "UMAP Dimension 1", "umap_y": "UMAP Dimension 2"},
                        title="Reviews Clustered by Semantic Similarity"
                    )
                    
                    # Customize the plot
                    fig.update_traces(marker=dict(size=8, opacity=0.7))
                    fig.update_layout(
                        plot_bgcolor="white",
                        height=700,
                        width=1000
                    )
                    
                    # Show plot
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add explanation
                    st.markdown("""
                    ### Understanding the Visualization
                    
                    - Each point represents a review
                    - Colors indicate the rating (green = high, red = low)
                    - Points that are close to each other have similar language or discuss similar topics
                    - Hover over points to see review details
                    
                    This visualization helps identify clusters of similar reviews and understand what guests are talking about when giving different ratings.
                    """)
                    
                    # Add an analysis of reviews by rating
                    st.subheader("Top Touchpoints by Rating")
                    
                    # Group data by rating and collect touchpoints
                    rating_touchpoints = {}
                    for rating in range(1, 6):
                        # Get reviews with this rating
                        rating_reviews = merged_df[merged_df["Rating"] == rating]
                        # Count touchpoints
                        touchpoint_counts = rating_reviews["touchpoint"].value_counts()
                        # Store top 5 touchpoints
                        rating_touchpoints[rating] = touchpoint_counts.head(5).to_dict() if len(touchpoint_counts) > 0 else {}
                    
                    # Create columns for each rating
                    rating_cols = st.columns(5)
                    
                    for i, rating in enumerate(range(1, 6)):
                        with rating_cols[i]:
                            st.write(f"### {rating}★")
                            if rating_touchpoints[rating]:
                                for tp, count in rating_touchpoints[rating].items():
                                    st.write(f"- {tp}: {count}")
                            else:
                                st.write("No data")
                else:
                    st.warning("No reviews match the selected touchpoints.")
    else:
        st.error("Embedding data not found. Please make sure embeddings are generated and saved.")
        
        st.markdown("""
        ### How to Generate Embeddings
        
        To use this visualization, you need to:
        
        1. Generate embeddings for your review texts
        2. Save them in a file named 'DisneylandReviews_Embedded_progress_1750.csv' in the data/A1 folder
        3. The file should include 'review_id' and 'embedding_str' columns
        
        Embeddings allow us to represent text as numbers that can be visualized in 2D space.
        """)