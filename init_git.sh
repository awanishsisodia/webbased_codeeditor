#!/bin/bash

# Git Repository Initialization Script for Python Code Editor
# This script helps set up a clean git repository

echo "🚀 Initializing Git Repository for Python Code Editor"
echo "===================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if this is already a git repository
if [ -d ".git" ]; then
    echo "⚠️  This directory is already a git repository."
    echo "💡 To reinitialize, remove .git folder first: rm -rf .git"
    exit 1
fi

# Initialize git repository
echo "📁 Initializing git repository..."
git init

# Add all files
echo "📝 Adding files to git..."
git add .

# Make initial commit
echo "💾 Making initial commit..."
git commit -m "Initial commit: Python Code Editor with Ollama integration

Features:
- Web-based Python code editor
- Ollama AI integration for code suggestions
- Safe Python code execution
- File management and workspace organization
- Error analysis with AI-powered fixes
- Modern responsive UI with CodeMirror"

# Set up git configuration
echo "⚙️  Setting up git configuration..."

# Configure line endings
git config core.autocrlf false
git config core.eol lf

# Configure user if not already set
if [ -z "$(git config user.name)" ]; then
    echo "👤 Please enter your git username:"
    read -r username
    git config user.name "$username"
fi

if [ -z "$(git config user.email)" ]; then
    echo "📧 Please enter your git email:"
    read -r email
    git config user.email "$email"
fi

# Show git status
echo ""
echo "📊 Git Repository Status:"
echo "========================="
git status

echo ""
echo "🎉 Git repository initialized successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Add remote origin: git remote add origin <your-repo-url>"
echo "2. Push to remote: git push -u origin main"
echo ""
echo "💡 Useful git commands:"
echo "   git status          - Check repository status"
echo "   git add .           - Stage all changes"
echo "   git commit -m 'msg' - Commit changes"
echo "   git log             - View commit history"
echo "   git branch          - List branches"
echo ""
echo "🔒 Your .gitignore is configured to exclude:"
echo "   - Environment files (.env)"
echo "   - Virtual environments (venv/)"
echo "   - Python cache files (__pycache__/)"
echo "   - IDE files (.vscode/, .idea/)"
echo "   - OS files (.DS_Store, Thumbs.db)"
echo "   - User workspace content (workspace/*)"
