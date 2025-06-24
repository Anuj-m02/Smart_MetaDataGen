import sys
import os
import streamlit as st
import json
import re

# ✅ Add backend directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.extractor import extract_text
from backend.ocr import extract_text_from_image
from backend.metadata_gen import generate_metadata

# ✅ Set page config
st.set_page_config(page_title="SmartMeta: AI Metadata Generator", layout="wide")
st.title("📄 SmartMeta: Automated Metadata Generation using GenAI")

# ✅ Add sidebar with instructions
st.sidebar.title("📋 Instructions")
st.sidebar.markdown("""
1. Upload a document (PDF, DOCX, TXT, or Image)
2. Preview the extracted text
3. Click 'Generate Metadata' to analyze
4. Download the generated metadata as JSON
""")

# ✅ File uploader
uploaded_file = st.file_uploader(
    "Upload a document (PDF, DOCX, TXT, PNG, JPG)", 
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"]
)

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    
    # ✅ Display file info
    st.info(f"**File:** {uploaded_file.name} | **Size:** {uploaded_file.size:,} bytes")
    
    # ✅ Save to temporary folder
    os.makedirs("app/temp", exist_ok=True)
    file_path = os.path.join("app/temp", uploaded_file.name)
    
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # ✅ Extract text from file
        with st.spinner("Extracting text from document..."):
            if uploaded_file.type.startswith("image/"):
                text = extract_text_from_image(file_path)
            else:
                text = extract_text(file_path)
        
        # ✅ Check if text extraction was successful
        if not text or len(text.strip()) < 10:
            st.warning("⚠️ Very little text extracted. Please check if the file is readable or contains text.")
            text = "No meaningful text could be extracted from this document."
        
        # ✅ Show extracted text preview
        st.subheader("📜 Extracted Text Preview")
        
        # Show character count
        st.caption(f"Total characters extracted: {len(text):,}")
        
        # Show preview in expandable section
        with st.expander("View Full Text", expanded=False):
            st.text_area("Full Text", value=text, height=400, disabled=True)
        
        # Show truncated preview
        preview_text = text[:2000] + "..." if len(text) > 2000 else text
        st.text_area("Preview (First 2000 characters)", value=preview_text, height=200, disabled=True)
        
        # ✅ Button to generate metadata
        if st.button("🔍 Generate Metadata", type="primary"):
            if len(text.strip()) < 10:
                st.error("❌ Insufficient text content for metadata generation.")
            else:
                with st.spinner("🤖 Analyzing document with GenAI..."):
                    try:
                        raw_output = generate_metadata(text)
                        
                        # ✅ Parse JSON response
                        try:
                            # Try to extract JSON from response
                            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_output, re.DOTALL | re.IGNORECASE)
                            
                            if json_match:
                                json_str = json_match.group(1)
                            else:
                                # Try to find JSON without code blocks
                                json_match = re.search(r'(\{.*\})', raw_output, re.DOTALL)
                                if json_match:
                                    json_str = json_match.group(1)
                                else:
                                    raise ValueError("No JSON found in response")
                            
                            # Parse the JSON
                            metadata = json.loads(json_str)
                            
                            # ✅ Display metadata in organized format
                            st.subheader("📊 Generated Metadata")
                            
                            # Create tabs for better organization
                            tab1, tab2, tab3 = st.tabs(["📋 Overview", "🏷️ Details", "📥 Download"])
                            
                            with tab1:
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    if 'title' in metadata:
                                        st.metric("Title", metadata['title'])
                                    if 'document_category' in metadata:
                                        st.metric("Category", metadata['document_category'])
                                    if 'language' in metadata:
                                        st.metric("Language", metadata['language'])
                                    if 'sentiment' in metadata:
                                        st.metric("Sentiment", metadata['sentiment'])
                                
                                with col2:
                                    if 'author' in metadata:
                                        st.metric("Author", metadata['author'])
                                    if 'estimated_reading_time' in metadata:
                                        st.metric("Reading Time", f"{metadata['estimated_reading_time']} min")
                                    if 'confidential' in metadata:
                                        st.metric("Confidential", metadata['confidential'])
                                
                                if 'summary' in metadata:
                                    st.subheader("📝 Summary")
                                    st.write(metadata['summary'])
                            
                            with tab2:
                                st.json(metadata)
                            
                            with tab3:
                                # ✅ Download button
                                json_bytes = json.dumps(metadata, indent=4).encode('utf-8')
                                st.download_button(
                                    "⬇️ Download Metadata JSON",
                                    data=json_bytes,
                                    file_name=f"metadata_{uploaded_file.name}.json",
                                    mime="application/json"
                                )
                                
                                # Option to copy to clipboard
                                st.code(json.dumps(metadata, indent=2), language="json")
                                
                        except json.JSONDecodeError as e:
                            st.error(f"❌ Failed to parse JSON response: {str(e)}")
                            st.subheader("🔍 Raw API Response")
                            st.text_area("Debug Output", value=raw_output, height=300)
                        
                        except Exception as e:
                            st.error(f"❌ Error processing metadata: {str(e)}")
                            st.subheader("🔍 Raw API Response")
                            st.text_area("Debug Output", value=raw_output, height=300)
                    
                    except Exception as e:
                        st.error(f"❌ Failed to generate metadata: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
    
    finally:
        # ✅ Clean up temporary file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

else:
    # ✅ Show instructions when no file is uploaded
    st.info("👆 Please upload a document to get started!")
    
    # ✅ Show supported formats
    st.subheader("📋 Supported Formats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Documents:**
        - 📄 PDF files
        - 📝 DOCX files
        - 📄 TXT files
        """)
    
    with col2:
        st.markdown("""
        **Images:**
        - 🖼️ PNG files
        - 📸 JPG/JPEG files
        - 🔍 OCR enabled
        """)
    
    with col3:
        st.markdown("""
        **Features:**
        - 🤖 AI-powered analysis
        - 🏷️ Rich metadata extraction
        - 📥 JSON export
        """)