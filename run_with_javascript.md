# Running the RAG Engine with JavaScript (Node.js)

The RAG Engine operates as a standalone executable that you can communicate with via Standard I/O (stdin/stdout). This makes it extremely easy to use in Node.js applications by simply spawning it as a child process.

## Example Code

Below is a complete, minimal example using Node.js to spawn the engine and request an AI answer.

```javascript
const { spawn } = require('child_process');
const readline = require('readline');

// 1. Spawn the compiled RAG engine executable
const engine = spawn('./rag_engine.exe');

// 2. Set up a readline interface to parse responses line-by-line
const rl = readline.createInterface({
  input: engine.stdout,
  terminal: false
});

// 3. Listen for responses from the engine
rl.on('line', (line) => {
  try {
    const response = JSON.parse(line);
    
    // Print the AI's answer
    if (response.answer) {
      console.log('--- AI Response ---');
      console.log(response.answer);
      console.log('-------------------');
      console.log(`Sources Used: ${response.sources_used}`);
    } else {
      console.log('Engine Output:', response);
    }
  } catch (err) {
    // Some lines might just be standard engine logs/warnings
    console.log('[LOG]:', line);
  }
});

// Handle errors
engine.stderr.on('data', (data) => {
  console.error(`[ERROR]: ${data}`);
});

// 4. Send a Chat Request payload to the engine via Standard Input
const requestPayload = {
  action: "chat",
  session_id: "example-session-id",
  question: "Can you summarize the key points of the documents?",
  rank: 5,
  strictness: 2
};

console.log("Sending question to RAG Engine...");
engine.stdin.write(JSON.stringify(requestPayload) + '\n');
```

## How it Works
1. **`spawn`**: We launch the `rag_engine.exe` process.
2. **`readline`**: We attach a line reader to standard output, because the engine outputs JSON objects on a single line when responding.
3. **`stdin.write`**: We send our request payload as a stringified JSON object, followed by a newline (`\n`), which triggers the engine to process the request.
