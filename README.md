# RAG Engine SDK Kit

Welcome to the standalone **RAG Engine SDK Kit**. This kit provides a fully compiled, self-contained intelligent retrieval-augmented generation (RAG) engine. It is packaged as an executable that can be easily distributed and interacted with by front-end clients via standard I/O Streams.

## Table of Contents
1. [SDK Components](#sdk-components)
2. [Running the Engine](#running-the-engine)
3. [Prompt Customization](#prompt-customization)
4. [API Connectivity (StdIO)](#api-connectivity-stdio)
5. [Security & Key Management](#security--key-management)

---

## SDK Components
- **`rag_engine.exe`**: The core, compiled RAG Engine. Contains document ingestion pipelines, chunking logic, LLM routers, vector stores, and the standard I/O API interface.
- **`PromptEditor.exe`**: A lightweight standalone UI application used to interactively visualize and edit system prompts across various strictness levels.
- **`secure_config.enc`**: An encrypted container storing API keys for remote LLMs (OpenAI, Gemini, OpenRouter, etc.).
- **`prompts.json`**: Configurations that control the system prompts and instruction formatting dynamically.

---

## Running the Engine
The engine does not require Python or any dependencies to be installed on the target machine. It can be run directly from the command line or spawned as a child process by another application.

```bash
# Launch the RAG Engine manually (mostly for testing, usually spawned programmatically)
.\rag_engine.exe
```

---

## Prompt Customization
The system prompt used by the engine dynamically changes based on the configured strictness level (e.g., Ultra-Strict vs Creative). These prompts are managed in `prompts.json`.

To modify the prompts safely without making JSON syntax errors, simply launch the Prompt Editor:
```bash
.\PromptEditor.exe
```

---

## API Connectivity (StdIO)
The engine is designed to operate as a child process. It listens for JSON requests on Standard Input (`stdin`) and outputs JSON responses on Standard Output (`stdout`).

### Example Node.js Connection
```javascript
const { spawn } = require('child_process');

const engine = spawn('./rag_engine.exe');

// Send a chat request
engine.stdin.write(JSON.stringify({
  action: 'chat',
  session_id: '1234-abcd',
  question: 'What is the user skilled in?',
  rank: 5,
  strictness: 2
}) + '\n');

// Read the response
engine.stdout.on('data', (data) => {
  const result = JSON.parse(data.toString());
  console.log('AI Answer:', result.answer);
  console.log('Source Chunks Used:', result.sources);
});
```

### Supported API Commands
1. **Initialize Engine**: `{ "action": "init" }`
2. **Ingest Document**: `{ "action": "ingest", "file_path": "path/to/doc.pdf", "session_id": "1234-abcd" }`
3. **Chat**: `{ "action": "chat", "session_id": "1234-abcd", "question": "Explain this.", "rank": 5, "strictness": 3 }`

---

## Security & Key Management
Remote API keys are handled securely through `secure_config.enc`. The engine decrypts this file automatically at runtime (using the system's MAC address or a machine-specific key) so plaintext keys are never exposed in configuration files.

> **IMPORTANT**: Never push `secure_config.enc` to public repositories if it contains active credentials. Add it to your `.gitignore`.