import streamlit as st
import os
import fitz  # PyMuPDF
from pdf2image import convert_from_bytes
import pytesseract
from docx import Document
from io import BytesIO

st.title("PDF Converter App")

# Interface options
conversion_type = st.radio("Select Conversion Type:", ["PDF to Text (Digital)", "Scanned PDF to OCR (Image)"])
output_format = st.selectbox("Select Output Format:", [".txt", ".rtf", ".docx"])

# File selector
uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

if uploaded_file is not None:
    if st.button("Convert and Save"):
        with st.spinner("Converting..."):
            extracted_text = ""

            # 1. Extract Text
            if conversion_type == "Scanned PDF to OCR (Image)":
                images = convert_from_bytes(uploaded_file.read())
                for img in images:
                    extracted_text += pytesseract.image_to_string(img) + "\n"
            else:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page in doc:
                    extracted_text += page.get_text()

            # 2. Prepare download
            base_name = os.path.splitext(uploaded_file.name)[0]

            if output_format == ".txt":
                data = extracted_text.encode("utf-8")
                mime = "text/plain"

            elif output_format == ".rtf":
                rtf_content = "{\\rtf1\\ansi\n" + extracted_text.replace("\n", "\\par\n") + "\n}"
                data = rtf_content.encode("utf-8")
                mime = "application/rtf"

            elif output_format == ".docx":
                buffer = BytesIO()
                word_doc = Document()
                word_doc.add_paragraph(extracted_text)
                word_doc.save(buffer)
                data = buffer.getvalue()
                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

            st.success("Conversion complete! Click below to download.")
            st.download_button(
                label="Download File",
                data=data,
                file_name=f"{base_name}{output_format}",
                mime=mime
            )

st.markdown("---")
st.markdown("<center>App brought to you by <a href='https://www.karloz.art'>www.karloz.art</a></center>", unsafe_allow_html=True)