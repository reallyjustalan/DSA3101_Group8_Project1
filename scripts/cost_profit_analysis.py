import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_cost_profit_data(filepath):
    """Load and preprocess the cost-profit data"""
    df = pd.read_csv(filepath, delimiter=";")
    df['cost_effectiveness'] = df['popularity'] / df['distance']
    return df

def plot_cost_profit_scatter(df):
    """Create a scatter plot of distance vs popularity"""
    plt.figure(figsize=(8,5))
    scatter = sns.scatterplot(data=df, x='distance', y='popularity', hue='category', alpha=0.7)
    plt.title("Distance vs Popularity (Cost vs Profit)")
    return scatter.get_figure()

def get_cost_profit_insights(df):
    """Generate insights from the cost-profit data"""
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
