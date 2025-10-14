import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def generate_segments(df):
    """
    Takes a raw dataframe from the 'Online Retail' dataset and performs
    RFM analysis, segmentation, and clustering.
    """
    # --- 1. Data Cleaning ---
    df.dropna(subset=['CustomerID'], inplace=True)
    df['CustomerID'] = df['CustomerID'].astype(int)
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0] # Added to avoid zero unit price issues
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # --- 2. Derive RFM Columns ---
    df['Monetary'] = df['Quantity'] * df['UnitPrice']
    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    
    rfm_df = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda date: (snapshot_date - date.max()).days,
        'InvoiceNo': 'nunique',
        'Monetary': 'sum'
    })
    rfm_df.rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'Monetary': 'Monetary'}, inplace=True)

    # --- 3. Calculate RFM Scores and Segments ---
    r_labels = range(4, 0, -1)
    f_labels = range(1, 5)
    m_labels = range(1, 5)

    rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], q=4, labels=r_labels, duplicates='drop').astype(int)
    rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), q=4, labels=f_labels).astype(int)
    rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], q=4, labels=m_labels, duplicates='drop').astype(int)
    
    def assign_segment(df_row):
        if df_row['R_Score'] >= 3 and df_row['F_Score'] >= 3:
            return 'Champions'
        elif df_row['R_Score'] >= 3 and df_row['F_Score'] < 3:
            return 'Potential Loyalists'
        elif df_row['R_Score'] < 3 and df_row['F_Score'] >= 3:
            return 'Loyal Customers'
        elif df_row['R_Score'] == 2 and df_row['F_Score'] == 2:
            return 'Needs Attention'
        elif df_row['R_Score'] < 2 and df_row['F_Score'] < 2:
            return 'At Risk'
        else:
            return 'Other'
            
    rfm_df['Segment'] = rfm_df.apply(assign_segment, axis=1)

    # --- 4. Apply Clustering ---
    rfm_for_clustering = rfm_df[['Recency', 'Frequency', 'Monetary']]
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_for_clustering)
    
    kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42, n_init=10)
    rfm_df['Cluster'] = kmeans.fit_predict(rfm_scaled)
    rfm_df['Cluster'] = rfm_df['Cluster'].astype(str)

    rfm_df.reset_index(inplace=True)
    return rfm_df
