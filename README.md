# Academic Question Answering System Using RAG

An AI-powered academic question-answering system built using
**Retrieval-Augmented Generation (RAG)**. The system retrieves relevant
information from academic documents and uses it as context to generate
accurate, document-grounded answers.

The current implementation uses **Operating Systems study material**
as the initial knowledge base.

---

## 📌 Project Overview

Students often need to search through large amounts of academic
material to find specific concepts, definitions, algorithms, and
answers.

This project aims to provide a conversational interface where students
can ask questions in natural language and receive answers based on
their academic study material.

Instead of relying only on the knowledge of an LLM, the system first
retrieves relevant information from the provided academic documents
and then uses that information to generate the final response.

### Core Approach

```text
Academic Documents
        ↓
   Document Loading
        ↓
    Text Splitting
        ↓
 Embedding Generation
        ↓
   Vector Database
        ↓
   Similarity Search
        ↓
 Relevant Context
        ↓
        LLM
        ↓
  Generated Answer


## 🏗️ Project Structure

```text
HCL_RAG_Project/
│
├── Academic-RAG/
│   ├── rag_V1.ipynb
│   └── OS_notes.pdf
│
├── Documentation/
│   ├── Academic_RAG_Project_Documentation.docx
│   └── Academic_RAG_SRS.pdf
│
├── .gitignore
└── README.md

## Project Status
Current Status: Prototype / Development
The current version implements the core RAG pipeline using academic
Operating Systems material. Future versions will focus on improving
retrieval quality, expanding the knowledge base, and developing a
scalable academic platform.