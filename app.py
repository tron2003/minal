import streamlit as st
import pdfplumber
import pandas as pd
import io

# Set Streamlit page config
st.set_page_config(page_title="Bank Statement Converter", page_icon="📄")

# App Title
st.title("Bank Statement PDF to Excel Converter")

# Short description
st.write("Easily convert your bank statement PDFs to Excel format. Just upload a PDF, and we'll extract the data for you!")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.success("File uploaded successfully!")
    extracted_text = []

    with st.spinner("Extracting text from PDF..."):
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.extend(text.split("\n"))

    if extracted_text:
        df = pd.DataFrame({"Extracted Text": extracted_text})

        # Display extracted data
        st.subheader("Extracted Data")
        st.dataframe(df)

        # Convert DataFrame to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Bank Statement", index=False)
        output.seek(0)

        # Download button with color on click
        st.markdown(
            """
            <style>
                .stDownloadButton>button {
                    background-color: #007BFF;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }
                .stDownloadButton>button:active {
                    background-color: #0056b3;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.download_button(
            label="Download Excel File",
            data=output,
            file_name="bank_statement.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.error(
            "No text extracted from the PDF. Ensure the document is not an image-based scan.")
