# 📄 SmartMeta: Automated Metadata Generation System

An intelligent document analysis system that automatically generates comprehensive metadata from various document formats using AI/GenAI technology.

## 🌟 Features

- **Multi-format Support**: PDF, DOCX, TXT, and image files (PNG, JPG, JPEG)
- **OCR Integration**: Extract text from scanned documents and images
- **AI-Powered Analysis**: Generate rich metadata using advanced language models
- **Web Interface**: User-friendly Streamlit application
- **Comprehensive Metadata**: Extract 15+ metadata fields including:
  - Title, Summary, Keywords
  - Document Category, Language, Sentiment
  - Named Entities (People, Organizations, Locations)
  - Content Features, Technical Level
  - And much more!

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system
- OpenRouter API key (for AI analysis)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smartmeta-metadata-generator.git
   cd smartmeta-metadata-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   
   **Windows:**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install and note the installation path
   
   **macOS:**
   ```bash
   brew install tesseract
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install tesseract-ocr
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file and add your OpenRouter API key
   ```

5. **Get OpenRouter API Key**
   - Visit [OpenRouter.ai](https://openrouter.ai/)
   - Sign up and get your API key
   - Add it to your `.env` file

### Running the Application

```bash
streamlit run app/main.py
```

The application will be available at `http://localhost:8501`

## 📁 Project Structure

```
smartmeta-metadata-generator/
├── app/
│   ├── main.py              # Streamlit web application
│   └── temp/                # Temporary file storage
├── backend/
│   ├── extractor.py         # Document text extraction
│   ├── ocr.py              # OCR functionality
│   └── metadata_gen.py     # AI metadata generation
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── README.md               # This file
└── demo/                   # Demo materials
    └── sample_documents/   # Sample files for testing
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

### Windows-Specific Configuration

If you're on Windows, you may need to configure paths in the Python files:

**In `backend/ocr.py` and `backend/extractor.py`:**
```python
# Uncomment and adjust these paths
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"
```

## 📋 Supported File Formats

| Format | Description | Features |
|--------|-------------|----------|
| PDF | Portable Document Format | Text extraction + OCR for scanned PDFs |
| DOCX | Microsoft Word Document | Text + Tables extraction |
| TXT | Plain Text File | Multiple encoding support |
| PNG/JPG | Image Files | OCR text extraction |

## 🤖 AI Models

The system supports multiple AI models through OpenRouter:

- **meta-llama/llama-3-8b-instruct** (default)
- **openai/gpt-3.5-turbo**
- **anthropic/claude-3-haiku**
- **google/gemini-pro**
- **mistralai/mistral-7b-instruct**

Change the model in `backend/metadata_gen.py`:
```python
MODEL = "openai/gpt-3.5-turbo"  # Change this line
```

## 📊 Generated Metadata Fields

The system extracts comprehensive metadata including:

### Basic Information
- **Title**: Document title (inferred if not explicit)
- **Summary**: 2-3 sentence overview
- **Keywords**: 5-10 relevant keywords
- **Language**: Primary document language

### Classification
- **Document Category**: Legal, Academic, Finance, etc.
- **Sentiment**: Positive, Negative, Neutral
- **Technical Level**: Beginner, Intermediate, Advanced
- **Intended Audience**: Target readership

### Content Analysis
- **Named Entities**: People, Organizations, Locations
- **Important Dates**: Key dates mentioned
- **Document Structure**: Main sections
- **Content Features**: Tables, Charts, Images, References

### Metrics
- **Word Count**: Estimated word count
- **Reading Time**: Estimated reading time in minutes
- **Document Quality**: High, Medium, Low assessment

## 🧪 Testing

Test individual components:

```python
# Test text extraction
from backend.extractor import test_extraction
test_extraction("path/to/your/document.pdf")

# Test OCR functionality
from backend.ocr import test_ocr_setup
test_ocr_setup()

# Test metadata generation
from backend.metadata_gen import test_metadata_generation
test_metadata_generation()
```

## 🚀 Deployment

### Local Deployment
```bash
streamlit run app/main.py --server.port 8501
```

### Cloud Deployment

**Streamlit Cloud:**
1. Push code to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Add secrets for environment variables

**Heroku:**
1. Create `Procfile`: `web: streamlit run app/main.py --server.port=$PORT`
2. Add buildpacks for Python and APT (for Tesseract)
3. Configure environment variables

**Docker:**
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . /app
WORKDIR /app

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔍 Troubleshooting

### Common Issues

**1. Tesseract not found**
```
pytesseract.pytesseract.TesseractNotFoundError
```
- **Solution**: Install Tesseract OCR and configure path in code

**2. OpenRouter API errors**
```
API error: 401 - Unauthorized
```
- **Solution**: Check your API key in `.env` file

**3. PDF processing errors**
```
No module named 'fitz'
```
- **Solution**: Install PyMuPDF: `pip install PyMuPDF`

**4. Memory issues with large files**
- **Solution**: The system automatically truncates large texts. For very large files, consider pre-processing.

### Performance Tips

- **Large Documents**: Files are automatically truncated to prevent timeout
- **Scanned PDFs**: OCR processing takes longer; be patient
- **API Limits**: The system includes rate limiting and retry logic

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 🎯 Future Enhancements

- [ ] Batch processing for multiple files
- [ ] Custom metadata templates
- [ ] Integration with document management systems
- [ ] Advanced NLP features (topic modeling, summarization)
- [ ] Multi-language support enhancement
- [ ] API endpoint for programmatic access

## 📈 Demo

A 2-minute demo video showing the system in action is available in the `demo/` folder.

---

**Built with ❤️ using Python, Streamlit, and AI**
