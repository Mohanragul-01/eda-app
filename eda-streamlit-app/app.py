import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Page configuration
st.set_page_config(page_title='EDA Application',
                   layout='centered',
                   page_icon='📊')


# Custom CSS for the sidebar and overall app styling
st.markdown("""
    <style>
    footer, header, .css-1outpf7, .css-1pjkge8 {
        visibility: hidden;
    }
    .main .block-container {
        padding: 10px 50px;
        margin: 30px;
        max-width: 100%;
    }       
    .stAlert {
        width: auto;
        max-width: 65%;
        # margin: auto;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    }
    .st-emotion-cache-16txtl3  {
        padding: 4.5rem 1.5rem;
    }
    .st-emotion-cache-1v0mbdj {
        width: 75%;
        padding: 0rem 4rem;
    }
    .st-emotion-cache-1v0mbdj img {
        max-width: 100%;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


# Title of the application
st.title("📊 Exploratory Data Analysis Application")


# Upload the dataset
st.sidebar.header("Upload your CSV file")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])


if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    
    # Show the dataframe
    st.header("Dataset")
    if st.checkbox("Show Dataset"):
        st.write(data)
    
    # Analysis options
    st.sidebar.header("Analysis Options")
    analysis_option = st.sidebar.selectbox("Select Analysis Process", ["Basic Statistics", "Data Types", "Missing Values", "Unique Values in Categorical Columns", "Correlation Matrix", 
                                                                      "Outlier Detection", "Value Counts", "Custom Analysis", "Data Distribution"])
    
    # Perform analysis based on selected option
    st.header("Analysis Results")
    
    # Basic statistics
    if analysis_option == "Basic Statistics":
        st.subheader("Basic Statistics")
        st.write(data.describe())
    
    # Data types
    elif analysis_option == "Data Types":
        st.subheader("Data Types")
        st.write(data.dtypes)
    
    # Missing values
    elif analysis_option == "Missing Values":
        st.subheader("Missing Values")
        missing_values = data.isnull().sum()
        st.write(missing_values[missing_values > 0])
    
    # Unique values in categorical columns
    elif analysis_option == "Unique Values in Categorical Columns":
        st.subheader("Unique Values in Categorical Columns")
        cat_columns = data.select_dtypes(include=['object']).columns.tolist()
        for col in cat_columns:
            st.write(f"**{col}**: {data[col].nunique()} unique values")
    
    # Correlation matrix
    elif analysis_option == "Correlation Matrix":
        st.subheader("Correlation Matrix")
        corr_matrix = data.select_dtypes(include=['float64', 'int64']).corr()
        st.write(corr_matrix)
        # Show correlation heatmap
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    
    # Outlier detection
    elif analysis_option == "Outlier Detection":
        st.subheader("Outlier Detection")
        selected_num_column_outliers = st.selectbox("Select a numerical column for Outlier Detection", data.select_dtypes(include=['float64', 'int64']).columns.tolist())
        st.write(data[selected_num_column_outliers])
        column_data = data[selected_num_column_outliers]
        z_scores = (column_data - column_data.mean()) / column_data.std()
        threshold = 3
        outliers = np.abs(z_scores) > threshold
        st.subheader("Outliers Detected using Z-score")
        st.write(data[outliers])

    # Value counts
    elif analysis_option == "Value Counts":
        st.subheader("Value Counts")
        selected_column_value_counts = st.selectbox("Select a column for Value Counts", data.columns.tolist())
        st.write(data[selected_column_value_counts].value_counts())
   
    # Custom analysis
    elif analysis_option == "Custom Analysis":
        st.subheader("Custom Analysis")
        custom_analysis_text = st.text_area("Enter your custom analysis code here", height=100)
        if st.button("Run Custom Analysis"):
            if custom_analysis_text:
                try:
                    exec(custom_analysis_text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter your custom analysis code")
# ========== Example code ===========
# selected_column = 'total_bill' 
# mean_value = data[selected_column].mean()
# median_value = data[selected_column].median()
# std_dev = data[selected_column].std()

# st.write("Mean:", mean_value)
# st.write("Median:", median_value)
# st.write("Standard Deviation:", std_dev)
# =================================

    # Data distribution
    elif analysis_option == "Data Distribution":
        st.subheader("Data Distribution")
        selected_columns_data_distribution = st.multiselect("Select columns for Data Distribution", data.columns.tolist())
        if selected_columns_data_distribution:
            for col in selected_columns_data_distribution:
                st.subheader(f"Data Distribution for {col}")
                st.write(data[col].describe())
                fig, ax = plt.subplots()
                sns.histplot(data[col], kde=True, ax=ax)
                st.pyplot(fig)


    # Visualization options
    st.sidebar.header("Visualization Options")
    visualization_option = st.sidebar.selectbox("Select a visualization type", ["Histogram", "Bar Plot", "Pairplot", "Scatter Plot", "Line Plot", 
                                                                                "Box Plot", "Pie Chart", "Count Plot", "Violin Plot"])

    # Histogram
    if visualization_option == "Histogram":
        st.subheader("Histogram")
        selected_num_column_hist = st.sidebar.selectbox("Select a numerical column for Histogram", data.select_dtypes(include=['float64', 'int64']).columns.tolist())
        fig, ax = plt.subplots()
        data[selected_num_column_hist].hist(bins=30, ax=ax)
        st.pyplot(fig)
    
    # Bar Plot
    elif visualization_option == "Bar Plot":
        st.subheader("Bar Plot")
        selected_cat_column_bar = st.sidebar.selectbox("Select a categorical column for Bar Plot", data.select_dtypes(include=['object']).columns.tolist())
        fig, ax = plt.subplots()
        data[selected_cat_column_bar].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)
    
    # Pairplot
    elif visualization_option == "Pairplot":
        st.subheader("Pairplot for Numerical Columns")
        selected_num_columns_pairplot = st.sidebar.multiselect("Select numerical columns for Pairplot", data.select_dtypes(include=['float64', 'int64']).columns.tolist())
        if selected_num_columns_pairplot:
            fig = sns.pairplot(data[selected_num_columns_pairplot])
            st.pyplot(fig)
    
    # Scatter plot
    elif visualization_option == "Scatter Plot":
        st.subheader("Scatter Plot")
        x_column_scatter = st.sidebar.selectbox("Select X-axis data for Scatter Plot", data.select_dtypes(include=['float64', 'int64']).columns.tolist())
        y_column_scatter = st.sidebar.selectbox("Select Y-axis data for Scatter Plot", data.select_dtypes(include=['float64', 'int64']).columns.tolist())
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x=x_column_scatter, y=y_column_scatter, ax=ax)
        st.pyplot(fig)
    
    # Line plot
    elif visualization_option == "Line Plot":
        st.subheader("Line Plot")
        x_column_line = st.sidebar.selectbox("Select X-axis data for Line Plot", data.select_dtypes(include=['float64', 'int64']).columns.tolist())
        y_column_line = st.sidebar.selectbox("Select Y-axis data for Line Plot", data.select_dtypes(include=['float64', 'int64']).columns.tolist())
        fig, ax = plt.subplots()
        sns.lineplot(data=data, x=x_column_line, y=y_column_line, ax=ax)
        st.pyplot(fig)
    
    # Box plot
    elif visualization_option == "Box Plot":
        st.subheader("Box Plot")
        selected_column_box = st.sidebar.selectbox("Select a column for Box Plot", data.select_dtypes(include=['float64', 'int64']).columns.tolist())
        fig, ax = plt.subplots()
        sns.boxplot(data=data[selected_column_box], ax=ax)
        st.pyplot(fig)
   
    # Pie chart
    elif visualization_option == "Pie Chart":
        st.subheader("Pie Chart")
        selected_column_pie = st.sidebar.selectbox("Select a column for Pie Chart", data.select_dtypes(include=['object']).columns.tolist())
        pie_data = data[selected_column_pie].value_counts()
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
    
    # Count plot
    elif visualization_option == "Count Plot":
        st.subheader("Count Plot")
        selected_column_count = st.sidebar.selectbox("Select a column for Count Plot", data.select_dtypes(include=['object']).columns.tolist())
        fig, ax = plt.subplots()
        sns.countplot(data=data, x=selected_column_count, ax=ax)
        st.pyplot(fig)
    
    # Violin plot
    elif visualization_option == "Violin Plot":
        st.subheader("Violin Plot")
        x_column_violin = st.sidebar.selectbox("Select X-axis data for Violin Plot", data.select_dtypes(include=['object']).columns.tolist())
        y_column_violin = st.sidebar.selectbox("Select Y-axis data for Violin Plot", data.select_dtypes(include=['float64', 'int64']).columns.tolist())
        fig, ax = plt.subplots()
        sns.violinplot(data=data, x=x_column_violin, y=y_column_violin, ax=ax)
        st.pyplot(fig)

else:
    st.info("Awaiting for CSV file to be uploaded.")
