# Running the RAG Engine with Python

The RAG Engine operates as a standalone executable that communicates via Standard I/O (stdin/stdout). This means you do not need to import any complex libraries to use it in Python; you simply spawn it as a subprocess.

## Example Code

Below is a complete, minimal example using Python's built-in `subprocess` module to spawn the engine, send a query, and read the response.

```python
import subprocess
import json
import threading

def run_rag_engine():
    # 1. Spawn the compiled RAG engine executable
    engine = subprocess.Popen(
        ['./rag_engine.exe'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,        # Use strings instead of bytes
        encoding='utf-8'
    )

    # Helper function to continuously read stderr logs
    def read_stderr():
        for line in engine.stderr:
            print(f"[ENGINE LOG] {line.strip()}")
            
    threading.Thread(target=read_stderr, daemon=True).start()

    # 2. Construct the request payload
    request_payload = {
        "action": "chat",
        "session_id": "example-session-id",
        "question": "Can you summarize the key points of the documents?",
        "rank": 5,
        "strictness": 2
    }

    # 3. Send the payload to the engine via Standard Input
    print("Sending question to RAG Engine...")
    engine.stdin.write(json.dumps(request_payload) + "\n")
    engine.stdin.flush()

    # 4. Listen for the response on Standard Output
    for line in engine.stdout:
        line = line.strip()
        if not line:
            continue
            
        try:
            response = json.loads(line)
            if "answer" in response:
                print("\n--- AI Response ---")
                print(response["answer"])
                print("-------------------")
                print(f"Sources Used: {response.get('sources_used', 0)}")
                break # Exit after receiving the answer
        except json.JSONDecodeError:
            # Some output lines might just be status messages
            print(f"[STATUS] {line}")

    # Terminate the engine when done
    engine.terminate()

if __name__ == "__main__":
    run_rag_engine()
```

## How it Works
1. **`subprocess.Popen`**: We launch `rag_engine.exe` with pipes attached to its standard inputs and outputs.
2. **`stdin.write()`**: We serialize our JSON object into a string, append a newline character `\n`, and flush the buffer to ensure the engine receives it immediately.
3. **Reading lines**: The engine outputs its final answer as a single line of JSON, which we parse and print.
