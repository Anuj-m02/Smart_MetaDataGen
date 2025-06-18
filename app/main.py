import sys
import os
import streamlit as st
import json
import re 

# ✅ Add backend directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.extractor import extract_text
from backend.ocr import extract_text_from_image
from backend.metadata_gen import generate_metadata  # uses OpenRouter API inside

# ✅ Set page config
st.set_page_config(page_title="SmartMeta: AI Metadata Generator", layout="wide")
st.title("📄 SmartMeta: Automated Metadata Generation using GenAI")

# ✅ File uploader
uploaded_file = st.file_uploader(
    "Upload a document (PDF, DOCX, TXT, PNG, JPG)", 
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"]
)

if uploaded_file:
    st.success("✅ File uploaded!")

    # ✅ Save to temporary folder
    os.makedirs("app/temp", exist_ok=True)
    file_path = os.path.join("app/temp", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ✅ Extract text from file
    if uploaded_file.type.startswith("image/"):
        text = extract_text_from_image(file_path)
    else:
        text = extract_text(file_path)

    # ✅ Show extracted text preview
    st.subheader("📜 Extracted Text")
    st.text_area("Preview", value=text[:2000], height=300)

    # ✅ Button to generate metadata
    import re

# ✅ Button to generate metadata
    import re

    if st.button("🔍 Generate Metadata"):
        with st.spinner("Analyzing with GenAI..."):
            raw_output = generate_metadata(text)

        try:
            # ✅ Extract JSON block from anywhere in the response using regex
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_output, re.DOTALL)
            if not match:
                # fallback if triple backticks not used — try to extract bare JSON
                match = re.search(r"(\{.*\})", raw_output, re.DOTALL)

            if match:
                cleaned_json = match.group(1)
                metadata = json.loads(cleaned_json)
                st.subheader("📊 Generated Metadata")
                st.json(metadata)

                # ✅ Download button
                json_bytes = json.dumps(metadata, indent=4).encode('utf-8')
                st.download_button(
                    "⬇️ Download Metadata JSON", 
                    data=json_bytes, 
                    file_name="metadata.json", 
                    mime="application/json"
                )
            else:
                raise ValueError("No JSON block found in response.")

        except Exception as e:
            st.error("⚠️ Failed to parse output as JSON.")
            st.text_area("🔎 Raw API Output", value=raw_output or "No response received", height=300)


