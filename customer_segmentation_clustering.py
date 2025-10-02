import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# --- 1. Load and Clean the Dataset ---
try:
    df = pd.read_excel('Online Retail.xlsx', sheet_name='Online Retail')
    df.to_csv('Online Retail.csv', index=False)
except FileNotFoundError:
    print("Error: 'Online Retail.xlsx - Online Retail.csv' not found.")
    #Dummy dataframe if file not found
    df = pd.DataFrame()

if not df.empty:
    print("Dataset loaded successfully.")
    # Drop rows with missing CustomerID
    df.dropna(subset=['CustomerID'], inplace=True)

    # Convert CustomerID to integer type
    df['CustomerID'] = df['CustomerID'].astype(int)

    # Remove returns (invoices starting with 'C') and negative quantities
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[df['Quantity'] > 0]
    
    # Convert InvoiceDate to datetime objects
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    print("Data cleaning complete.")

    # --- 2. Derive RFM Columns ---
    print("Calculating RFM values...")
    # Calculate Monetary value for each transaction
    df['Monetary'] = df['Quantity'] * df['UnitPrice']

    # Set a snapshot date (one day after the last transaction) for recency calculation
    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)

    # Group data by customer to calculate Recency, Frequency, and Monetary values
    rfm_df = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda date: (snapshot_date - date.max()).days,
        'InvoiceNo': 'nunique',
        'Monetary': 'sum'
    })

    # Rename the columns for clarity
    rfm_df.rename(columns={'InvoiceDate': 'Recency',
                           'InvoiceNo': 'Frequency',
                           'Monetary': 'Monetary'}, inplace=True)

    print("RFM calculation complete.")

    # --- 3. Calculate RFM Scores and Segments ---
    print("Assigning RFM scores and segments.")
    # Create labels and assign scores for Recency, Frequency, and Monetary
    r_labels = range(4, 0, -1) # Lower recency is better (higher score)
    f_labels = range(1, 5)
    m_labels = range(1, 5)

    rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], q=4, labels=r_labels, duplicates='drop').astype(int)
    rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), q=4, labels=f_labels).astype(int)
    rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], q=4, labels=m_labels, duplicates='drop').astype(int)

    # Combine scores to create a single RFM_Score
    rfm_df['RFM_Score'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)

    # Define segment names based on R and F scores
    def assign_segment(df):
        if df['R_Score'] >= 3 and df['F_Score'] >= 3:
            return 'Champions'
        elif df['R_Score'] >= 3 and df['F_Score'] < 3:
            return 'Potential Loyalists'
        elif df['R_Score'] < 3 and df['F_Score'] >= 3:
            return 'Loyal Customers'
        elif df['R_Score'] == 2 and df['F_Score'] == 2:
            return 'Needs Attention'
        elif df['R_Score'] < 2 and df['F_Score'] < 2:
            return 'At Risk'
        else:
            return 'Other'

    rfm_df['Segment'] = rfm_df.apply(assign_segment, axis=1)
    print("Segmentation complete.")

    # --- 4. Apply Clustering ---
    print("Applying K-Means clustering.")
    # Prepare data for clustering by scaling
    rfm_for_clustering = rfm_df[['Recency', 'Frequency', 'Monetary']]
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_for_clustering)

    # Use the Elbow Method to find the optimal number of clusters
    inertia = {}
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, random_state=42, n_init=10)
        kmeans.fit(rfm_scaled)
        inertia[k] = kmeans.inertia_

    # Plotting the Elbow Method graph (optional, for verification)
    plt.figure(figsize=(8, 5))
    plt.plot(list(inertia.keys()), list(inertia.values()), 'o-')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method For Optimal k')
    # plt.show() # Uncomment to display the plot

    # Based on the elbow method, let's choose 4 clusters
    optimal_k = 4
    kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42, n_init=10)
    rfm_df['Cluster'] = kmeans.fit_predict(rfm_scaled)

    print(f"K-Means clustering complete. Customers grouped into {optimal_k} clusters.")
    
    # --- 5. Generate Output File for Power BI ---
    # Reset index to turn CustomerID from index to column
    rfm_df.reset_index(inplace=True)
    
    # Save the final dataframe to a CSV file
    output_filename = 'customer_segmentation_output.csv'
    rfm_df.to_csv(output_filename, index=False)

    print(f"Successful! The segmented customer data has been saved to '{output_filename}'.")
    print("This file contains the original RFM values, scores, segments, and cluster labels needed for your Power BI dashboard.")

else:
    print("Execution skipped as the initial dataset could not be loaded.")
