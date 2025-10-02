# Customer Segmentation using RFM Analysis & K-Means Clustering

###  [View the Interactive Power BI Dashboard](https://nittemeenaksh-my.sharepoint.com/:u:/g/personal/1nt22ai007_aryan_nmit_ac_in/EYWTfyX6Ms5DltqwjPwdo0cBqg6Txo0JVTrNmkIBGxNRZg) ## Project Overview

This project performs customer segmentation for an online retail business by leveraging RFM (Recency, Frequency, Monetary) analysis and K-Means clustering. The goal is to identify distinct customer groups to enable targeted and effective marketing strategies, ultimately enhancing customer relationship management and driving business growth. The entire analysis is presented in an interactive Power BI dashboard.

## 🚀 Problem Statement

In a competitive retail market, understanding customer behavior is key to success. A one-size-fits-all marketing approach is often inefficient and costly. This project aims to answer the question:

*How can we segment customers into meaningful groups based on their purchasing behavior to tailor marketing and sales strategies for each group?*

---

## 💾 Dataset

The dataset used is the **Online Retail Data Set** from the UCI Machine Learning Repository. It contains transactional data for a UK-based online retail company from 01/12/2010 to 09/12/2011.

* **Source**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/online+retail)
* **Size**: 541,909 records
* **Attributes**: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`.

---

## 🔧 Methodology

The project follows a structured data analysis workflow:

#### 1. Data Cleaning and Preprocessing
* Loaded the dataset from an Excel file.
* Handled missing values, particularly `CustomerID`.
* Removed transactional records with negative `Quantity`, as these represent returns.
* Ensured correct data types for columns like `InvoiceDate` and `CustomerID`.

#### 2. RFM Feature Engineering
Calculated the three key RFM metrics for each customer:
* **Recency (R)**: Days since the customer's last transaction.
* **Frequency (F)**: Total number of unique transactions made by the customer.
* **Monetary (M)**: Total amount spent by the customer.

#### 3. RFM Scoring and Segmentation
* Assigned scores from 1 to 4 to each RFM metric using quantiles.
* Defined descriptive customer segments (e.g., `Champions`, `Loyal Customers`, `At Risk`) based on these scores to provide actionable business insights.

#### 4. K-Means Clustering
* Applied the K-Means clustering algorithm to the scaled RFM values to identify natural groupings within the customer base.
* Used the **Elbow Method** to determine the optimal number of clusters for the dataset, which was found to be 4.

#### 5. Data Visualization
* The final segmented and clustered data was exported to a CSV file.
* An interactive dashboard was built in **Power BI** to visualize the customer segments, their monetary value, and their distribution, providing a comprehensive tool for business analysis.

---

## 🛠️ Tools and Technologies

* **Programming Language**: Python 3
* **Libraries**: Pandas, NumPy, Scikit-learn (for KMeans & StandardScaler), Matplotlib
* **BI Tool**: Microsoft Power BI
* **Environment**: Jupyter Notebook / VS Code

---

## ⚙️ How to Run This Project

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    ```
2.  **Install the required libraries:**
    ```sh
    pip install pandas numpy scikit-learn matplotlib openpyxl
    ```
3.  **Add the dataset:**
    Download the `Online Retail.xlsx` file and place it in the project's root directory.

4.  **Run the script:**
    ```sh
    python your_script_name.py
    ```
5.  **Output:**
    The script will generate a file named `customer_segmentation_output.csv`, which contains the final data ready for use in Power BI.

---

## 🎯 Key Insights from the Dashboard

The segmentation revealed several key customer groups, enabling targeted actions:

* **Champions**: Our best customers who buy frequently and have spent the most. They should be rewarded with loyalty programs and exclusive offers.
* **At Risk**: Customers who used to be valuable but have not purchased in a long time. They need to be re-engaged with personalized reactivation campaigns.
* **Potential Loyalists**: Recent customers with a good frequency or monetary value. They can be nurtured into 'Champions' with targeted product recommendations and engagement.
* **New Customers**: Customers who have made very few recent purchases. They need a smooth onboarding experience and introductory offers to encourage repeat business.

This project successfully transforms raw transactional data into a powerful strategic asset for the marketing and sales teams.
