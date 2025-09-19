import streamlit as st
import pandas as pd
import json

st.title("JSON to Dashboard")

# User can paste JSON or upload a file
st.subheader("Input JSON")
json_input = st.text_area("Paste your JSON here", height=200)
uploaded_file = st.file_uploader("Or upload a JSON file", type=["json"])

data = None

if uploaded_file:
    try:
        data = json.load(uploaded_file)
    except Exception as e:
        st.error(f"Failed to load JSON: {e}")
elif json_input:
    try:
        data = json.loads(json_input)
    except Exception as e:
        st.error(f"Failed to parse JSON: {e}")

if data is not None:
    st.subheader("Raw JSON Preview")
    st.json(data)

    # Try to flatten and convert to tabular if possible
    def json_to_dataframe(data):
        # If it's a list of dicts, treat as DataFrame
        if isinstance(data, list) and all(isinstance(i, dict) for i in data):
            return pd.DataFrame(data)
        # If it's a dict of lists, treat as DataFrame
        if isinstance(data, dict) and all(isinstance(i, list) for i in data.values()):
            return pd.DataFrame(data)
        # Try flattening one level
        if isinstance(data, dict):
            return pd.DataFrame([data])
        # Otherwise, return None
        return None

    df = json_to_dataframe(data)
    if df is not None and not df.empty:
        st.subheader("Tabular View")
        st.dataframe(df)

        # Show basic charts if numeric data is present
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            st.subheader("Quick Charts")
            col = st.selectbox("Select column to plot", numeric_cols)
            st.line_chart(df[col])
    else:
        st.info("No tabular data detected to display as a table