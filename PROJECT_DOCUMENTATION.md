# DexGA - Document Extraction using Gemma with Localization

## Project Overview

**DexGA** is a web application that enables intelligent document extraction and interactive chat capabilities using local LLM (Gemma). The application allows users to upload PDF documents, extract key information, and interact with the content through a conversational interface. A unique localization feature highlights the exact location in the document where information is retrieved from.

### Original Project Idea
**DexGA** is designed around a core concept: *Document extraction using Gemma and providing localization features*. Users upload documents and extract information while the Streamlit UI visualizes **exactly where** in the document that information comes from. Beyond extraction, users can engage in interactive chatting with their uploaded documents, creating a comprehensive document intelligence platform.

### Key Features
- 📄 PDF document upload (max 2 pages)
- 🖼️ Image processing and understanding (Vision capability via Gemma 4 E2B)
- 🤖 AI-powered information extraction using Gemma 4 E2B LLM
- 🎯 Source localization - shows exactly where information comes from
- 💬 Interactive chat interface to query documents
- 🔒 Privacy-first: Local processing, automatic cleanup after session
- 🎨 User-friendly Streamlit interface

---

## Architecture

### Layered Architecture Diagram

```
╔════════════════════════════════════════════════════════════════════╗
║                    PRESENTATION LAYER                              ║
║  ┌──────────────────────────────────────────────────────────────┐  ║
║  │         Streamlit Web UI (Responsive Interface)              │  ║
║  │  ┌─────────────────┬──────────────────┬──────────────────┐   │  ║
║  │  │ Upload Module   │ Chat Interface   │ Visualization    │   │  ║
║  │  │                 │                  │ (Highlights)     │   │  ║
║  │  └────────┬────────┴────────┬─────────┴────────┬─────────┘   │  ║
║  └───────────┼─────────────────┼────────────────┬───────────────┤│ ║
║              │                 │                │                  ║
╠══════════════╤═════════════════╤════════════════╤══════════════════╣
║              │ USER             │               │                  ║
║              │ INTERACTIONS     │               │                  ║
╠══════════════╤═════════════════╤════════════════╤══════════════════╣
║        BUSINESS LOGIC LAYER                                        ║
║  ┌──────────────────┬──────────────────┬───────────────────────┐   ║
║  │ Session Manager  │  Chat Manager    │ Document Handler      │   ║
║  │ • Auth/Sessions  │ • Context Store  │ • PDF Parsing         │   ║
║  │ • State Mgmt     │ • Convo History  │ • Text Extraction     │   ║
║  │ • Validation     │ • Prompt Build   │ • Metadata Parse      │   ║
║  └────────┬─────────┴────────┬─────────┴──────────┬────────────┘   ║
║           │                  │                    │                ║
╠═══════════╤════════════════╤═════════════════════╤═════════════════╣
║           │                │                     │                 ║
║  LLM INTEGRATION LAYER            UTILITIES LAYER                  ║
║  ┌─────────┴──────┐        │  ┌──────────────┬────────────────┐    ║
║  │ Gemma Service  │        │  │  PDF Utils   │  Base64 Utils  │    ║
║  │ • API Calls    │        │  │  • PyMuPDF   │  • Encoding    │    ║
║  │ • Inference    │        │  │  • Parsing   │  • Decoding    │    ║
║  │ • Prompts      │        │  └──────────────┴────────────────┘    ║
║  │ • Parsing      │        │  ┌──────────────┬────────────────┐    ║
║  └────────┬───────┘        │  │   Logging    │   Validators   │    ║
║           │                │  │  • File Logs │  • Input Valid │    ║
║           │                │  │  • Debug     │  • Format Check│    ║
║           │                │  └──────────────┴────────────────┘    ║
║           │                │                                       ║
╠═══════════╤════════════════╤═══════════════════════════════════════╣
║           │                │                                       ║
║   DATA ACCESS & STORAGE LAYER                                      ║
║   ┌────────┴────────┬──────┴────────┐                              ║
║   │ Local Storage   │ Session Cache │                              ║
║   │ • Temp PDFs     │ • Chat History│                              ║
║   │ • Base64 Files  │ • Metadata    │                              ║
║   └────────┬────────┴──────┬────────┘                              ║
║            │               │                                       ║
╠════════════╤═══════════════╤═══════════════════════════════════════╣
║            │               │                                       ║
║     CLEANUP & MAINTENANCE LAYER                                    ║
║     ┌───────┴───────┬──────┴──────┐                                ║
║     │ Auto Cleanup  │  Monitoring  │                               ║
║     │ • Delete Temp │  • Error Log │                               ║
║     │ • Clear Cache │  • Metrics   │                               ║
║     └───────────────┴──────────────┘                               ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

### Component Breakdown

**1. Presentation Layer (UI)**
- Streamlit web interface
- Upload component with drag-and-drop
- Chat message display with source highlighting
- Document viewer with bounding box highlights
- Session state management

**2. Business Logic Layer (Core)**
- `Session Manager`: Authentication, session lifecycle, state management
- `Chat Manager`: Conversation history, context building, prompt management
- `Document Handler`: PDF processing, metadata extraction, text parsing

**3. LLM Integration Layer**
- `Gemma Service`: API communication, inference, model management
- `Prompt Engine`: Prompt templates, dynamic prompt generation
- `Response Parser`: Extract structured data, identify source locations

**4. Utilities Layer**
- `PDF Processor`: PyMuPDF integration, text extraction, page parsing
- `Base64 Encoder`: Encoding/decoding for safe data transmission
- `Validators`: Input validation, file format checking
- `Logger`: Debug logging, error tracking

**5. Data Access Layer**
- `Local Storage`: Temporary file management, session storage
- `Session Cache`: In-memory chat history, user metadata
- `Base64 Storage`: Encoded document storage

**6. Cleanup & Maintenance**
- `Auto Cleanup`: Remove temp files after session
- `Monitoring`: Track errors, logs, performance metrics

---

## Project Structure

```
DexGA/
│
├── .env                          # Environment variables (gitignored)
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
├── README.md                     # Quick start guide
├── PROJECT_DOCUMENTATION.md      # Detailed project documentation
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup configuration
├── pytest.ini                    # Pytest configuration
├── Dockerfile                    # Docker container definition
├── docker-compose.yml            # Docker compose setup
│
├── config/                       # Configuration module
│   ├── __init__.py              # Package initializer
│   └── settings.py              # Application settings & constants
│
├── app/                          # Main application package
│   ├── __init__.py              # Package initializer
│   ├── main.py                  # Streamlit entry point
│   │
│   ├── ui/                      # User Interface components
│   │   ├── __init__.py          # Package initializer
│   │   ├── components.py        # Reusable Streamlit components
│   │   ├── pages.py             # Page layouts & views
│   │   └── styles.py            # CSS/styling definitions
│   │
│   ├── core/                    # Core business logic
│   │   ├── __init__.py          # Package initializer
│   │   ├── document_handler.py  # Document processing logic
│   │   ├── chat_manager.py      # Chat & conversation management
│   │   └── extraction_engine.py # Information extraction logic
│   │
│   ├── gemma/                   # Gemma LLM integration
│   │   ├── __init__.py          # Package initializer
│   │   ├── api_call.py          # Gemma API communication
│   │   ├── prompts.py           # Prompt templates & builders
│   │   └── response_parser.py   # Parse & structure responses
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py          # Package initializer
│       ├── pdf_processor.py     # PDF handling with PyMuPDF
│       ├── base64_encoder.py    # Base64 encoding/decoding
│       ├── session_manager.py   # Session lifecycle management
│       ├── validators.py        # Input & file validation
│       ├── logger.py            # Logging configuration
│       └── exceptions.py        # Custom exceptions
│
├── storage/                     # Storage & persistence
│   ├── __init__.py              # Package initializer
│   ├── local_storage.py         # Local file storage operations
│   ├── session_cache.py         # In-memory session caching
│   └── cleanup.py               # Automatic cleanup routines
│
├── tests/                       # Test suite
│   ├── __init__.py              # Package initializer
│   ├── conftest.py              # Pytest fixtures & config
│   │
│   ├── unit/                    # Unit tests
│   │   ├── test_pdf_processor.py
│   │   ├── test_base64_encoder.py
│   │   ├── test_validators.py
│   │   └── test_gemma_api.py
│   │
│   └── integration/             # Integration tests
│       ├── test_document_handler.py
│       ├── test_chat_flow.py
│       └── test_end_to_end.py
│
└── logs/                        # Application logs
    ├── app.log                  # Main application log
    └── error.log                # Error log
```

### File Descriptions

| File | Purpose |
|------|---------|
| **config/settings.py** | App constants, API keys, model config, file size limits |
| **app/main.py** | Streamlit app entry point, page routing, session setup |
| **app/ui/components.py** | Reusable Streamlit UI components (buttons, forms, viewers) |
| **app/ui/pages.py** | Multi-page layouts (Upload, Chat, History, Settings) |
| **app/core/document_handler.py** | PDF loading, parsing, chunking, metadata extraction |
| **app/core/chat_manager.py** | Chat history, context building, conversation state |
| **app/core/extraction_engine.py** | Information extraction logic, source tracking |
| **app/gemma/api_call.py** | Ollama/Gemma API calls, model inference |
| **app/gemma/prompts.py** | Prompt templates with variables, dynamic prompt building |
| **app/gemma/response_parser.py** | Parse LLM responses, extract structured data |
| **app/utils/pdf_processor.py** | PyMuPDF operations, text extraction, bounding boxes |
| **app/utils/base64_encoder.py** | Encode/decode PDFs to Base64 for transmission |
| **app/utils/session_manager.py** | Session lifecycle, user state, cleanup triggers |
| **app/utils/validators.py** | File type, size, format validation |
| **app/utils/logger.py** | Centralized logging configuration |
| **app/utils/exceptions.py** | Custom exception classes |
| **storage/local_storage.py** | Create/read/delete temp files, directory management |
| **storage/session_cache.py** | In-memory storage for chat history, metadata |
| **storage/cleanup.py** | Auto-delete temp files, cache clearing |
| **tests/** | Unit & integration test suite |

---

## Technical Stack

### Dependencies
```
streamlit              # Web UI framework
pymupdf               # PDF processing and parsing
pillow                # Image handling
ollama                # Local LLM runtime (Gemma)
python-dotenv         # Environment variable management
numpy                 # Numerical operations
pandas                # Data manipulation (optional)
```

### Technology Choices

| Component | Technology | Reason |
|-----------|-----------|--------|
| **Frontend** | Streamlit | Rapid prototyping, interactive UI, easy deployment |
| **PDF Handling** | PyMuPDF | Fast PDF parsing, accurate text extraction, image support |
| **LLM** | Gemma 4 E2B (Local) | Vision capability, privacy-first, offline, no API costs |
| **Encoding** | Base64 | Safe data transmission, cross-platform compatibility |

---

## Data Flow

### 1. Document Upload & Processing
```
User Uploads PDF
      ↓
Streamlit receives file
      ↓
Validate (max 2 pages)
      ↓
PyMuPDF extracts text + metadata
      ↓
Convert to Base64
      ↓
Store temporarily in local storage
      ↓
Display in UI
```

### 2. Information Extraction
```
User requests extraction / asks question
      ↓
Streamlit prepares prompt
      ↓
Send document content + query to Gemma
      ↓
Gemma processes and extracts info
      ↓
Response includes source page/location
      ↓
Display with highlighting in UI
```

### 3. Chat Interaction
```
User types message
      ↓
Context-aware prompt creation
      ↓
Gemma retrieves relevant sections
      ↓
Generate conversational response
      ↓
Show source localization
      ↓
Store in chat history
```

### 4. Session Cleanup
```
User ends session / closes browser
      ↓
Delete temporary PDF files
      ↓
Clear session memory
      ↓
Device returns to clean state
```

---

## Core Features in Detail

### 1. **PDF Upload & Validation**
- Accept PDF files through Streamlit file uploader
- Enforce maximum 2-page limit
- Display file info (name, page count, size)
- Error handling for corrupted files

### 2. **Information Extraction**
- Extract text content with position metadata
- Parse document structure (headings, paragraphs, tables)
- Generate embeddings for efficient retrieval
- Provide page/section references

### 3. **Source Localization**
- Track extracted info source (page number, section)
- Highlight relevant areas in PDF viewer
- Display visual indicators in chat
- Citation format: "Page X, Section Y"

### 4. **Interactive Chat**
- Maintain conversation context
- Multi-turn dialogue support
- Follow-up question handling
- Contextual understanding of user queries

---

## Security & Privacy Considerations

✅ **Privacy-First Design**
- All processing happens locally
- No data sent to external servers
- No cloud storage dependency
- Automatic session cleanup

🔒 **Data Protection**
- Base64 encoding for safe transmission
- Temporary files deleted after session
- Memory cleared on logout
- No persistent logs of document content

⚠️ **Security Notes**
- Run on trusted networks
- Consider HTTPS for production
- Implement user authentication if needed
- Regular dependency updates

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Ollama (for Gemma 4 E2B model)
- 6GB+ RAM recommended
- 1GB+ disk space (model storage)

### Installation Steps

1. **Clone/Setup Project**
```bash
cd DexGA
pip install -r requirements.txt
```

2. **Download Gemma 4 E2B Model**
```bash
ollama pull gemma-4:e2b
```

3. **Run Application**
```bash
streamlit run app/main.py
```

4. **Access Application**
Open browser to `http://localhost:8501`

---

## Usage Workflow

1. **Upload Document**
   - Click "Upload PDF" button
   - Select file (max 2 pages)
   - View document preview

2. **Extract Information**
   - Enter query in chat input
   - Click "Send" or press Enter
   - View extracted information with source

3. **Ask Questions**
   - Type follow-up questions
   - Chat maintains context
   - Source localization updates accordingly

4. **Review & Export** (Optional)
   - View chat history
   - See source references
   - Copy extracted information

5. **End Session**
   - Close browser or click logout
   - Automatic cleanup triggered
   - Device cleared of temporary files

---

## Suggested Improvements & Enhancements

This section outlines critical improvements to transform DexGA from a basic POC into a production-ready solution:

### 1. **Document Format Support** 
**Improvement**: Support multiple document formats beyond PDF
- DOCX/DOC files for Word documents
- Images (JPEG, PNG, etc.) with OCR capabilities
- TXT and CSV for structured data
- Scanned document OCR support
- **Implementation**: Extend PDF handler to multi-format processor

### 2. **Enhanced Context Management**
**Improvement**: Implement smart retrieval for better accuracy
- **Document Chunking**: Split documents into manageable chunks (300-500 tokens)
- **Semantic Embeddings**: Create embeddings for efficient retrieval
- **Vector Database**: Use Chroma or FAISS to store and retrieve relevant sections
- **Context Window Optimization**: Feed only relevant document sections to LLM
- **Benefits**: Faster responses, better accuracy, reduced token usage

### 3. **Advanced Source Localization Visualization**
**Improvement**: Go beyond text references with visual highlights
- **PDF Viewer Integration**: Embed PDF viewer in Streamlit
- **Bounding Box Highlighting**: Draw boxes around extracted text locations
- **Color-Coded References**: Different colors for different extraction types
- **Interactive Highlights**: Click highlights to see full context
- **Page Navigation**: Jump to specific pages with one click

### 4. **Conversation Memory & History**
**Improvement**: Maintain context across conversations
- **Session-Based Memory**: Store chat history during session
- **Conversation Context**: Reference previous messages for follow-ups
- **Summary Generation**: Auto-generate conversation summaries
- **Export Options**: Save chats as JSON/PDF
- **Multi-turn Support**: Enable complex dialogue with context retention

### 5. **Robust Error Handling**
**Improvement**: Handle edge cases gracefully
- **File Validation**: Check format, size, corruption
- **Large Document Handling**: Implement pagination for 2+ pages
- **Timeout Management**: Handle slow LLM responses
- **Graceful Degradation**: Fallback responses on failure
- **User Feedback**: Clear error messages with recovery options

### 6. **Performance Optimization**
**Improvement**: Ensure fast, responsive experience
- **Response Caching**: Cache frequent queries and responses
- **Asynchronous Processing**: Non-blocking document processing
- **Batch Processing**: Handle multiple queries efficiently
- **GPU Acceleration**: Leverage GPU for Gemma inference if available
- **Response Streaming**: Stream LLM responses for real-time feedback
- **Loading States**: Show progress indicators for long operations

### 7. **Extraction Templates & Customization**
**Improvement**: Let users define what to extract
- **Template Builder**: Create custom extraction templates
- **Pre-built Templates**: Resume parsing, Invoice extraction, Contract analysis
- **Field Mapping**: Map document fields to extraction targets
- **Validation Rules**: Ensure extracted data quality
- **Export Schemas**: JSON/CSV export with defined fields

### 8. **Advanced Features for Production**
- **Authentication**: User login & session management
- **Multi-document Chat**: Chat across multiple documents
- **Comparison Tools**: Compare extractions across documents
- **Batch Upload**: Process multiple documents
- **Webhook Integration**: API endpoints for external systems
- **Audit Trail**: Log all extractions and queries

---

## Architecture Enhancement Roadmap

```
Phase 1 (Current POC)
└── Basic PDF upload → Gemma extraction → Chat

Phase 2 (Improvements)
├── Vector DB integration
├── Advanced visualization
├── Multi-format support
└── Template system

Phase 3 (Enterprise)
├── Authentication & RBAC
├── API endpoints
├── Batch processing
└── Analytics dashboard
```

---

## Error Handling

| Error | Handling |
|-------|----------|
| File too large | Reject with user message |
| PDF corruption | Display error, allow re-upload |
| LLM timeout | Graceful fallback message |
| Memory overflow | Session reset |
| Invalid extraction | Retry with refined prompt |

---

## Deployment Notes

### Development Environment
```bash
streamlit run app/main.py
```

### Production Deployment
- Deploy on cloud server (AWS, GCP, Azure)
- Use environment variables for config
- Implement load balancing for scale
- Add monitoring & logging
- Enable HTTPS/SSL

### Scalability Considerations
- GPU acceleration for Gemma inference
- Distributed model serving (vLLM, Ray)
- Caching layer for repeated queries
- Horizontal scaling with message queue

---

## Testing Strategy

- **Unit Tests**: PDF parsing, text extraction
- **Integration Tests**: End-to-end workflows
- **Performance Tests**: Large document handling
- **Security Tests**: File upload validation

---

## Support & Maintenance

### Known Limitations
- ⚠️ Maximum 2 pages per document (POC limit)
- ⚠️ Single user session
- ⚠️ No persistence between sessions
- ⚠️ Requires local Gemma model

### Future Scope

- Cloud-based deployment
- Mobile application
- Enterprise integration

---

**Last Updated**: May 2026  
**Version**: 1.0 (Work)
