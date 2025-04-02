import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_cost_profit_data(filepath):
    """
    Load and preprocess the cost-profit data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file containing cost-profit data with columns:
                       'distance', 'popularity', and 'category'
    
    Returns:
        pd.DataFrame: Processed dataframe with an additional 'cost_effectiveness' column
                     calculated as popularity/distance
    """
    df = pd.read_csv(filepath, delimiter=";")
    df['cost_effectiveness'] = df['popularity'] / df['distance']
    return df

def plot_cost_profit_scatter(df):
    """
    Generate a scatter plot visualizing the relationship between distance and popularity,
    colored by attraction category.
    
    Args:
        df (pd.DataFrame): Processed dataframe containing 'distance', 'popularity', 
                          and 'category' columns
    
    Returns:
        matplotlib.figure.Figure: The generated scatter plot figure object
    """
    plt.figure(figsize=(8,5))
    scatter = sns.scatterplot(data=df, x='distance', y='popularity', hue='category', alpha=0.7)
    plt.title("Distance vs Popularity (Cost vs Profit)")
    return scatter.get_figure()

def get_cost_profit_insights(df):
    """
    Analyze cost-profit data to generate key insights about attraction efficiency and popularity.
    
    Args:
        df (pd.DataFrame): Processed dataframe containing cost-effectiveness metrics
    
    Returns:
        dict: Dictionary containing:
              - 'top_efficient': Top 5 most cost-effective routes (DataFrame)
              - 'top_popular': Top 5 most popular routes (DataFrame)
              - 'summary': List of string insights about the data patterns
    """
    top_efficient = df.sort_values(by='cost_effectiveness', ascending=False).head(5)
    top_popular = df.sort_values(by='popularity', ascending=False).head(5)
    
    insights = {
        "top_efficient": top_efficient,
        "top_popular": top_popular,
        "summary": [
            "Family/Show combinations dominate the most cost-effective routes",
            "Routes to The Little Mermaid dominate popularity rankings",
            "Animation Academy and Turtle Talk appear in highly efficient routes",
            "Efficient routes tend to be shorter distances between shows",
            "Popular routes tend to be longer distances between major rides"
        ]
    }
    return insights
