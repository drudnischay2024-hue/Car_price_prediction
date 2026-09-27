import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data(filepath):
    return pd.read_csv(filepath)

def plot_price_distribution(df, save_dir):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Price'], bins=20, kde=True, color='blue')
    plt.title('Distribution of Car Prices')
    plt.xlabel('Price ($1000s)')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(save_dir, 'price_distribution.png'))
    plt.close()

def plot_price_vs_feature(df, feature, save_dir):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=feature, y='Price')
    plt.title(f'Price vs {feature}')
    plt.xlabel(feature)
    plt.ylabel('Price ($1000s)')
    plt.savefig(os.path.join(save_dir, f'price_vs_{feature.lower()}.png'))
    plt.close()

def plot_price_vs_category(df, category, save_dir):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x=category, y='Price')
    plt.title(f'Price vs {category}')
    plt.xlabel(category)
    plt.ylabel('Price ($1000s)')
    plt.savefig(os.path.join(save_dir, f'price_vs_{category.lower()}.png'))
    plt.close()

def plot_correlation(df, save_dir):
    plt.figure(figsize=(12, 10))
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'correlation_matrix.png'))
    plt.close()

def main():
    print("Running EDA...")
    df = load_data('data/car_data.csv')
    save_dir = 'reports/eda_plots'
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Price Distribution
    plot_price_distribution(df, save_dir)
    
    # 2. Price vs Numerical Features (e.g. Horsepower, MPG.city)
    plot_price_vs_feature(df, 'Horsepower', save_dir)
    plot_price_vs_feature(df, 'MPG.city', save_dir)
    
    # 3. Price vs Categorical Features (e.g. Type, Origin)
    plot_price_vs_category(df, 'Type', save_dir)
    plot_price_vs_category(df, 'Origin', save_dir)
    
    # 4. Correlation Analysis
    plot_correlation(df, save_dir)
    
    print(f"EDA completed. Plots saved to {save_dir}")

if __name__ == "__main__":
    main()
