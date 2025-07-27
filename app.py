# app.py
import streamlit as st
import os
from legal_assistant import generate_document, save_to_pdf
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="⚖️ LexiMate", layout="centered")

st.title("⚖️ LexiMate")
st.write("Generate professional legal documents with LexiMate AI.")

doc_type = st.selectbox(
    "Choose document type",
    [
        "Rental Agreement", "Employment Contract", "Business Partnership Agreement", "NDA",
        "MOU", "Contractor Agreement", "Loan Agreement", "SLA"
    ]
)

party1 = st.text_input("Party 1 Name")
party2 = st.text_input("Party 2 Name")

# Conditional fields
duration = st.text_input("Duration (months)", placeholder="e.g., 12") if "rental" in doc_type.lower() else ""
salary = st.text_input("Salary (per year)") if "employment" in doc_type.lower() else ""

generate_btn = st.button("Generate Document")

if generate_btn:
    if party1 and party2:
        with st.spinner("Generating legal document..."):
            output = generate_document(doc_type, party1, party2, duration, salary)

        if output and not output.startswith("Error"):
            st.text_area("Generated Legal Document", output, height=400)

            with st.spinner("Creating PDF..."):
                pdf_file = save_to_pdf(output)

            if os.path.exists(pdf_file):
                with open(pdf_file, "rb") as f:
                    st.download_button("📄 Download PDF", f, file_name="legal_document.pdf", mime="application/pdf")
            else:
                st.error(f"Failed to generate PDF: {pdf_file}")
        else:
            st.error(output)
    else:
        st.warning("Please enter both Party 1 and Party 2 names.")
