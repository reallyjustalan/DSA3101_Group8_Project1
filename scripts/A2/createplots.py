import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def create_plots(df_all, df_hongkong, df_california, df_paris):
    fig, axs = plt.subplots(3, 2, figsize=(14, 15))

    datasets = {
        "All Data": df_all,
        "Hong Kong": df_hongkong,
        "California": df_california,
        "Paris": df_paris
    }

    # Plot: Average Rating by Continent
    for name, data in datasets.items():
        axs[0, 0].plot(data.groupby('Continent')['Rating'].mean(), marker='o', label=name)
    axs[0, 0].set_title('Average Rating by Continent')
    axs[0, 0].set_xlabel('Continent')
    axs[0, 0].set_ylabel('Average Rating')
    axs[0, 0].legend()

    # Plot: Average Sentiment by Continent
    for name, data in datasets.items():
        axs[0, 1].plot(data.groupby('Continent')['Sentiment'].mean(), marker='o', label=name)
    axs[0, 1].set_title('Average Sentiment by Continent')
    axs[0, 1].set_xlabel('Continent')
    axs[0, 1].set_ylabel('Average Sentiment')
    axs[0, 1].legend()

    # Plot: Average Rating by Month
    for name, data in datasets.items():
        axs[1, 0].plot(data.groupby('Month')['Rating'].mean(), marker='o', label=name)
    axs[1, 0].set_title('Average Rating by Month')
    axs[1, 0].set_xlabel('Month')
    axs[1, 0].set_ylabel('Average Rating')
    axs[1, 0].legend()

    # Plot: Average Sentiment by Month
    for name, data in datasets.items():
        axs[1, 1].plot(data.groupby('Month')['Sentiment'].mean(), marker='o', label=name)
    axs[1, 1].set_title('Average Sentiment by Month')
    axs[1, 1].set_xlabel('Month')
    axs[1, 1].set_ylabel('Average Sentiment')
    axs[1, 1].legend()

    # Plot: Average Rating by Year
    for name, data in datasets.items():
        axs[2, 0].plot(data.groupby('Year')['Rating'].mean(), marker='o', label=name)
    axs[2, 0].set_title('Average Rating by Year')
    axs[2, 0].set_xlabel('Year')
    axs[2, 0].set_ylabel('Average Rating')
    axs[2, 0].legend()

    # Plot: Average Sentiment by Year
    for name, data in datasets.items():
        axs[2, 1].plot(data.groupby('Year')['Sentiment'].mean(), marker='o', label=name)
    axs[2, 1].set_title('Average Sentiment by Year')
    axs[2, 1].set_xlabel('Year')
    axs[2, 1].set_ylabel('Average Sentiment')
    axs[2, 1].legend()

    plt.tight_layout()
    plt.show()

    # Second figure: Count Plots
    fig2, axs2 = plt.subplots(1, 2, figsize=(14, 6))
    sns.countplot(x='Visit_Type', hue='Continent', data=df_all, ax=axs2[0], palette="Set3")
    axs2[0].set_title('Visit_Type Count by Continent')
    axs2[0].set_xlabel('Visit Type')
    axs2[0].set_ylabel('Count')

    sns.countplot(x='Visit_Type', hue='Branch', data=df_all, ax=axs2[1], palette="Set3")
    axs2[1].set_title('Visit_Type Count by Branch')
    axs2[1].set_xlabel('Visit Type')
    axs2[1].set_ylabel('Count')

    plt.tight_layout()
    plt.show()

    # Third figure: Bar Plots and Count Plot
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

    # Continent Count by Branch
    sns.countplot(x='Branch', hue='Continent', data=df_all, ax=axs3[1, 0], palette="Set3")
    axs3[1, 0].set_title('Continent Count by Branch')
    axs3[1, 0].set_xlabel('Branch')
    axs3[1, 0].set_ylabel('Count')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    pass