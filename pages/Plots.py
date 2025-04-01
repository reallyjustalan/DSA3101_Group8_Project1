import sys
import streamlit as st
from pathlib import Path
import os
import seaborn as sns
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent 
scripts_a2_path = BASE_DIR / "scripts" / "A2"
sys.path.append(str(scripts_a2_path))

import dataprocessing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "../data/A2/updated_disneylandreviews.csv")
df = dataprocessing.load_and_clean_data(csv_path)

df_all = df
df_hongkong = df_all[df_all['Branch'] == 'Disneyland_HongKong']
df_california = df_all[df_all['Branch'] == 'Disneyland_California']
df_paris = df_all[df_all['Branch'] == 'Disneyland_Paris']

def main():
    st.title("Exploratory Data Analysis")
    figures = []

    fig1, axs = plt.subplots(3, 2, figsize=(20, 18))
    datasets = {
        "All Data": df_all,
        "Hong Kong": df_hongkong,
        "California": df_california,
        "Paris": df_paris
    }
    # Average Rating by Continent
    for name, data in datasets.items():
        axs[0, 0].plot(data.groupby('Continent')['Rating'].mean(), marker='o', label=name)
    axs[0, 0].set_title('Average Rating by Continent')
    axs[0, 0].set_xlabel('Continent')
    axs[0, 0].set_ylabel('Average Rating')
    axs[0, 0].legend()

    # Average Sentiment by Continent
    for name, data in datasets.items():
        axs[0, 1].plot(data.groupby('Continent')['Sentiment'].mean(), marker='o', label=name)
    axs[0, 1].set_title('Average Sentiment by Continent')
    axs[0, 1].set_xlabel('Continent')
    axs[0, 1].set_ylabel('Average Sentiment')
    axs[0, 1].legend()

    # Average Rating by Month
    for name, data in datasets.items():
        axs[1, 0].plot(data.groupby('Month')['Rating'].mean(), marker='o', label=name)
    axs[1, 0].set_title('Average Rating by Month')
    axs[1, 0].set_xlabel('Month')
    axs[1, 0].set_ylabel('Average Rating')
    axs[1, 0].legend()

    # Average Sentiment by Month
    for name, data in datasets.items():
        axs[1, 1].plot(data.groupby('Month')['Sentiment'].mean(), marker='o', label=name)
    axs[1, 1].set_title('Average Sentiment by Month')
    axs[1, 1].set_xlabel('Month')
    axs[1, 1].set_ylabel('Average Sentiment')
    axs[1, 1].legend()

    # Average Rating by Year
    for name, data in datasets.items():
        axs[2, 0].plot(data.groupby('Year')['Rating'].mean(), marker='o', label=name)
    axs[2, 0].set_title('Average Rating by Year')
    axs[2, 0].set_xlabel('Year')
    axs[2, 0].set_ylabel('Average Rating')
    axs[2, 0].legend()

    # Average Sentiment by Year
    for name, data in datasets.items():
        axs[2, 1].plot(data.groupby('Year')['Sentiment'].mean(), marker='o', label=name)
    axs[2, 1].set_title('Average Sentiment by Year')
    axs[2, 1].set_xlabel('Year')
    axs[2, 1].set_ylabel('Average Sentiment')
    axs[2, 1].legend()

    plt.tight_layout()
    figures.append(fig1)

    # Visit_Type Count by Continent
    fig2, axs2 = plt.subplots(1, 2, figsize=(14, 6))
    sns.countplot(x='Visit_Type', hue='Continent', data=df_all, ax=axs2[0], palette="Set3")
    axs2[0].set_title('Visit_Type Count by Continent')
    axs2[0].set_xlabel('Visit Type')
    axs2[0].set_ylabel('Count')

    # Visit_Type Count by Branch
    sns.countplot(x='Visit_Type', hue='Branch', data=df_all, ax=axs2[1], palette="Set3")
    axs2[1].set_title('Visit_Type Count by Branch')
    axs2[1].set_xlabel('Visit Type')
    axs2[1].set_ylabel('Count')

    plt.tight_layout()
    figures.append(fig2)

    fig3, axs3 = plt.subplots(2, 2, figsize=(14, 12))
    
    # Average Rating for Visit_Type
    visit_rating = df_all.groupby('Visit_Type')['Rating'].mean()
    axs3[0, 0].bar(visit_rating.index, visit_rating.values, color='skyblue')
    axs3[0, 0].set_title('Average Rating for Visit_Type')
    axs3[0, 0].set_xlabel('Visit Type')
    axs3[0, 0].set_ylabel('Average Rating')

    # Average Sentiment for Visit_Type
    visit_sentiment = df_all.groupby('Visit_Type')['Sentiment'].mean()
    axs3[0, 1].bar(visit_sentiment.index, visit_sentiment.values, color='salmon')
    axs3[0, 1].set_title('Average Sentiment for Visit_Type')
    axs3[0, 1].set_xlabel('Visit Type')
    axs3[0, 1].set_ylabel('Average Sentiment')

    sns.countplot(x='Branch', hue='Continent', data=df_all, ax=axs3[1, 0], palette="Set3")
    axs3[1, 0].set_title('Continent Count by Branch')
    axs3[1, 0].set_xlabel('Branch')
    axs3[1, 0].set_ylabel('Count')

    plt.tight_layout()
    figures.append(fig3)

    for i, fig in enumerate(figures, start=1):
        st.pyplot(fig)

if __name__ == "__main__":
    main()

