# DexGA - Document Extraction using Gemma with Localization

Quick start guide for DexGA application.

## Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download Gemma 4 E2B Model (with Vision Capability)
```bash
ollama pull gemma-4:e2b
```

### 3. Run Application
```bash
streamlit run app/main.py
```

The app will be available at `http://localhost:8501`

## Project Structure

- `config/` - Configuration and settings
- `app/` - Main application code
  - `ui/` - Streamlit UI components
  - `core/` - Business logic
  - `gemma/` - LLM integration
  - `utils/` - Utility functions
- `storage/` - Storage and cache management
- `tests/` - Test suite

## Features

✅ PDF document upload and parsing  
✅ Image understanding and processing (Vision capability)  
✅ AI-powered information extraction  
✅ Source localization  
✅ Interactive chat interface  
✅ Local processing for privacy  
✅ Automatic session cleanup  

## Documentation

See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for detailed documentation.

## Environment Variables

Create `.env` file with:
```
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=gemma:7b
LOG_LEVEL=INFO
DEBUG_MODE=False
```

## Requirements

- Python 3.8+
- Ollama with Gemma 4 E2B model (vision/image processing support)
- 6GB+ RAM (recommended for image processing)
- 1GB+ disk space (model storage)

## Support

For issues or questions, please refer to the project documentation.
