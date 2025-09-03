# Python Code Editor with LLaMA3 Integration

A web-based Python code editor that provides intelligent code recommendations using LLaMA3, code execution capabilities, and comprehensive error analysis with fix suggestions.

## Features

- **Web-based Code Editor**: Modern, responsive interface with syntax highlighting
- **Ollama AI Integration**: AI-powered code recommendations and suggestions
- **Real-time Code Suggestions**: Instant suggestions as you type with Tab completion
- **Python Code Execution**: Fast Python code execution with caching
- **Filesystem Management**: Create, edit, save, and organize Python files and folders
- **Error Analysis**: Post-execution error analysis with intelligent fix recommendations
- **Context-aware Hints**: Smart suggestions based on your current code context
- **Workspace Download**: Download your entire workspace as a ZIP file
- **Keyboard Shortcuts**: Tab completion, Ctrl+Space for suggestions, Ctrl+Enter to run

## Prerequisites

- Python 3.8+
- LLaMA3 model deployed locally (accessible via API)
- Modern web browser

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CodeEditor
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Ollama Connection
Create a `.env` file in the root directory:
```env
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama3
WORKSPACE_DIR=./workspace
```

### 5. Start the Application
```bash
python app.py
```

The application will be available at `http://localhost:5002`

## Project Structure

```
CodeEditor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               # Static assets (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/            # HTML templates
├── utils/                # Utility functions
│   ├── __init__.py
│   ├── llama_client.py   # LLaMA3 API client
│   ├── code_executor.py  # Python code execution
│   └── file_manager.py   # Filesystem operations
├── workspace/            # Default workspace directory
└── README.md
```

## Usage

### Code Editor
1. Open the web interface in your browser
2. Use the file tree to navigate and create Python files
3. Write Python code in the editor
4. Use **Ctrl+Enter** to execute code
5. View execution results and any errors

### Real-time Suggestions
- **Type patterns** like `#function to add` and press **Tab** for instant suggestions
- **Press Ctrl+Space** to see common code patterns
- **Context hints** appear automatically as you code
- **Tab completion** accepts suggestions instantly

### File Management
- **Create folders**: Click "New Folder" button
- **Create files**: Click "New File" button  
- **Download workspace**: Click "Download" button to get ZIP file
- **Organize projects**: Drag and drop files in the file tree

### LLaMA3 Integration
- Code suggestions appear as you type
- Right-click for context-aware recommendations
- Error analysis provides intelligent fix suggestions

### File Management
- Create new Python files
- Save files automatically
- Organize files in folders
- Import existing Python projects

## API Endpoints

- `GET /` - Main editor interface
- `POST /api/execute` - Execute Python code
- `POST /api/suggest` - Get LLaMA3 code suggestions
- `GET /api/files` - List workspace files
- `POST /api/files` - Create/save files
- `DELETE /api/files/<path>` - Delete files
- `POST /api/analyze` - Analyze code errors

## Configuration

### Ollama Setup
Ensure your Ollama service is running and accessible. The application expects:
- Ollama running on localhost:11434
- LLaMA3 model available (or any other model you specify)
- Support for Python code analysis
- Error understanding capabilities

### Workspace Configuration
- Default workspace: `./workspace`
- Configurable via environment variables
- Supports multiple project directories

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Testing
```bash
python -m pytest tests/
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Check if Ollama service is running (`ollama serve`)
   - Verify API endpoint in `.env` file (should be http://localhost:11434)
   - Check if the specified model is available (`ollama list`)
   - Check network connectivity

2. **Code Execution Errors**
   - Ensure Python environment is properly set up
   - Check file permissions in workspace directory
   - Verify Python packages are installed

3. **File System Issues**
   - Check workspace directory permissions
   - Ensure sufficient disk space
   - Verify file path configurations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation
