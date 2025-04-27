# PDF Chat

A powerful RAG (Retrieval-Augmented Generation) application that enables intelligent conversations with your PDF documents. Built with FastAPI, React, and powered by Cohere's language models.

## 📊 Overview

PDF Chat is a modern web application that allows users to upload PDF documents and have interactive, context-aware conversations about their content. The application uses advanced RAG techniques to provide accurate, document-based responses while maintaining complete user control over data.

## ⚡ Key Features

- **🔍 Intelligent Document Processing**
  - Upload and process PDF documents up to 40 pages (recommended 10-20 pages for optimal performance)
  - Automatic text extraction and semantic chunking
  - Vector storage using PostgreSQL for efficient retrieval

- **💬 Advanced Chat Capabilities**
  - Context-aware conversations about your documents
  - Powered by Cohere's state-of-the-art language models
  - Real-time responses with markdown support

- **🛠️ Technical Features**
  - FastAPI backend with async support
  - React frontend with TypeScript
  - TailwindCSS for responsive design
  - Vector similarity search using pgvector
  - Secure document storage and management

- **🔐 Data Control & Security**
  - Complete control over uploaded documents
  - Ability to view and manage stored files
  - Option to delete documents and their associated vectors
  - Local document processing and storage

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- PostgreSQL with pgvector extension

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file:
   ```
   DATABASE_URL=your_postgres_database_url
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## 🎯 Usage

1. **Upload Documents**
   - Navigate to the Upload page
   - Drag and drop or select your PDF file
   - Wait for processing confirmation

2. **Chat Interface**
   - Go to the Chat page
   - Ask questions about your documents
   - Receive context-aware responses

3. **Manage Documents**
   - View uploaded documents in My Files
   - Delete documents when no longer needed
   - Monitor vector storage usage

## ⚠️ Rate Limits

Currently, the application uses Cohere's free tier which has rate limitations. For optimal performance:
- Keep documents under 20 pages
- Allow processing time between uploads
- Consider upgrading to a paid API key for higher limits

## 🔧 Technical Architecture

- **Frontend**: React, TypeScript, TailwindCSS, Framer Motion
- **Backend**: FastAPI, Langchain, Cohere Embeddings
- **Database**: PostgreSQL with pgvector extension
- **File Processing**: PyMuPDF for PDF handling

## 🌟 Acknowledgments

- [Cohere](https://cohere.ai/) for providing the language models
- [Langchain](https://www.langchain.com/) for the RAG implementation
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend framework
