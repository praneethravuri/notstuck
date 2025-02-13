[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15.1.6-blue.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-blue.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green.svg)](https://www.mongodb.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-orange.svg)](https://www.pinecone.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-9cf.svg)](https://openai.com/)
[![Docker](https://img.shields.io/badge/Docker-20.10.17-blue.svg)](https://www.docker.com/)
![CI/CD](https://github.com/praneethravuri/notstuck/actions/workflows/ci-cd.yml/badge.svg)
![Fly.io](https://github.com/praneethravuri/notstuck/actions/workflows/fly.yml/badge.svg)

# NotStuck - AI-Powered Knowledge Base Assistant

## Project Description
NotStuck is an AI-powered knowledge base assistant that allows users to upload documents, ask questions, and get intelligent, context-aware answers. The system uses advanced natural language processing (NLP) techniques, including document chunking, embeddings, and retrieval-augmented generation (RAG), to provide accurate and relevant responses. The project is built with a modern tech stack, including FastAPI for the backend, Next.js for the frontend, and MongoDB and Pinecone for data storage and retrieval.

## Table of Contents
1. [Project Description](#project-description)
2. [Architecture](#architecture)
3. [Installation and Setup](#installation-and-setup)
4. [Usage](#usage)
5. [Badges](#badges)

## Architecture
NotStuck is built with a modular architecture, consisting of the following components:

### Backend
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **MongoDB**: A NoSQL database used to store chat sessions and metadata.
- **Pinecone**: A vector database used to store document embeddings for efficient similarity search.
- **OpenAI Embeddings**: Used to generate embeddings for document chunks and user queries.
- **LangChain**: A framework for working with language models, used for document chunking and processing.

### Frontend
- **Next.js**: A React framework for building server-rendered and static web applications.
- **Tailwind CSS**: A utility-first CSS framework for rapidly building custom user interfaces.
- **Shadcn UI**: A collection of reusable UI components built with Radix UI and Tailwind CSS.

### Workflow
1. **Document Upload**: Users upload documents (currently supports only PDFs) through the frontend. The backend processes these documents and splits them into chunks.
2. **Embedding Generation**: Each document chunk is embedded using OpenAI's embedding model and stored in Pinecone.
3. **Query Processing**: When a user asks a question, the query is embedded, and the most relevant document chunks are retrieved from Pinecone.
4. **Response Generation**: The retrieved chunks are used as context for generating a response using OpenAI's GPT model.

## Installation and Setup

### Prerequisites
- Python 3.10+
- Node.js 20+
- Docker and Docker Compose
- MongoDB
- Pinecone API Key
- OpenAI API Key

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/notstuck.git
   cd notstuck/backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   Create a `.env` file in the `backend` directory with the following content:
   ```env
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENV=your_pinecone_environment
   OPENAI_API_KEY=your_openai_api_key
   MONGODB_URI=mongodb://myuser:mypassword@localhost:27017/notstuck
   ```
4. Run the backend using Docker:
   ```bash
   docker-compose up --build
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables:
   Create a `.env` file in the `frontend` directory with the following content:
   ```env
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   ```
4. Run the frontend:
   ```bash
   npm run dev
   ```

## Usage
1. **Upload Documents**: Use the "Upload Documents" section in the sidebar to drag and drop files or click to select files from your computer. The system will process and embed your documents automatically.
2. **Ask Questions**: Enter your question in the chat input and press "Send". The system will retrieve relevant information from the uploaded documents and generate a response.
3. **View Active Sources:**: Active sources and relevant document chunks are displayed alongside the chat, giving you insights into which parts of your documents are being referenced.
4. **Adjust Settings**: Use the settings panel to adjust parameters such as similarity threshold, response style, and model temperature.


---

NotStuck is designed to help users quickly find information within their documents using AI. Whether you're a researcher, student, or professional, NotStuck can help you get unstuck with intelligent, context-aware answers.