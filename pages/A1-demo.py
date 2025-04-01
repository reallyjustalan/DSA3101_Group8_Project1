import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
import html

st.set_page_config(layout="wide")
st.title("Disneyland Reviews Analysis")

# Load data
@st.cache_data
def load_data():
    df_coded = pd.read_csv("data/A1/DisneylandReviews_Coded.csv")
    df_sample = pd.read_csv("data/A1/DisneylandReviews_Sample.csv")
    df_sample = df_sample.rename(columns={'Review_ID': "review_id"})
    
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

df_analysis, merged_df = load_data()

# Calculate correlations
def calculate_correlations(df):
    numeric_df = df.select_dtypes(include="number")
    corr_matrix = numeric_df.corr(method="pearson")
    corr_with_rating = corr_matrix["Rating"].sort_values(ascending=False)
    return corr_with_rating

corr_with_rating = calculate_correlations(df_analysis)

# Add custom CSS for highlighted text tooltips
st.markdown("""
<style>
.tooltip-text {
    position: relative;
    display: inline-block;
    border-bottom: 2px dotted #999;
    cursor: pointer;
}

.tooltip-text.positive, .tooltip-text.very_positive {
    background-color: rgba(0, 255, 0, 0.2);
    border-bottom: 2px dotted green;
}

.tooltip-text.negative, .tooltip-text.very_negative {
    background-color: rgba(255, 0, 0, 0.2);
    border-bottom: 2px dotted red;
}

.tooltip-text.neutral {
    background-color: rgba(255, 255, 0, 0.2);
    border-bottom: 2px dotted orange;
}

.tooltip-text .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: #555;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -100px;
    opacity: 0;
    transition: opacity 0.3s;
}

.tooltip-text:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
</style>
""", unsafe_allow_html=True)

# Add JavaScript for better tooltip experience
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', (event) => {
    // Add event listeners to tooltips
    const tooltips = document.querySelectorAll('.tooltip-text');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const tooltiptext = this.querySelector('.tooltiptext');
            tooltiptext.style.visibility = 'visible';
            tooltiptext.style.opacity = '1';
        });
        
        tooltip.addEventListener('mouseleave', function() {
            const tooltiptext = this.querySelector('.tooltiptext');
            tooltiptext.style.visibility = 'hidden';
            tooltiptext.style.opacity = '0';
        });
    });
});
</script>
""", unsafe_allow_html=True)

# Function to highlight text excerpts in the full review text
def highlight_text_excerpts(review_text, excerpts_data):
    """
    Highlights text excerpts in the full review text with tooltips showing 
    touchpoint and sentiment information.
    
    Args:
        review_text (str): The full review text
        excerpts_data (list): A list of dictionaries containing excerpt data
            with keys: 'text_excerpt', 'touchpoint', 'sentiment'
    
    Returns:
        str: HTML for the review text with highlighted excerpts
    """
    # Sort excerpts by length in descending order to avoid nested matches
    excerpts_data = sorted(excerpts_data, key=lambda x: len(x['text_excerpt']), reverse=True)
    
    # Escape HTML entities in the review text
    safe_text = html.escape(review_text)
    
    # Track already highlighted positions to avoid overlaps
    highlighted_positions = []
    
    for excerpt_data in excerpts_data:
        excerpt = excerpt_data['text_excerpt']
        touchpoint = excerpt_data['touchpoint']
        sentiment = excerpt_data['sentiment']
        
        # Skip if excerpt is empty
        if not excerpt or not isinstance(excerpt, str):
            continue
            
        # Get sentiment class for styling
        sentiment_class = 'positive' if 'positive' in sentiment else 'negative' if 'negative' in sentiment else 'neutral'
        
        # Define tooltip content
        tooltip_content = f"{touchpoint} ({sentiment})"
        
        # Find all occurrences of the excerpt in the text
        safe_excerpt = re.escape(html.escape(excerpt))
        
        # Find all matches and their positions
        for match in re.finditer(safe_excerpt, safe_text, re.IGNORECASE):
            start, end = match.span()
            
            # Check if this position overlaps with any already highlighted text
            overlap = False
            for pos_start, pos_end in highlighted_positions:
                if start < pos_end and end > pos_start:
                    overlap = True
                    break
                    
            if not overlap:
                # Add tooltip HTML
                tooltip_html = f'<span class="tooltip-text {sentiment_class}">{safe_text[start:end]}<span class="tooltiptext">{tooltip_content}</span></span>'
                
                # Replace the excerpt with the highlighted version
                safe_text = safe_text[:start] + tooltip_html + safe_text[end:]
                
                # Adjust positions for all subsequent replacements
                highlighted_positions.append((start, end))
                for i in range(len(highlighted_positions)):
                    if highlighted_positions[i][0] > end:
                        # Update positions after the current replacement
                        pos_start, pos_end = highlighted_positions[i]
                        highlighted_positions[i] = (
                            pos_start + len(tooltip_html) - (end - start),
                            pos_end + len(tooltip_html) - (end - start)
                        )
                        
                # We need to recompute matches after modifying the text
                break
    
    # Replace newlines with <br> tags for proper HTML rendering
    safe_text = safe_text.replace('\n', '<br>')
    
    return safe_text

# Display in tabs
tab1, tab2, tab3 = st.tabs(["Correlation Analysis", "Examples of Reviews", "Raw Data"])

with tab1:
    st.header("Correlation Between Touchpoints and Ratings")

    # Filter out the Rating correlation with itself
    filtered_corr = corr_with_rating[corr_with_rating.index != 'Rating']
    
    # Set number of top/bottom correlations to display
    num_correlations = st.slider("Number of top/bottom correlations to display:", 3, 10, 5)
    
    # Get top positive and negative correlations
    top_positive = filtered_corr.nlargest(num_correlations)
    top_negative = filtered_corr.nsmallest(num_correlations)
    
    # Create a dataframe for visualization
    top_corrs = pd.concat([top_positive, top_negative])
    top_corrs = top_corrs.reset_index()
    top_corrs.columns = ['Touchpoint_Sentiment', 'Correlation']
    
    # Clean up touchpoint names for display
    top_corrs['Touchpoint'] = top_corrs['Touchpoint_Sentiment'].apply(lambda x: x.split('_')[0])
    top_corrs['Sentiment'] = top_corrs['Touchpoint_Sentiment'].apply(lambda x: x.split('_')[1])
    
    # Create a color map
    colors = ['#1e88e5' if x > 0 else '#ff5252' for x in top_corrs['Correlation']]
    
    # Plot horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(top_corrs['Touchpoint_Sentiment'], top_corrs['Correlation'], color=colors)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    ax.set_xlabel('Correlation with Rating')
    ax.set_title('Top Correlations with Guest Ratings')
    
    # Add labels with correlation values
    for i, bar in enumerate(bars):
        width = bar.get_width()
        label_x_pos = width + 0.01 if width > 0 else width - 0.08
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, 
                f'{top_corrs["Correlation"].iloc[i]:.2f}', 
                va='center', fontsize=10)
    
    st.pyplot(fig)
    
    st.subheader("Key Insights")
    
    # Add touchpoint category descriptions
    touchpoint_descriptions = {
        "staff": "Employee interactions (ride operators, food service staff, retail employees, etc.)",
        "attractions": "Rides, interactive exhibits, wait times, ride operations",
        "pre-visit": "Planning, booking, website experience, app usage before arrival",
        "entry/admission": "Parking, tickets, entry gates, security screening, arrival experience, cost of admission",
        "entertainment": "Parades, shows, fireworks, street performers",
        "characters": "Character meet-and-greets, character interactions, photo opportunities",
        "food/beverage": "Restaurants, snack stands, food quality, dining experience, its associated costs",
        "retail": "Shopping experiences, merchandise, souvenirs, cost of merchandise",
        "facilities": "Restrooms, baby care, first aid, accessibility features",
        "cleanliness": "Park maintenance, trash management, overall park cleanliness",
        "navigation": "Park layout, wayfinding, walking experience, crowding, in park transportation",
        "atmosphere": "Theming, ambiance, music, decorations, overall feel",
        "timing": "Time of visit directly impacts satisfaction (\"weekday visits are better\")",
        "comparison": "Comparing to other Disney parks or similar attractions",
        "recommendation": "Specific statements about recommending or not recommending the park to others"
    }
    
    # Get top positive correlations (excluding Rating itself)
    top_pos = filtered_corr.nlargest(3)
    st.write("**Most positive impact on ratings:**")
    for idx, val in top_pos.items():
        touchpoint = idx.split('_')[0]
        sentiment = idx.split('_')[1]
        st.write(f"• **{touchpoint}** ({sentiment}): {val:.3f} correlation")
        if touchpoint in touchpoint_descriptions:
            st.write(f"  <span style='color:gray; font-size:0.9em'>{touchpoint_descriptions[touchpoint]}</span>", unsafe_allow_html=True)
    
    # Get top negative correlations
    top_neg = filtered_corr.nsmallest(3)
    st.write("**Most negative impact on ratings:**")
    for idx, val in top_neg.items():
        touchpoint = idx.split('_')[0]
        sentiment = idx.split('_')[1]
        st.write(f"• **{touchpoint}** ({sentiment}): {val:.3f} correlation")
        if touchpoint in touchpoint_descriptions:
            st.write(f"  <span style='color:gray; font-size:0.9em'>{touchpoint_descriptions[touchpoint]}</span>", unsafe_allow_html=True)
    
    # Show correlation heatmap
    st.subheader("Correlation Heatmap")
    # Take top 10 correlated touchpoints
    top_touchpoints = pd.concat([filtered_corr.nlargest(5), filtered_corr.nsmallest(5)])
    selected_cols = list(top_touchpoints.index) + ['Rating']
    
    # Subset the correlation matrix
    numeric_df = df_analysis.select_dtypes(include="number")
    corr_subset = numeric_df[selected_cols].corr()
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_subset, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax, 
                fmt='.2f', linewidths=0.5)
    plt.tight_layout()
    st.pyplot(fig)

with tab2:
    st.header("Example Reviews with Highlighted Touchpoints")
    
    # Use predefined touchpoints from the original prompt with descriptions
    touchpoint_descriptions = {
        "staff": "Employee interactions (ride operators, food service staff, retail employees, etc.)",
        "attractions": "Rides, interactive exhibits, wait times, ride operations",
        "pre-visit": "Planning, booking, website experience, app usage before arrival",
        "entry/admission": "Parking, tickets, entry gates, security screening, arrival experience, cost of admission",
        "entertainment": "Parades, shows, fireworks, street performers",
        "characters": "Character meet-and-greets, character interactions, photo opportunities",
        "food/beverage": "Restaurants, snack stands, food quality, dining experience, its associated costs",
        "retail": "Shopping experiences, merchandise, souvenirs, cost of merchandise",
        "facilities": "Restrooms, baby care, first aid, accessibility features",
        "cleanliness": "Park maintenance, trash management, overall park cleanliness",
        "navigation": "Park layout, wayfinding, walking experience, crowding, in park transportation",
        "atmosphere": "Theming, ambiance, music, decorations, overall feel",
        "timing": "Time of visit directly impacts satisfaction (\"weekday visits are better\")",
        "comparison": "Comparing to other Disney parks or similar attractions",
        "recommendation": "Specific statements about recommending or not recommending the park to others"
    }
    
    all_touchpoints = list(touchpoint_descriptions.keys())
    selected_touchpoint = st.selectbox("Select a touchpoint to see example reviews:", all_touchpoints)
    
    # Show description of selected touchpoint
    if selected_touchpoint in touchpoint_descriptions:
        st.info(f"**{selected_touchpoint}**: {touchpoint_descriptions[selected_touchpoint]}")
    
    if selected_touchpoint:
        # Get sentiments for the selected touchpoint
        sentiments = sorted(list(set([col.split('_')[1] for col in df_analysis.columns 
                              if '_' in col and col.split('_')[0] == selected_touchpoint])))
        
        sentiment_options = ["All sentiments"] + sentiments
        selected_sentiment = st.selectbox("Filter by sentiment:", sentiment_options)
        
        # Find reviews with this touchpoint
        if selected_sentiment == "All sentiments":
            relevant_reviews = merged_df[merged_df['touchpoint'] == selected_touchpoint]
        else:
            relevant_reviews = merged_df[
                (merged_df['touchpoint'] == selected_touchpoint) & 
                (merged_df['sentiment'] == selected_sentiment)
            ]
        
        # Get unique review IDs
        unique_review_ids = relevant_reviews['review_id'].unique()
        
        if len(unique_review_ids) > 0:
            st.write(f"Found {len(unique_review_ids)} reviews mentioning '{selected_touchpoint}'")
            
            # Get sample reviews
            num_examples = min(5, len(unique_review_ids))
            max_examples = min(20, len(unique_review_ids))
            num_to_show = st.slider("Number of example reviews to show:", 1, max_examples, num_examples)
            
            # Sample reviews
            sampled_review_ids = unique_review_ids[:num_to_show]
            
            # Display each sample review with highlighted excerpts
            for i, review_id in enumerate(sampled_review_ids):
                # Get full review text
                review_data = df_analysis[df_analysis['review_id'] == review_id].iloc[0]
                review_text = review_data['Review_Text']
                rating = review_data['Rating']
                branch = review_data['Branch']
                
                # Get all excerpts for this review
                review_excerpts = merged_df[merged_df['review_id'] == review_id]
                
                # Prepare excerpt data for highlighting
                excerpts_data = review_excerpts[['text_excerpt', 'touchpoint', 'sentiment']].to_dict('records')
                
                # Create highlighted review text with tooltips
                highlighted_text = highlight_text_excerpts(review_text, excerpts_data)
                
                # Display in an expander
                with st.expander(f"Review #{i+1} - Rating: {rating} stars (Branch: {branch})", expanded=(i==0)):
                    # Instructions
                    st.info("Hover over the highlighted text to see touchpoint and sentiment information")
                    
                    # Display the highlighted text
                    st.markdown(highlighted_text, unsafe_allow_html=True)
                    
                    # Show coded touchpoints as a table for reference
                    st.write("**Coded touchpoints in this review:**")
                    
                    # Create a DataFrame with touchpoint information
                    touchpoints_df = review_excerpts[['touchpoint', 'sentiment', 'text_excerpt']].copy()
                    
                    # Add color to sentiment
                    def color_sentiment(val):
                        if val == 'positive' or val == 'very_positive':
                            return 'background-color: rgba(0, 255, 0, 0.2)'
                        elif val == 'negative' or val == 'very_negative':
                            return 'background-color: rgba(255, 0, 0, 0.2)'
                        else:
                            return 'background-color: rgba(255, 255, 0, 0.2)'
                    
                    # Display styled table
                    st.dataframe(touchpoints_df.style.applymap(color_sentiment, subset=['sentiment']))
        else:
            st.write(f"No reviews found mentioning '{selected_touchpoint}'.")

with tab3:
    st.header("Raw Data")
    st.dataframe(df_analysis)
    
    # Show coded data
    st.subheader("Coded Excerpts Data")
    st.dataframe(merged_df[['review_id', 'touchpoint', 'sentiment', 'text_excerpt']])
    
    # Download option
    csv = df_analysis.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="disneyland_reviews_analysis.csv",
        mime="text/csv"
    )

# Add instructions at the bottom
st.markdown("""
### How to Use This Dashboard

1. **Correlation Analysis**: See which touchpoints have the most positive or negative impact on ratings
2. **Review Examples**: Browse real reviews with highlighted touchpoints - hover over highlighted text to see touchpoint and sentiment details
3. **Raw Data**: Explore and download the full dataset

This dashboard helps identify key factors affecting guest satisfaction at Disneyland based on review analysis.
""")