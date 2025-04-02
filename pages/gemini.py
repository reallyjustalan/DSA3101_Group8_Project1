import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ast
from sklearn.decomposition import PCA
import umap.umap_ as umap
import datetime
from scipy.stats import chi2_contingency
import json
from streamlit_plotly_events import plotly_events

# Set page configuration
st.set_page_config(
    page_title="Disney Customer Experience Dashboard",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2070b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #044389;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .subsection-header {
        font-size: 1.4rem;
        color: #0a66c2;
        margin-top: 0.8rem;
        margin-bottom: 0.3rem;
    }
    .info-box {
        background-color: #f0f7ff;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        padding: 1rem;
        text-align: center;
    }
    .highlight-text {
        color: #ff5757;
        font-weight: bold;
    }
    .positive-sentiment {
        color: #28a745;
        font-weight: bold;
    }
    .negative-sentiment {
        color: #dc3545;
        font-weight: bold;
    }
    .neutral-sentiment {
        color: #6c757d;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the Disney review data"""
    try:
        # Load the main datasets
        original_reviews = pd.read_csv("data/A1/DisneylandReviews_Sample.csv")
        coded_reviews = pd.read_csv("data/A1/DisneylandReviews_Coded.csv")
        
        # Convert embeddings from string to numpy arrays if they exist
        try:
            embedded_reviews = pd.read_csv("data/A1/DisneylandReviews_Embedded.csv")
            
            # Convert string representation of embeddings to actual arrays
            # Only process rows where the embedding is not NaN
            def parse_embedding(emb_str):
                if isinstance(emb_str, str):
                    try:
                        # Remove brackets and split by commas
                        values = emb_str.strip('[]').split(',')
                        # Convert strings to floats
                        return np.array([float(x) for x in values])
                    except:
                        return None
                return None
            
            embedded_reviews['embedding_array'] = embedded_reviews['embedding'].apply(parse_embedding)
        except:
            st.warning("Embedded reviews file not found. Some visualizations will be disabled.")
            embedded_reviews = None
        
        # Merge original review data with coded data
        if 'review_id' in coded_reviews.columns:
            # Join coded reviews with original data to get additional fields
            original_reviews = original_reviews.rename(columns={'Review_ID': 'review_id'}) if 'Review_ID' in original_reviews.columns else original_reviews
            
            # Get unique review IDs from coded_reviews
            unique_review_ids = coded_reviews['review_id'].unique()
            
            # Filter original_reviews to only include those IDs
            filtered_original_reviews = original_reviews[original_reviews['review_id'].isin(unique_review_ids)]
            
            # Convert date columns if they exist
            date_columns = ['Year_Month', 'Review_Date']
            for col in date_columns:
                if col in filtered_original_reviews.columns:
                    filtered_original_reviews[col] = pd.to_datetime(filtered_original_reviews[col], errors='coerce')
        else:
            filtered_original_reviews = original_reviews
            
        return {
            'original_reviews': original_reviews,
            'filtered_original_reviews': filtered_original_reviews,
            'coded_reviews': coded_reviews,
            'embedded_reviews': embedded_reviews
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def prepare_analytics_data(data):
    """Prepare processed data for analytics"""
    try:
        # Extract key metrics and aggregations
        df = data['coded_reviews']
        
        # Touchpoint frequency and sentiment analysis
        touchpoint_metrics = df.groupby('touchpoint')['sentiment'].value_counts().unstack(fill_value=0)
        
        # Add total column
        touchpoint_metrics['total'] = touchpoint_metrics.sum(axis=1)
        
        # Calculate sentiment percentages
        for sentiment in ['positive', 'negative', 'neutral']:
            if sentiment in touchpoint_metrics.columns:
                touchpoint_metrics[f'{sentiment}_pct'] = (touchpoint_metrics[sentiment] / touchpoint_metrics['total'] * 100).round(1)
        
        # Calculate impact scores (simplified version)
        # Here we're using a simple ratio of positive to negative mentions as a proxy for impact
        touchpoint_metrics['impact_score'] = touchpoint_metrics.apply(
            lambda x: (x.get('positive', 0) - x.get('negative', 0)) / x['total'] if x['total'] > 0 else 0, 
            axis=1
        ).round(2)
        
        # Calculate correlation scores if Rating is available in original reviews
        if 'filtered_original_reviews' in data and 'Rating' in data['filtered_original_reviews'].columns:
            # Merge ratings with touchpoint data
            reviews_with_ratings = pd.merge(
                df,
                data['filtered_original_reviews'][['review_id', 'Rating']],
                on='review_id',
                how='inner'
            )
            
            # Calculate correlation by touchpoint
            touchpoint_correlations = {}
            for touchpoint in df['touchpoint'].unique():
                touchpoint_df = reviews_with_ratings[reviews_with_ratings['touchpoint'] == touchpoint]
                
                # Create numeric sentiment values (positive=1, neutral=0, negative=-1)
                touchpoint_df['sentiment_value'] = touchpoint_df['sentiment'].map({
                    'positive': 1,
                    'neutral': 0,
                    'negative': -1
                })
                
                # Calculate correlation between sentiment and rating
                if touchpoint_df.shape[0] > 5:  # Need enough data points
                    correlation = touchpoint_df[['sentiment_value', 'Rating']].corr().iloc[0, 1]
                    touchpoint_correlations[touchpoint] = round(correlation, 2)
            
            touchpoint_metrics['correlation_score'] = pd.Series(touchpoint_correlations)
        
        # Sort by total mentions
        touchpoint_metrics = touchpoint_metrics.sort_values('total', ascending=False)
        
        # Top codes by touchpoint
        top_codes = df.groupby(['touchpoint', 'code']).size().reset_index(name='count')
        top_codes = top_codes.sort_values(['touchpoint', 'count'], ascending=[True, False])
        top_codes_by_touchpoint = {}
        
        for touchpoint in df['touchpoint'].unique():
            top_codes_by_touchpoint[touchpoint] = top_codes[top_codes['touchpoint'] == touchpoint].head(5)
        
        # Demographics analysis
        demo_cols = ['travel_party', 'first_visit', 'visit_timing']
        demographics = {}
        
        for col in demo_cols:
            if col in df.columns:
                # Get frequency counts, handling NaNs
                demo_counts = df[col].fillna('Not specified').value_counts().to_dict()
                demographics[col] = demo_counts
        
        # Prepare sentiment by demographic
        sentiment_by_demographic = {}
        
        for col in demo_cols:
            if col in df.columns:
                # Create a contingency table
                temp = df.dropna(subset=[col]).pivot_table(
                    index=col, 
                    columns='sentiment', 
                    values='review_id', 
                    aggfunc='count', 
                    fill_value=0
                )
                
                # Calculate percentages
                row_totals = temp.sum(axis=1)
                temp_pct = temp.div(row_totals, axis=0) * 100
                sentiment_by_demographic[col] = temp_pct
        
        # Get representative reviews (examples of extremely positive or negative experiences)
        if 'review_text' in data['filtered_original_reviews'].columns:
            # Join with the original text
            df_with_text = pd.merge(
                df, 
                data['filtered_original_reviews'][['review_id', 'review_text' if 'review_text' in data['filtered_original_reviews'].columns else 'Review_Text']], 
                on='review_id'
            )
            
            # Get examples of positive and negative reviews for each touchpoint
            representative_reviews = {}
            
            for touchpoint in df['touchpoint'].unique():
                touchpoint_df = df_with_text[df_with_text['touchpoint'] == touchpoint]
                
                # Get examples by sentiment
                representative_reviews[touchpoint] = {
                    'positive': touchpoint_df[touchpoint_df['sentiment'] == 'positive'].head(3).to_dict('records'),
                    'negative': touchpoint_df[touchpoint_df['sentiment'] == 'negative'].head(3).to_dict('records')
                }
        else:
            representative_reviews = None
            
        return {
            'touchpoint_metrics': touchpoint_metrics,
            'top_codes_by_touchpoint': top_codes_by_touchpoint,
            'demographics': demographics,
            'sentiment_by_demographic': sentiment_by_demographic,
            'representative_reviews': representative_reviews
        }
    except Exception as e:
        st.error(f"Error preparing analytics data: {e}")
        return None

@st.cache_data
def compute_vector_projections(embedded_reviews):
    """Compute 2D/3D projections of embeddings for visualization"""
    if embedded_reviews is None or 'embedding_array' not in embedded_reviews.columns:
        return None
    
    # Filter out rows with None embeddings
    valid_embeddings = embedded_reviews.dropna(subset=['embedding_array'])
    
    if len(valid_embeddings) == 0:
        return None
    
    # Stack the embedding arrays into a single numpy array
    embedding_matrix = np.vstack(valid_embeddings['embedding_array'].values)
    
    # Generate 2D projection using PCA (faster than UMAP for initial visualization)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(embedding_matrix)
    
    # Add projection results to dataframe
    projection_df = valid_embeddings.copy()
    projection_df['x'] = pca_result[:, 0]
    projection_df['y'] = pca_result[:, 1]
    
    # Try to generate UMAP projection if dataset is not too large
    if len(valid_embeddings) <= 5000:  # UMAP can be slow for very large datasets
        try:
            reducer = umap.UMAP(random_state=42)
            umap_result = reducer.fit_transform(embedding_matrix)
            projection_df['umap_x'] = umap_result[:, 0]
            projection_df['umap_y'] = umap_result[:, 1]
        except:
            st.warning("UMAP projection failed. Only PCA projection will be available.")
    
    return projection_df

def render_executive_summary(data, analytics):
    """Render the executive summary section"""
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    
    # Top row with sentiment and impact
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="subsection-header">Overall Sentiment</div>', unsafe_allow_html=True)
        
        # Calculate overall sentiment distribution
        sentiment_counts = data['coded_reviews']['sentiment'].value_counts()
        total_sentiments = sentiment_counts.sum()
        sentiment_pcts = (sentiment_counts / total_sentiments * 100).round(1)
        
        # Create a gauge chart to show the sentiment ratio
        positive_pct = sentiment_pcts.get('positive', 0)
        negative_pct = sentiment_pcts.get('negative', 0)
        neutral_pct = sentiment_pcts.get('neutral', 0)
        
        # Create a pie chart
        fig = go.Figure(data=[go.Pie(
            labels=['Positive', 'Neutral', 'Negative'],
            values=[positive_pct, neutral_pct, negative_pct],
            hole=.4,
            marker_colors=['#28a745', '#6c757d', '#dc3545']
        )])
        
        fig.update_layout(
            title_text="Sentiment Distribution",
            showlegend=True,
            height=300,
            margin=dict(l=20, r=20, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        metrics_cols = st.columns(3)
        with metrics_cols[0]:
            total_reviews = len(data['coded_reviews']['review_id'].unique())
            st.metric("Total Reviews Analyzed", total_reviews)
        with metrics_cols[1]:
            total_touchpoints = len(data['coded_reviews']['touchpoint'].unique())
            st.metric("Touchpoints Identified", total_touchpoints)
        with metrics_cols[2]:
            st.metric("Coded Elements", len(data['coded_reviews']))
        
    with col2:
        st.markdown('<div class="subsection-header">Touchpoint Impact</div>', unsafe_allow_html=True)
        
        # Get touchpoint impact metrics
        # Filter out 'general' and 'overall' touchpoints if they exist
        impact_metrics = analytics['touchpoint_metrics'][['impact_score', 'total']]
        impact_metrics = impact_metrics[~impact_metrics.index.isin(['general', 'overall'])]
        impact_metrics = impact_metrics.sort_values('impact_score')
        
        # Create horizontal bar chart
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            y=impact_metrics.index,
            x=impact_metrics['impact_score'],
            orientation='h',
            marker_color=impact_metrics['impact_score'].apply(
                lambda x: '#28a745' if x > 0.2 else '#dc3545' if x < -0.2 else '#6c757d'
            ),
            text=impact_metrics['impact_score'].round(2),
            textposition='auto',
            name='Impact Score'
        ))
        
        fig.update_layout(
            title_text="Touchpoint Impact Score",
            xaxis_title="Impact (Positive to Negative Ratio)",
            height=500,
            margin=dict(l=20, r=20, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row with key insights below the charts
    st.markdown('<div class="subsection-header">Key Insights</div>', unsafe_allow_html=True)
    
    insights_cols = st.columns(2)
    
    with insights_cols[0]:
        # Identify best performing touchpoints
        top_touchpoints = analytics['touchpoint_metrics'].sort_values('impact_score', ascending=False).head(3)
        top_touchpoints = top_touchpoints[~top_touchpoints.index.isin(['general', 'overall'])]
        
        st.markdown("#### Strengths")
        for idx, (touchpoint, row) in enumerate(top_touchpoints.iterrows()):
            st.markdown(f"**{idx+1}. {touchpoint.capitalize()}** (Impact: {row['impact_score']:.2f})")
            
            # Show top codes
            if touchpoint in analytics['top_codes_by_touchpoint']:
                top_codes = analytics['top_codes_by_touchpoint'][touchpoint]
                if not top_codes.empty:
                    st.markdown("*Top associated codes:*")
                    for _, code_row in top_codes.iterrows():
                        st.markdown(f"- {code_row['code']} ({code_row['count']} mentions)")
    
    with insights_cols[1]:
        # Identify worst performing touchpoints
        bottom_touchpoints = analytics['touchpoint_metrics'].sort_values('impact_score').head(3)
        bottom_touchpoints = bottom_touchpoints[~bottom_touchpoints.index.isin(['general', 'overall'])]
        
        st.markdown("#### Improvement Areas")
        for idx, (touchpoint, row) in enumerate(bottom_touchpoints.iterrows()):
            st.markdown(f"**{idx+1}. {touchpoint.capitalize()}** (Impact: {row['impact_score']:.2f})")
            
            # Show top codes
            if touchpoint in analytics['top_codes_by_touchpoint']:
                top_codes = analytics['top_codes_by_touchpoint'][touchpoint]
                if not top_codes.empty:
                    st.markdown("*Top associated codes:*")
                    for _, code_row in top_codes.iterrows():
                        st.markdown(f"- {code_row['code']} ({code_row['count']} mentions)")


def render_touchpoint_analysis(data, analytics):
    """Render the touchpoint analysis section"""
    st.markdown('<div class="section-header">Touchpoint Analysis</div>', unsafe_allow_html=True)
    
    # Define allowed touchpoints
    allowed_touchpoints = [
        'staff', 'attractions', 'pre-visit', 'entry/admission', 'entertainment', 
        'characters', 'food/beverage', 'retail', 'facilities', 'cleanliness', 
        'navigation', 'atmosphere', 'timing', 'comparison', 'recommendation'
    ]
    
    # Apply filters to get filtered dataframe
    filtered_df = data['coded_reviews'].copy()
    # Filter to only include allowed touchpoints
    filtered_df = filtered_df[filtered_df['touchpoint'].isin(allowed_touchpoints)]
    
    # Create sentiment pivot table
    sentiment_pivot = filtered_df.pivot_table(
        index='touchpoint', 
        columns='sentiment', 
        values='review_id', 
        aggfunc='count', 
        fill_value=0
    )
    
    # Add total column
    sentiment_pivot['total'] = sentiment_pivot.sum(axis=1)
    
    # Calculate percentages
    for col in sentiment_pivot.columns:
        if col != 'total':
            sentiment_pivot[f'{col}_pct'] = sentiment_pivot[col] / sentiment_pivot['total'] * 100
    
    
    # Display top codes for each touchpoint
    st.markdown('<div class="subsection-header">Top Themes by Touchpoint</div>', unsafe_allow_html=True)
    
    # Get top codes for each touchpoint
    top_codes = filtered_df.groupby(['touchpoint', 'code']).size().reset_index(name='count')
    top_codes = top_codes.sort_values(['touchpoint', 'count'], ascending=[True, False])
    
    top_touchpoints = sentiment_pivot.index.tolist()
    
    tabs = st.tabs(top_touchpoints)
    
    for i, touchpoint in enumerate(top_touchpoints):
        with tabs[i]:
            touchpoint_df = filtered_df[filtered_df['touchpoint'] == touchpoint]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Show top codes overall
                st.markdown(f"##### Top Codes for {touchpoint.capitalize()}")
                top_touchpoint_codes = top_codes[top_codes['touchpoint'] == touchpoint].head(10)
                
                if not top_touchpoint_codes.empty:
                    # Create a horizontal bar chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        y=top_touchpoint_codes['code'],
                        x=top_touchpoint_codes['count'],
                        orientation='h',
                        marker_color='#1f77b4'
                    ))
                    
                    fig.update_layout(
                        xaxis_title="Count",
                        yaxis_title="Code",
                        height=350,
                        margin=dict(l=20, r=20, t=20, b=20)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No codes found for this touchpoint.")
            
            with col2:
                # Show sentiment breakdown for codes
                st.markdown(f"##### Sentiment by Code for {touchpoint.capitalize()}")
                
                # Get sentiment breakdown by code
                code_sentiment = touchpoint_df.groupby(['code', 'sentiment']).size().reset_index(name='count')
                
                # Get top codes by total count
                top_codes_by_count = touchpoint_df.groupby('code').size().reset_index(name='count')
                top_codes_by_count = top_codes_by_count.sort_values('count', ascending=False).head(10)
                
                # Filter code_sentiment to only include top codes
                code_sentiment = code_sentiment[code_sentiment['code'].isin(top_codes_by_count['code'])]
                
                # Pivot to get codes as rows and sentiments as columns
                pivot_code_sentiment = code_sentiment.pivot_table(
                    index='code',
                    columns='sentiment',
                    values='count',
                    fill_value=0
                )
                
                # Ensure all sentiment columns exist
                for sentiment in ['positive', 'negative', 'neutral']:
                    if sentiment not in pivot_code_sentiment.columns:
                        pivot_code_sentiment[sentiment] = 0
                
                # Create a grouped bar chart
                fig = go.Figure()
                
                for sentiment, color in zip(['positive', 'negative', 'neutral'], ['#28a745', '#dc3545', '#6c757d']):
                    if sentiment in pivot_code_sentiment.columns:
                        fig.add_trace(go.Bar(
                            y=pivot_code_sentiment.index,
                            x=pivot_code_sentiment[sentiment],
                            name=sentiment.capitalize(),
                            orientation='h',
                            marker_color=color
                        ))
                
                fig.update_layout(
                    xaxis_title="Count",
                    yaxis_title="Code",
                    barmode='stack',
                    height=350,
                    margin=dict(l=20, r=20, t=20, b=20),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Show representative quotes
            st.markdown("##### Representative Quotes")
            
            quote_cols = st.columns(2)
            
            with quote_cols[0]:
                st.markdown("**Positive Examples**")
                positive_examples = touchpoint_df[touchpoint_df['sentiment'] == 'positive'].head(3)
                
                for _, row in positive_examples.iterrows():
                    st.markdown(f"*\"{row['text_excerpt']}\"*")
                    st.markdown(f"**Code**: {row['code']}")
                    st.markdown("---")
            
            with quote_cols[1]:
                st.markdown("**Negative Examples**")
                negative_examples = touchpoint_df[touchpoint_df['sentiment'] == 'negative'].head(3)
                
                for _, row in negative_examples.iterrows():
                    st.markdown(f"*\"{row['text_excerpt']}\"*")
                    st.markdown(f"**Code**: {row['code']}")
                    st.markdown("---")

def render_deep_dive(data, analytics, projections):
    """Render the deep dive analysis section"""
    st.markdown('<div class="section-header">Deep Dive Analysis</div>', unsafe_allow_html=True)
    
    # Create tabs for different analyses
    tabs = st.tabs(["Sentiment Trends", "Vector Space Exploration", "Review Explorer"])
    
    with tabs[0]:
        st.markdown("#### Sentiment Trends")
        
        # Check if we have date information
        has_dates = False
        date_col = None
        
        if 'filtered_original_reviews' in data:
            date_cols = ['Year_Month', 'Review_Date']
            for col in date_cols:
                if col in data['filtered_original_reviews'].columns and pd.api.types.is_datetime64_any_dtype(data['filtered_original_reviews'][col]):
                    has_dates = True
                    date_col = col
                    break
        
        if has_dates:
            # Create a date-based analysis
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Filter options
                touchpoints = sorted(data['coded_reviews']['touchpoint'].unique().tolist())
                selected_touchpoint = st.selectbox("Select Touchpoint", touchpoints, key="trend_touchpoint")
                
                # Date range
                min_date = data['filtered_original_reviews'][date_col].min().date()
                max_date = data['filtered_original_reviews'][date_col].max().date()
                
                date_range = st.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="trend_date_range"
                )
                
                if len(date_range) == 2:
                    start_date, end_date = date_range
                else:
                    start_date, end_date = min_date, max_date
            
            with col2:
                # Filter the data
                review_ids = data['filtered_original_reviews'][(data['filtered_original_reviews'][date_col].dt.date >= start_date) & 
                                                 (data['filtered_original_reviews'][date_col].dt.date <= end_date)]['review_id'].unique()
                
                filtered_reviews = data['coded_reviews'][data['coded_reviews']['review_id'].isin(review_ids)]
                filtered_reviews = filtered_reviews[filtered_reviews['touchpoint'] == selected_touchpoint]
                
                # Join with dates
                filtered_reviews = pd.merge(
                    filtered_reviews,
                    data['filtered_original_reviews'][['review_id', date_col]],
                    on='review_id'
                )
                
                # Group by month and sentiment
                filtered_reviews['month'] = filtered_reviews[date_col].dt.to_period('M')
                sentiment_over_time = filtered_reviews.groupby(['month', 'sentiment']).size().reset_index(name='count')
                
                # Pivot the data
                pivot_sentiment_time = sentiment_over_time.pivot_table(
                    index='month',
                    columns='sentiment',
                    values='count',
                    fill_value=0
                )
                
                # Ensure all sentiment columns exist
                for sentiment in ['positive', 'negative', 'neutral']:
                    if sentiment not in pivot_sentiment_time.columns:
                        pivot_sentiment_time[sentiment] = 0
                
                # Convert period index to datetime for plotting
                pivot_sentiment_time.index = pivot_sentiment_time.index.to_timestamp()
                
                # Create a stacked area chart
                fig = go.Figure()
                
                for sentiment, color in zip(['positive', 'negative', 'neutral'], ['#28a745', '#dc3545', '#6c757d']):
                    if sentiment in pivot_sentiment_time.columns:
                        fig.add_trace(go.Scatter(
                            x=pivot_sentiment_time.index,
                            y=pivot_sentiment_time[sentiment],
                            mode='lines',
                            stackgroup='one',
                            name=sentiment.capitalize(),
                            line=dict(color=color, width=0.8),
                            fillcolor=color
                        ))
                
                fig.update_layout(
                    title=f"Sentiment Trends for {selected_touchpoint.capitalize()} Over Time",
                    xaxis_title="Date",
                    yaxis_title="Count",
                    height=500,
                    margin=dict(l=40, r=40, t=40, b=40),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show NPS-like score over time
                pivot_sentiment_time['nps_score'] = (pivot_sentiment_time['positive'] - pivot_sentiment_time['negative']) / (pivot_sentiment_time['positive'] + pivot_sentiment_time['negative'] + pivot_sentiment_time['neutral']) * 100
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=pivot_sentiment_time.index,
                    y=pivot_sentiment_time['nps_score'],
                    mode='lines+markers',
                    name='Sentiment Score',
                    line=dict(color='#1f77b4', width=2),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title=f"Sentiment Score for {selected_touchpoint.capitalize()} Over Time",
                    xaxis_title="Date",
                    yaxis_title="Sentiment Score (-100 to 100)",
                    height=300,
                    margin=dict(l=40, r=40, t=40, b=40),
                    yaxis=dict(range=[-100, 100])
                )
                
                # Add a horizontal line at y=0
                fig.add_shape(
                    type="line",
                    x0=pivot_sentiment_time.index.min(),
                    x1=pivot_sentiment_time.index.max(),
                    y0=0,
                    y1=0,
                    line=dict(color="gray", width=1, dash="dash")
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Date information is not available in the data. Sentiment trends analysis is not possible.")
    
    with tabs[1]:
        st.markdown("#### Vector Space Exploration")
        
        if projections is not None:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Filter options
                projection_type = st.radio("Projection Type", ["PCA", "UMAP"], key="projection_type")
                
                if projection_type == "UMAP" and 'umap_x' not in projections.columns:
                    st.warning("UMAP projection is not available. Using PCA instead.")
                    projection_type = "PCA"
                
                # Color by options
                color_by = st.selectbox("Color By", ["touchpoint", "sentiment"], key="vector_color_by")
                
                # Touchpoint filter
                touchpoints = sorted(projections['touchpoint'].unique().tolist())
                selected_touchpoints = st.multiselect("Filter Touchpoints", touchpoints, default=touchpoints[:3], key="vector_touchpoints")
                
                # Point size and opacity
                point_size = st.slider("Point Size", 2, 10, 5, key="vector_point_size")
                opacity = st.slider("Opacity", 0.1, 1.0, 0.7, key="vector_opacity")
            
            with col2:
                # Filter data
                if selected_touchpoints:
                    filtered_projections = projections[projections['touchpoint'].isin(selected_touchpoints)]
                else:
                    filtered_projections = projections
                
                # Determine coordinates based on projection type
                x_col = 'umap_x' if projection_type == "UMAP" else 'x'
                y_col = 'umap_y' if projection_type == "UMAP" else 'y'
                
                # Create scatter plot
                fig = px.scatter(
                    filtered_projections,
                    x=x_col,
                    y=y_col,
                    color=color_by,
                    hover_name="text_excerpt",
                    hover_data=["touchpoint", "sentiment", "code"],
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    opacity=opacity,
                    size_max=point_size
                )
                
                fig.update_layout(
                    title=f"{projection_type} Projection of Review Embeddings",
                    height=600,
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show a sample of the selected points
                st.markdown("#### Sample Points from Selection")
                
                sample_size = min(10, len(filtered_projections))
                sample_points = filtered_projections.sample(sample_size)
                
                for _, row in sample_points.iterrows():
                    st.markdown(f"**Touchpoint**: {row['touchpoint']} | **Sentiment**: {row['sentiment']} | **Code**: {row['code']}")
                    st.markdown(f"*\"{row['text_excerpt']}\"*")
                    st.markdown("---")
        else:
            st.warning("Vector embeddings are not available. Vector space exploration is not possible.")
    
    with tabs[2]:
        st.markdown("#### Review Explorer")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Search options
            search_type = st.radio("Search Type", ["Keyword", "Filter"], key="search_type")
            
            if search_type == "Keyword":
                search_term = st.text_input("Search Term", key="search_term")
                search_field = st.selectbox("Search In", ["text_excerpt", "code"], key="search_field")
            else:
                # Filter options
                touchpoints = sorted(data['coded_reviews']['touchpoint'].unique().tolist())
                selected_touchpoint = st.selectbox("Select Touchpoint", touchpoints, key="explorer_touchpoint")
                
                sentiments = sorted(data['coded_reviews']['sentiment'].unique().tolist())
                selected_sentiment = st.selectbox("Select Sentiment", ["All"] + sentiments, key="explorer_sentiment")
        
        with col2:
            # Get filtered data
            if search_type == "Keyword" and search_term:
                filtered_reviews = data['coded_reviews'][data['coded_reviews'][search_field].str.contains(search_term, case=False, na=False)]
            elif search_type == "Filter":
                filtered_reviews = data['coded_reviews'][data['coded_reviews']['touchpoint'] == selected_touchpoint]
                
                if selected_sentiment != "All":
                    filtered_reviews = filtered_reviews[filtered_reviews['sentiment'] == selected_sentiment]
            else:
                # Default: show a sample
                filtered_reviews = data['coded_reviews'].sample(min(20, len(data['coded_reviews'])))
            
            # Show the results
            st.markdown(f"#### Found {len(filtered_reviews)} Results")
            
            for _, row in filtered_reviews.head(20).iterrows():
                col1, col2, col3 = st.columns([2, 2, 3])
                
                with col1:
                    st.markdown(f"**Touchpoint**: {row['touchpoint']}")
                    
                with col2:
                    sentiment_color = "#28a745" if row['sentiment'] == 'positive' else "#dc3545" if row['sentiment'] == 'negative' else "#6c757d"
                    st.markdown(f"**Sentiment**: <span style='color:{sentiment_color}'>{row['sentiment']}</span>", unsafe_allow_html=True)
                    
                with col3:
                    st.markdown(f"**Code**: {row['code']}")
                
                st.markdown(f"*\"{row['text_excerpt']}\"*")
                st.markdown("---")

def main():
    """Main function to run the dashboard"""
    # Display header
    st.markdown('<h1 class="main-header">Disney Customer Experience Dashboard</h1>', unsafe_allow_html=True)
    # Load data
    with st.spinner("Loading and processing data..."):
        data = load_data()
    if data is None:
        st.error("Failed to load data. Please check the data files and try again.")
        return
    # Process analytics data
    with st.spinner("Analyzing data..."):
        analytics = prepare_analytics_data(data)
    if analytics is None:
        st.error("Failed to analyze data. Please check the analytics preparation and try again.")
        return
    
    # Compute vector projections if embeddings exist
    projections = None
    if 'embedded_reviews' in data and data['embedded_reviews'] is not None:
        with st.spinner("Computing vector projections for visualization..."):
            projections = compute_vector_projections(data['embedded_reviews'])
    
    # Create sidebar
    st.sidebar.markdown("## Dashboard Navigation")
    
    # Navigation options
    nav_options = [
        "Executive Summary",
        "Touchpoint Analysis",
        "Deep Dive Analysis",

    ]
    
    selected_section = st.sidebar.radio("Go to Section", nav_options)
    
    # Add info section to sidebar
    with st.sidebar.expander("About This Dashboard"):
        st.markdown("""
        This dashboard analyzes Disney customer experience using:
        - LLM-based review analysis
        - Vector embeddings for similarity
        - 15 touchpoint categories
        - Sentiment analysis
        
        The dashboard provides actionable insights for Disney operations and strategy teams.
        """)
    
    # Render selected section
    if selected_section == "Executive Summary":
        render_executive_summary(data, analytics)
    elif selected_section == "Touchpoint Analysis":
        render_touchpoint_analysis(data, analytics)
    elif selected_section == "Deep Dive Analysis":
        render_deep_dive(data, analytics, projections)

if __name__ == "__main__":
    main()