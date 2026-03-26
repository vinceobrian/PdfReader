import streamlit as st
import pandas as pd
import pdfplumber
import plotly.express as px  # <-- New import for awesome graphs

# --- Page Config ---
st.set_page_config(page_title="Candidate Dashboard", layout="wide")
st.title("📄 Candidate Shift & Timezone Dashboard")
st.write("Upload a PDF to extract candidate details, analyze timezones, and visualize shifts.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting and crunching data..."):
        all_data = []
        
        # Read the PDF
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    cleaned_table = [row for row in table if any(cell for cell in row)]
                    all_data.extend(cleaned_table)

    if all_data:
        # Create DataFrame
        headers = all_data[0]
        headers = [str(h).replace('\n', ' ').strip() if h else f"Column_{i}" for i, h in enumerate(headers)]
        df = pd.DataFrame(all_data[1:], columns=headers)
        df.dropna(how='all', inplace=True)

        # Dynamically find the right columns based on your Google Form headers
        tz_col = next((col for col in df.columns if "timezone" in col.lower() and "shift" not in col.lower()), None)
        shift_col = next((col for col in df.columns if "shift" in col.lower()), None)

        st.success("Data loaded and ready for analysis!")

        # --- Interactive Filters ---
        st.markdown("### 🔍 Filter the Data")
        filter_col1, filter_col2 = st.columns(2)
        
        filtered_df = df.copy()
        
        with filter_col1:
            if tz_col:
                timezones = ["All"] + list(df[tz_col].dropna().unique())
                selected_tz = st.selectbox("Filter by Timezone:", timezones)
                if selected_tz != "All":
                    filtered_df = filtered_df[filtered_df[tz_col] == selected_tz]

        with filter_col2:
            if shift_col:
                shifts = ["All"] + list(filtered_df[shift_col].dropna().unique())
                selected_shift = st.selectbox("Filter by Preferred Shift:", shifts)
                if selected_shift != "All":
                    filtered_df = filtered_df[filtered_df[shift_col] == selected_shift]


        # --- 📈 DATA ANALYSIS & GRAPHS ---
        st.markdown("### 📈 Analytics Overview")
        st.write("*(Note: The graphs update automatically based on the filters you set above!)*")
        
        if tz_col and shift_col:
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # 1. Bar Chart: Candidates per Timezone
                tz_counts = filtered_df[tz_col].value_counts().reset_index()
                tz_counts.columns = ['Timezone', 'Number of Candidates']
                fig_tz = px.bar(
                    tz_counts, x='Timezone', y='Number of Candidates', 
                    title="Headcount by Timezone",
                    color='Timezone',
                    text_auto=True # Shows the exact number on the bars
                )
                st.plotly_chart(fig_tz, use_container_width=True)
                
            with chart_col2:
                # 2. Donut Chart: Shift Distribution
                shift_counts = filtered_df[shift_col].value_counts().reset_index()
                shift_counts.columns = ['Shift', 'Count']
                fig_shift = px.pie(
                    shift_counts, names='Shift', values='Count', 
                    title="Distribution of Preferred Shifts",
                    hole=0.4 # Makes it a modern donut chart instead of a standard pie chart
                )
                fig_shift.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_shift, use_container_width=True)

        st.divider()

        # --- Data Table & Export ---
        st.markdown("### 📋 Raw Candidate Data")
        st.dataframe(filtered_df, use_container_width=True)
        
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Filtered CSV", data=csv, file_name='analyzed_candidates.csv', mime='text/csv')

    else:
        st.error("Could not find standard table structures. We might need to write a custom text-extractor for this specific PDF.")