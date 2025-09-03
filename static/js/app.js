/**
 * Python Code Editor - Frontend Application
 * Handles code editing, file management, and LLaMA3 integration
 */

class CodeEditor {
    constructor() {
        this.editor = null;
        this.currentFile = 'untitled.py';
        this.files = {};
        this.suggestionTimeout = null;
        
        this.init();
    }
    
    init() {
        this.initCodeMirror();
        this.bindEvents();
        this.loadFiles();
        this.setupKeyboardShortcuts();
    }
    
    initCodeMirror() {
        // Initialize CodeMirror editor
        this.editor = CodeMirror.fromTextArea(document.getElementById('codeEditor'), {
            mode: 'python',
            theme: 'monokai',
            lineNumbers: true,
            autoCloseBrackets: true,
            matchBrackets: true,
            showTrailingSpace: true,
            styleActiveLine: true,
            indentUnit: 4,
            tabSize: 4,
            indentWithTabs: false,
            lineWrapping: true,
            foldGutter: true,
            gutters: ['CodeMirror-linenumbers'],
            extraKeys: {
                'Ctrl-Enter': () => this.runCode(),
                'Ctrl-S': () => this.saveCurrentFile(),
                'Ctrl-N': () => this.showNewFileModal(),
                'Ctrl-F': () => this.searchFiles()
            }
        });
        
        // Set initial content
        this.editor.setValue('# Welcome to Python Code Editor!\n# Start coding here...\n\nprint("Hello, World!")');
        
        // Handle content changes for LLaMA3 suggestions
        this.editor.on('change', () => {
            this.handleCodeChange();
        });
    }
    
    bindEvents() {
        // Button events
        document.getElementById('runBtn').addEventListener('click', () => this.runCode());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveCurrentFile());
        document.getElementById('newFileBtn').addEventListener('click', () => this.showNewFileModal());
        document.getElementById('refreshFilesBtn').addEventListener('click', () => this.loadFiles());
        document.getElementById('createFolderBtn').addEventListener('click', () => this.showNewFolderModal());
        
        // Panel toggles
        document.getElementById('suggestionsToggle').addEventListener('click', () => this.toggleSuggestionsPanel());
        document.getElementById('outputToggle').addEventListener('click', () => this.toggleOutputPanel());
        
        // Output panel tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchOutputTab(e.target.dataset.tab));
        });
        
        // Modal events
        document.getElementById('createNewFile').addEventListener('click', () => this.createNewFile());
        document.getElementById('cancelNewFile').addEventListener('click', () => this.hideModal('newFileModal'));
        document.getElementById('createNewFolder').addEventListener('click', () => this.createNewFolder());
        document.getElementById('cancelNewFolder').addEventListener('click', () => this.hideModal('newFolderModal'));
        
        // Modal close buttons
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                this.hideModal(modal.id);
            });
        });
        
        // Click outside modal to close
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hideModal(modal.id);
                }
            });
        });
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'Enter':
                        e.preventDefault();
                        this.runCode();
                        break;
                    case 's':
                        e.preventDefault();
                        this.saveCurrentFile();
                        break;
                    case 'n':
                        e.preventDefault();
                        this.showNewFileModal();
                        break;
                    case 'f':
                        e.preventDefault();
                        this.searchFiles();
                        break;
                }
            }
        });
    }
    
    async runCode() {
        const code = this.editor.getValue();
        if (!code.trim()) {
            this.showNotification('No code to execute', 'warning');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displayExecutionResult(result.result);
            } else {
                this.showNotification(`Execution failed: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showNotification(`Execution error: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    displayExecutionResult(result) {
        // Display output
        const outputContent = document.getElementById('outputContent');
        if (result.output) {
            outputContent.innerHTML = `<pre class="code-output">${this.escapeHtml(result.output)}</pre>`;
        } else {
            outputContent.innerHTML = '<div class="output-placeholder"><i class="fas fa-check-circle"></i><p>Code executed successfully (no output)</p></div>';
        }
        
        // Display errors if any
        const errorsContent = document.getElementById('errorsContent');
        if (result.error) {
            errorsContent.innerHTML = `<pre class="code-error">${this.escapeHtml(result.error)}</pre>`;
            this.switchOutputTab('errors');
        } else {
            errorsContent.innerHTML = '<div class="errors-placeholder"><i class="fas fa-check-circle"></i><p>No errors</p></div>';
        }
        
        // Display LLaMA3 suggestions if available
        const fixesContent = document.getElementById('fixesContent');
        if (result.suggestions && result.suggestions.length > 0) {
            const suggestionsHtml = result.suggestions.map(suggestion => 
                `<div class="suggestion-item"><i class="fas fa-lightbulb"></i> ${this.escapeHtml(suggestion)}</div>`
            ).join('');
            fixesContent.innerHTML = suggestionsHtml;
            this.switchOutputTab('suggestions');
        } else {
            fixesContent.innerHTML = '<div class="fixes-placeholder"><i class="fas fa-check-circle"></i><p>No fixes needed</p></div>';
        }
        
        // Switch to output tab by default
        this.switchOutputTab('output');
    }
    
    async saveCurrentFile() {
        const content = this.editor.getValue();
        const fileName = this.currentFile;
        
        try {
            const response = await fetch('/api/files', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    path: fileName,
                    content: content
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showNotification('File saved successfully', 'success');
                this.files[fileName] = content;
            } else {
                this.showNotification(`Save failed: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showNotification(`Save error: ${error.message}`, 'error');
        }
    }
    
    async loadFiles() {
        try {
            const response = await fetch('/api/files');
            const result = await response.json();
            
            if (result.success) {
                this.files = result.files;
                this.renderFileTree();
            } else {
                this.showNotification(`Failed to load files: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showNotification(`Load error: ${error.message}`, 'error');
        }
    }
    
    renderFileTree() {
        const fileTree = document.getElementById('fileTree');
        fileTree.innerHTML = '';
        
        if (this.files.length === 0) {
            fileTree.innerHTML = '<div class="placeholder">No files in workspace</div>';
            return;
        }
        
        this.files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = `file-item ${file.type}`;
            fileItem.dataset.path = file.path;
            
            const icon = file.type === 'directory' ? 'fas fa-folder' : 'fas fa-file-code';
            fileItem.innerHTML = `
                <i class="${icon}"></i>
                <span>${file.name}</span>
            `;
            
            fileItem.addEventListener('click', () => this.openFile(file.path));
            fileTree.appendChild(fileItem);
        });
    }
    
    async openFile(filePath) {
        if (this.files.find(f => f.path === filePath)?.type === 'directory') {
            return; // Don't open directories
        }
        
        try {
            const response = await fetch(`/api/files/${encodeURIComponent(filePath)}`);
            const result = await response.json();
            
            if (result.success) {
                this.editor.setValue(result.content);
                this.currentFile = filePath;
                this.updateActiveTab(filePath);
                this.showNotification(`Opened ${filePath}`, 'success');
            } else {
                this.showNotification(`Failed to open file: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showNotification(`Open error: ${error.message}`, 'error');
        }
    }
    
    updateActiveTab(fileName) {
        // Update tab text
        const activeTab = document.querySelector('.tab.active');
        if (activeTab) {
            activeTab.querySelector('span').textContent = fileName;
            activeTab.dataset.file = fileName;
        }
    }
    
    handleCodeChange() {
        // Debounce LLaMA3 suggestions
        clearTimeout(this.suggestionTimeout);
        this.suggestionTimeout = setTimeout(() => {
            this.getSuggestions();
        }, 1000);
    }
    
    async getSuggestions() {
        const code = this.editor.getValue();
        if (!code.trim() || code.length < 10) {
            return;
        }
        
        try {
            const response = await fetch('/api/suggest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: code,
                    context: this.currentFile
                })
            });
            
            const result = await response.json();
            
            if (result.success && result.suggestions) {
                this.displaySuggestions(result.suggestions);
            }
        } catch (error) {
            console.error('Failed to get suggestions:', error);
        }
    }
    
    displaySuggestions(suggestions) {
        const suggestionsContent = document.getElementById('suggestionsContent');
        
        if (suggestions.length === 0) {
            suggestionsContent.innerHTML = '<p class="placeholder">No suggestions available</p>';
            return;
        }
        
        const suggestionsHtml = suggestions.map(suggestion => 
            `<div class="suggestion-item"><i class="fas fa-lightbulb"></i> ${this.escapeHtml(suggestion)}</div>`
        ).join('');
        
        suggestionsContent.innerHTML = suggestionsHtml;
    }
    
    showNewFileModal() {
        document.getElementById('newFileModal').classList.add('active');
        document.getElementById('newFileName').focus();
    }
    
    showNewFolderModal() {
        document.getElementById('newFolderModal').classList.add('active');
        document.getElementById('newFolderName').focus();
    }
    
    hideModal(modalId) {
        document.getElementById(modalId).classList.remove('active');
    }
    
    async createNewFile() {
        const fileName = document.getElementById('newFileName').value.trim();
        const content = document.getElementById('newFileContent').value;
        
        if (!fileName) {
            this.showNotification('Please enter a file name', 'warning');
            return;
        }
        
        try {
            const response = await fetch('/api/files', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    path: fileName,
                    content: content
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.editor.setValue(content);
                this.currentFile = fileName;
                this.updateActiveTab(fileName);
                this.hideModal('newFileModal');
                this.loadFiles();
                this.showNotification('File created successfully', 'success');
            } else {
                this.showNotification(`Creation failed: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showNotification(`Creation error: ${error.message}`, 'error');
        }
    }
    
    async createNewFolder() {
        const folderName = document.getElementById('newFolderName').value.trim();
        
        if (!folderName) {
            this.showNotification('Please enter a folder name', 'warning');
            return;
        }
        
        try {
            // For now, we'll create an empty Python file as a placeholder
            // In a real implementation, you'd want to create actual directories
            const response = await fetch('/api/files', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    path: `${folderName}/__init__.py`,
                    content: `# ${folderName} package`
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.hideModal('newFolderModal');
                this.loadFiles();
                this.showNotification('Folder created successfully', 'success');
            } else {
                this.showNotification(`Creation failed: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showNotification(`Creation error: ${error.message}`, 'error');
        }
    }
    
    toggleSuggestionsPanel() {
        const panel = document.getElementById('suggestionsPanel');
        panel.classList.toggle('collapsed');
        
        const toggle = document.getElementById('suggestionsToggle');
        const icon = toggle.querySelector('i');
        if (panel.classList.contains('collapsed')) {
            icon.className = 'fas fa-chevron-down';
        } else {
            icon.className = 'fas fa-chevron-up';
        }
    }
    
    toggleOutputPanel() {
        const panel = document.getElementById('outputPanel');
        panel.classList.toggle('collapsed');
        
        const toggle = document.getElementById('outputToggle');
        const icon = toggle.querySelector('i');
        if (panel.classList.contains('collapsed')) {
            icon.className = 'fas fa-chevron-right';
        } else {
            icon.className = 'fas fa-chevron-left';
        }
    }
    
    switchOutputTab(tabName) {
        // Remove active class from all tabs and content
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        // Add active class to selected tab and content
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`${tabName}Content`).classList.add('active');
    }
    
    searchFiles() {
        // Implement file search functionality
        this.showNotification('File search coming soon!', 'info');
    }
    
    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
        
        // Close button
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        });
    }
    
    getNotificationIcon(type) {
        switch (type) {
            case 'success': return 'check-circle';
            case 'error': return 'exclamation-circle';
            case 'warning': return 'exclamation-triangle';
            default: return 'info-circle';
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CodeEditor();
});

// Add notification styles
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #2d3748;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        z-index: 3000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 4px solid #38a169;
    }
    
    .notification-error {
        border-left: 4px solid #e53e3e;
    }
    
    .notification-warning {
        border-left: 4px solid #d69e2e;
    }
    
    .notification-info {
        border-left: 4px solid #3182ce;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: inherit;
        font-size: 1.25rem;
        cursor: pointer;
        padding: 0.25rem;
        border-radius: 0.25rem;
        opacity: 0.7;
        transition: opacity 0.2s ease;
        margin-left: auto;
    }
    
    .notification-close:hover {
        opacity: 1;
        background: rgba(255, 255, 255, 0.1);
    }
    
    .code-output {
        background: #1a202c;
        padding: 1rem;
        border-radius: 0.375rem;
        border: 1px solid #4a5568;
        font-family: 'Fira Code', monospace;
        white-space: pre-wrap;
        word-break: break-word;
        color: #e2e8f0;
    }
    
    .code-error {
        background: #742a2a;
        padding: 1rem;
        border-radius: 0.375rem;
        border: 1px solid #c53030;
        font-family: 'Fira Code', monospace;
        white-space: pre-wrap;
        word-break: break-word;
        color: #fed7d7;
    }
    
    .suggestion-item {
        background: #4a5568;
        padding: 0.75rem;
        border-radius: 0.375rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #63b3ed;
    }
    
    .suggestion-item i {
        color: #63b3ed;
        margin-right: 0.5rem;
    }
`;
document.head.appendChild(style);
