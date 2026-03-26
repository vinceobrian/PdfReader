import streamlit as st
import pandas as pd
import pdfplumber

# --- Page Config ---
st.set_page_config(page_title="Candidate Shift Dashboard", layout="wide")
st.title("📄 Candidate Shift & Timezone Dashboard")
st.write("Upload a PDF to extract candidate details and preferred shifts.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Expected headers based on your description
EXPECTED_HEADERS = [
    "Name", 
    "Personal Mail Id", 
    "GForm_Please select your local timezone", 
    "GForm_Please Select Preferred Shift in your timezone"
]

if uploaded_file is not None:
    with st.spinner("Extracting data from PDF..."):
        all_data = []
        
        # Read the PDF
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                # Extract tables from each page
                table = page.extract_table()
                if table:
                    # Clean out empty rows
                    cleaned_table = [row for row in table if any(cell for cell in row)]
                    all_data.extend(cleaned_table)

    if all_data:
        # Assume the first row of the first table is the header
        headers = all_data[0]
        
        # Clean up headers (replace newlines that PDFs often create)
        headers = [str(h).replace('\n', ' ').strip() if h else f"Column_{i}" for i, h in enumerate(headers)]
        
        # Create DataFrame from the rest of the data
        df = pd.DataFrame(all_data[1:], columns=headers)
        
        # Drop rows where all elements are missing
        df.dropna(how='all', inplace=True)

        st.success("PDF processed successfully!")

        # --- Dashboard Metrics ---
        st.markdown("### 📊 Quick Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Candidates", len(df))
        
        # Attempt to find the Timezone column dynamically (in case of slight spelling differences)
        tz_col = next((col for col in df.columns if "timezone" in col.lower() and "shift" not in col.lower()), None)
        shift_col = next((col for col in df.columns if "shift" in col.lower()), None)

        if tz_col:
             col2.metric("Unique Timezones", df[tz_col].nunique())
        if shift_col:
             col3.metric("Unique Shifts", df[shift_col].nunique())

        st.divider()

        # --- Interactive Filters ---
        st.markdown("### 🔍 Filter Data")
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

        # --- Data Table ---
        st.markdown("### 📋 Candidate Data")
        st.dataframe(filtered_df, use_container_width=True)
        
        # --- Download Button ---
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name='candidate_shifts.csv',
            mime='text/csv',
        )

    else:
        st.warning("Could not find tabular data in this PDF. If the PDF is just flat text, we may need to use a regex extractor instead.")