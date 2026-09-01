# RAG Document Chatbot

A Retrieval-Augmented Generation (RAG) based document chatbot that allows users to upload documents and ask questions based on their content. The application retrieves relevant information from the uploaded document and uses a Large Language Model (LLM) to generate context-aware answers.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RavPraveen/rag-chatbot.git
```

### 2. Navigate to the Project Directory

```bash
cd rag-document-chatbot
```

### 3. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install all required Python packages using:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory of the project.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key.


## Running the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

After running the command, Streamlit will start a local server.

Open the URL displayed in your terminal, typically:

```text
http://localhost:8501
```

## Features

* Upload and process PDF documents
* Extract and split document text into manageable chunks
* Generate embeddings for document chunks
* Store and retrieve relevant document information using a vector database
* Ask questions about uploaded documents
* Generate context-aware answers using an LLM
* Display relevant source information
* Interactive user interface built with Streamlit

## System Architecture

The application follows a Retrieval-Augmented Generation (RAG) pipeline:

```text
Document Upload
       │
       ▼
Document Loader
       │
       ▼
Text Extraction
       │
       ▼
Text Chunking
       │
       ▼
Embedding Generation
       │
       ▼
Vector Store
       │
       ▼
User Question
       │
       ▼
Question Embedding
       │
       ▼
Relevant Document Retrieval
       │
       ▼
LLM
       │
       ▼
Generated Answer
```

## Project Structure

```text
rag-document-chatbot/
│
├── app.py                    # Streamlit application
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
│
├── src/
│   ├── document_loader.py    # Document loading and text extraction
│   ├── text_splitter.py      # Document chunking
│   ├── embeddings.py         # Embedding model
│   ├── vector_store.py       # Vector database operations
│   ├── llm.py                # LLM integration
│   └── rag_pipeline.py       # Main RAG pipeline
│
└── data/                     # Optional document storage
```

## Prerequisites

Before running the project, make sure you have:

* Python 3.10 or higher
* Git
* An API key for the selected LLM provider


## How to Use the Application

1. Launch the application using `streamlit run app.py`.
2. Upload a supported document.
3. Wait for the document to be processed.
4. Enter your question in the chat interface.
5. The system retrieves relevant document chunks.
6. The LLM generates an answer based on the retrieved context.
7. Continue asking questions about the uploaded document.

## How It Works

The application uses Retrieval-Augmented Generation (RAG) to answer questions based on uploaded documents.

### Step 1: Document Processing

The uploaded document is loaded and its text content is extracted.

### Step 2: Text Chunking

The extracted text is divided into smaller chunks, making the document easier to process and retrieve efficiently.

### Step 3: Embedding Generation

Each text chunk is converted into a numerical vector representation using an embedding model.

### Step 4: Vector Storage

The generated embeddings are stored in a vector database.

### Step 5: Query Processing

When a user asks a question, the question is also converted into an embedding.

### Step 6: Similarity Search

The system searches the vector database to identify document chunks that are most relevant to the user's question.

### Step 7: Answer Generation

The retrieved document context and the user's question are sent to the LLM, which generates a relevant answer.

## Technologies Used

* Python
* Streamlit
* Large Language Models (LLMs)
* Embedding Models
* Vector Database
* Retrieval-Augmented Generation (RAG)

## Future Improvements

Possible future enhancements include:

* Support for multiple document formats
* Multi-document querying
* Conversation memory
* Persistent vector storage
* Improved source citations
* Document summaries
* Improved chat history management
* Support for additional LLM providers

## Author

Praveen Samarasekara

Developed as a document-based question answering application using Retrieval-Augmented Generation (RAG).

