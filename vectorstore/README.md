# Vector Database & Sessions

This folder (`vectorstore/`) is automatically generated and managed by the RAG Engine. You do not need to manually configure it.

Below is an explanation of what each component does:

- **`index.faiss`**: This is the compiled Facebook AI Similarity Search (FAISS) vector index. It contains the numerical embeddings of all ingested documents, optimized for lightning-fast similarity lookups.
- **`metadata.json`**: This file maps the numerical vectors in `index.faiss` back to their original human-readable text chunks, source filenames, and page numbers.
- **`sessions/`**: This directory acts as the engine's memory. Every time you start a chat with a new `session_id`, a folder is created here.
  - Inside a session folder, you'll find `chat_history.json`, which securely logs the entire conversation history (questions, AI answers, and source citations) so the engine can maintain context over time.
  - You will also find a `pdfs/` directory which retains the specific documents ingested for that session context.

*(Note: The files currently in this directory are sanitized structural examples provided so you can immediately see how the system operates!)*
