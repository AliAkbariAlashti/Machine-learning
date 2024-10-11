# telecom_analysis.py
# Script for analyzing telecom customer churn dataset and visualizing key insights

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('telecom_dataset.csv')

# Display basic dataset information
print("Dataset Information:")
print(df.info())

# Display basic statistics
print("\nDataset Summary:")
print(df.describe())

# 1. Distribution of customers by gender
def plot_gender_distribution():
    gender_counts = df['Gender'].value_counts()
    plt.bar(gender_counts.index, gender_counts.values, color=['blue', 'orange'])
    plt.title('Customer Distribution by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.show()

# 2. Distribution of customers by contract type
def plot_contract_distribution():
    contract_counts = df['Contract'].value_counts()
    plt.bar(contract_counts.index, contract_counts.values, color=['green', 'red', 'purple'])
    plt.title('Customer Distribution by Contract Type')
    plt.xlabel('Contract Type')
    plt.ylabel('Count')
    plt.show()

# 3. Histogram of Monthly Charges
def plot_monthly_charges_histogram():
    plt.hist(df['Monthly Charges'], bins=30, color='skyblue')
    plt.title('Distribution of Monthly Charges')
    plt.xlabel('Monthly Charges')
    plt.ylabel('Frequency')
    plt.show()

# 4. Pie chart for churn distribution
def plot_churn_distribution():
    churn_counts = df['Churn Label'].value_counts()
    plt.pie(churn_counts.values, labels=churn_counts.index, autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightgreen'])
    plt.title('Churn Distribution')
    plt.show()

# 5. Scatter plot of Monthly Charges vs Total Charges
def plot_monthly_vs_total_charges():
    plt.scatter(df['Monthly Charges'], df['Total Charges'], color='purple')
    plt.title('Monthly Charges vs Total Charges')
    plt.xlabel('Monthly Charges')
    plt.ylabel('Total Charges')
    plt.show()

# 6. Bar chart of churn reasons
def plot_churn_reasons():
    churn_reasons_counts = df['Churn Reason'].value_counts()
    plt.bar(churn_reasons_counts.index, churn_reasons_counts.values, color='teal')
    plt.xticks(rotation=90)
    plt.title('Distribution of Churn Reasons')
    plt.xlabel('Reason')
    plt.ylabel('Count')
    plt.show()

# Run analysis and plotting
if __name__ == "__main__":
    print("Running analysis...")

    plot_gender_distribution()
    plot_contract_distribution()
    plot_monthly_charges_histogram()
    plot_churn_distribution()
    plot_monthly_vs_total_charges()
    plot_churn_reasons()

    print("Analysis complete!")
