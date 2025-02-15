import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load student data from Excel
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

# Custom CSS for future styling
def load_css():
    css_file = "styles.css"  # Change this if you name the CSS file differently
    try:
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # If CSS isn't found, just continue without it

# UI Layout
st.title("📚 Teacher's Dashboard - Student Information")
st.sidebar.header("Filter Options")

# Load CSS
load_css()

# Upload Excel file
uploaded_file = st.sidebar.file_uploader("Upload Student Data (Excel)", type=["xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)

    # Sidebar: Filters
    filter_options = {}
    for col in df.select_dtypes(include=['object', 'category']).columns:
        filter_options[col] = st.sidebar.multiselect(f"Filter by {col}", options=df[col].unique())

    # Apply filters
    for col, values in filter_options.items():
        if values:
            df = df[df[col].isin(values)]

    # Display filtered DataFrame
    st.subheader("📄 Filtered Student Data")
    st.dataframe(df)

    # Dynamic Pie Chart Selection with Default Values
    st.subheader("📊 Generate Pie Chart")
    default_pie_values = [col for col in ["Gender", "Category"] if col in df.columns]
    pie_columns = st.multiselect("Select column(s) for Pie Chart", options=df.columns, default=default_pie_values)

    if pie_columns:
        for col in pie_columns:
            fig = px.pie(df, names=col, title=f"{col} Distribution", hole=0.3)
            fig.update_traces(textinfo='percent+label', textfont_size=12)  # Show numbers on the pie chart
            st.plotly_chart(fig)

    # Heatmap with Default Values
    st.subheader("🔥 Heatmap (Comparison of Two Fields)")
    heatmap_x = st.selectbox("Select X-axis", df.columns, index=df.columns.get_loc("Gender") if "Gender" in df.columns else 0)
    heatmap_y = st.selectbox("Select Y-axis", df.columns, index=df.columns.get_loc("Category") if "Category" in df.columns else 1)

    if heatmap_x and heatmap_y:
        pivot_table = df.pivot_table(index=heatmap_y, columns=heatmap_x, aggfunc="size", fill_value=0)
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns,
            y=pivot_table.index,
            colorscale="Viridis"
        ))
        fig.update_layout(title=f"Heatmap: {heatmap_x} vs {heatmap_y}")
        st.plotly_chart(fig)

else:
    st.warning("Please upload an Excel file to view student details.")