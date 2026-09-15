# RAG Engine SDK Kit

Welcome to the standalone **RAG Engine SDK Kit**. This kit provides a fully compiled, self-contained intelligent retrieval-augmented generation (RAG) engine. It is packaged as an executable that can be easily distributed and interacted with by front-end clients or scripts via standard I/O Streams.

## Table of Contents
1. [SDK Components](#sdk-components)
2. [Running the Engine](#running-the-engine)
3. [FAISS Vectorstore and File Directory](#faiss-vectorstore-and-file-directory)
4. [Strictness Levels Explained](#strictness-levels-explained)
5. [Security & Key Management](#security--key-management)
6. [Language-Specific Integration Guides](#language-specific-integration-guides)

---

## SDK Components
- **`rag_engine.exe`**: The core, compiled RAG Engine. Contains document ingestion pipelines, chunking logic, LLM routers, vector stores, and the standard I/O API interface.
- **`PromptEditor.exe`**: A lightweight standalone UI application used to interactively visualize and edit system prompts across various strictness levels.
- **`secure_config.enc`**: An encrypted container storing API keys for remote LLMs (OpenAI, Gemini, OpenRouter, etc.).
- **`custom_apis.json`**: A template file for first-time users to supply custom API routes or keys if they choose not to use the encrypted configuration.
- **`prompts.json`**: Configurations that control the system prompts and instruction formatting dynamically.

---

## Running the Engine
The engine does not require Python, Node.js, C++, or any dependencies to be installed on the target machine. It can be run directly from the command line or spawned as a child process by your application.

```bash
# Launch the RAG Engine manually from your terminal
.\rag_engine.exe
```

---

## FAISS Vectorstore and File Directory
When you start the SDK for the first time, you might notice that there is no database or FAISS vectorstore folder. **This is completely normal.**

The engine manages its own file directory automatically. The first time you run an ingestion command (or the engine attempts to load an existing session), it will automatically generate a `vectorstore/sessions/<session_id>` directory within the same folder where `rag_engine.exe` is located. 

You do not need to manually create any folders—simply spawn the engine and send the initialization or ingestion payloads, and the engine handles the rest.

---

## Strictness Levels Explained
When interacting with the RAG engine via the `chat` action, you must specify a `strictness` level (1, 2, or 3). These levels instruct the engine on how creatively it should answer based on the retrieved documents.

- **Level 1 (Creative)**: The engine acts creatively and conversationally. It uses the retrieved documents as inspiration but is free to extrapolate, brainstorm, and bring in external knowledge.
- **Level 2 (Balanced / Hybrid)**: The standard mode. It balances factual grounding with natural conversation, aiming to be helpful while staying primarily within the bounds of the provided documents.
- **Level 3 (Ultra Strict)**: The engine acts as a rigid data extractor. It will only answer using facts explicitly stated in the source documents. If the answer is not in the documents, it will decline to answer.

---

## Security & Key Management
The engine requires API keys to connect to cloud LLMs (unless running entirely local models). You can configure your keys in two ways:

1. **`custom_apis.json` (Plaintext for Development)**: Use the provided `custom_apis.json` template in this folder to insert your keys and endpoint configurations. 
2. **`secure_config.enc` (Encrypted for Production)**: Remote API keys are handled securely through `secure_config.enc`. The engine decrypts this file automatically at runtime so plaintext keys are never exposed in configuration files. (Use the provided `PromptEditor.exe` to manage this file).

> **IMPORTANT**: Never push `secure_config.enc` or `custom_apis.json` to public repositories if they contain active credentials.

---

## Language-Specific Integration Guides

The engine listens for JSON requests on Standard Input (`stdin`) and outputs JSON responses on Standard Output (`stdout`).

To see complete, simple examples of how to connect to the engine in your preferred programming language, please refer to the following guides included in this SDK:

- **[Javascript / Node.js Guide](./run_with_javascript.md)**
- **[Python Guide](./run_with_python.md)**
- **[C++ Guide](./run_with_cpp.md)**