import streamlit as st
import pandas as pd
import plotly.express as px
from customer_segmentation_clustering import generate_segments

# --- Page Configuration ---
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Data Loading Functions ---
@st.cache_data
def load_data_from_upload(uploaded_file):
    """Loads data from the uploaded Excel file."""
    try:
        df = pd.read_excel(uploaded_file, sheet_name='Online Retail')
        return df
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
        return None

@st.cache_data
def load_sample_data(file_path):
    """Loads sample data from a local CSV file within the repository."""
    try:
        # This dataset is known to have encoding issues.
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        # Ensure the InvoiceDate is in the correct format
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        return df
    except FileNotFoundError:
        st.error(f"Sample data file '{file_path}' not found. Make sure it is in your GitHub repository.")
        return None
    except Exception as e:
        st.error(f"Error reading the sample data file: {e}")
        return None

# --- Sidebar ---
with st.sidebar:
    st.title("📊 Customer Segmentation")
    st.markdown("Upload your 'Online Retail' dataset to generate the dashboard.")
    
    uploaded_file = st.file_uploader(
        "Choose an XLSX file", 
        type="xlsx",
        help="Please upload the 'Online Retail.xlsx' file."
    )
    
    st.markdown("<p style='text-align: center;'>OR</p>", unsafe_allow_html=True)
    
    use_sample_data = st.button("Load Sample Dataset")

# --- Main Dashboard ---
st.title("RFM Analysis and Customer Segmentation")

SAMPLE_DATA_FILE = 'Online Retail.xlsx - Online Retail.csv'

df_to_process = None

# Logic to decide which data to load
if use_sample_data:
    df_to_process = load_sample_data(SAMPLE_DATA_FILE)
elif uploaded_file is not None:
    df_to_process = load_data_from_upload(uploaded_file)

# Process and display the dashboard if data is loaded
if df_to_process is not None:
    with st.spinner('Processing your data... This may take a moment.'):
        rfm_data = generate_segments(df_to_process.copy())

    if rfm_data is not None:
        st.success("Data processed successfully! Here's your dashboard.")

        # --- KPI Cards ---
        st.header("Overall Customer Insights")
        total_customers = rfm_data['CustomerID'].nunique()
        avg_recency = rfm_data['Recency'].mean()
        total_monetary = rfm_data['Monetary'].sum()

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Total Customers", value=f"{total_customers:,}")
        kpi2.metric(label="Average Recency (Days)", value=f"{avg_recency:.2f}")
        kpi3.metric(label="Total Monetary Value", value=f"${total_monetary:,.2f}")

        st.markdown("---")

        # --- Visualizations ---
        col1, col2 = st.columns((2, 3))

        with col1:
            st.subheader("Customers by Segment")
            segment_counts = rfm_data['Segment'].value_counts().reset_index()
            segment_counts.columns = ['Segment', 'Count']
            fig_bar = px.bar(segment_counts, x='Count', y='Segment', orientation='h', text='Count', color='Segment', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_bar.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)

            st.subheader("Monetary Value by Segment")
            segment_monetary = rfm_data.groupby('Segment')['Monetary'].sum().reset_index()
            fig_donut = px.pie(segment_monetary, values='Monetary', names='Segment', hole=0.4, color='Segment', color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_donut, use_container_width=True)

        with col2:
            st.subheader("RFM Bubble Chart")
            rfm_agg = rfm_data.groupby('Segment').agg(Recency=('Recency', 'mean'), Frequency=('Frequency', 'mean'), Monetary=('Monetary', 'sum'), CustomerID=('CustomerID', 'count')).reset_index()
            fig_scatter = px.scatter(rfm_agg, x="Recency", y="Frequency", size="Monetary", color="Segment", hover_name="Segment", size_max=60, log_x=True, title="Segment Analysis")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.subheader("Customers by Cluster")
            cluster_counts = rfm_data['Cluster'].value_counts().reset_index()
            cluster_counts.columns = ['Cluster', 'Count']
            fig_cluster_bar = px.bar(cluster_counts, x='Cluster', y='Count', text='Count', color='Cluster', title="Customer Distribution Across Clusters")
            st.plotly_chart(fig_cluster_bar, use_container_width=True)

        st.markdown("---")

        st.subheader("Detailed Segment Data")
        segment_summary = rfm_data.groupby('Segment').agg(Count=('CustomerID', 'count'), Sum_of_Frequency=('Frequency', 'sum'), Sum_of_Monetary=('Monetary', 'sum'), Sum_of_Recency=('Recency', 'sum')).reset_index()
        st.dataframe(segment_summary, use_container_width=True)
    else:
        st.error("Could not process the data. Please check the file format.")
else:
    st.info("Upload your 'Online Retail.xlsx' file, or click 'Load Sample Dataset' in the sidebar to begin.")

