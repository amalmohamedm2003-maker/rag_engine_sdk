# Running the RAG Engine with C++

The RAG Engine operates as a standalone executable that communicates via Standard I/O (stdin/stdout). To keep things conceptually simple without relying on third-party libraries, we can interact with it using native OS pipes. 

Below is an example using the standard Windows API (`CreateProcess`) to spawn the engine, write a JSON string to its input stream, and read the response.

## Example Code

```cpp
#include <iostream>
#include <windows.h>
#include <string>

int main() {
    HANDLE hChildStdInRead, hChildStdInWrite;
    HANDLE hChildStdOutRead, hChildStdOutWrite;

    SECURITY_ATTRIBUTES saAttr;
    saAttr.nLength = sizeof(SECURITY_ATTRIBUTES);
    saAttr.bInheritHandle = TRUE;
    saAttr.lpSecurityDescriptor = NULL;

    // Create a pipe for the child process's STDOUT
    if (!CreatePipe(&hChildStdOutRead, &hChildStdOutWrite, &saAttr, 0)) {
        std::cerr << "Stdout pipe creation failed\n";
        return 1;
    }
    SetHandleInformation(hChildStdOutRead, HANDLE_FLAG_INHERIT, 0);

    // Create a pipe for the child process's STDIN
    if (!CreatePipe(&hChildStdInRead, &hChildStdInWrite, &saAttr, 0)) {
        std::cerr << "Stdin pipe creation failed\n";
        return 1;
    }
    SetHandleInformation(hChildStdInWrite, HANDLE_FLAG_INHERIT, 0);

    // Set up process startup info
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(STARTUPINFOA));
    si.cb = sizeof(STARTUPINFOA);
    si.hStdError = hChildStdOutWrite;
    si.hStdOutput = hChildStdOutWrite;
    si.hStdInput = hChildStdInRead;
    si.dwFlags |= STARTF_USESTDHANDLES;
    ZeroMemory(&pi, sizeof(PROCESS_INFORMATION));

    // Spawn the RAG engine
    char cmd[] = "rag_engine.exe";
    if (!CreateProcessA(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi)) {
        std::cerr << "CreateProcess failed\n";
        return 1;
    }

    // Close handles to the write end of the stdout pipe and read end of the stdin pipe
    // (these are used by the child, not the parent)
    CloseHandle(hChildStdOutWrite);
    CloseHandle(hChildStdInRead);

    // 1. Prepare our JSON payload as a raw string
    std::string requestPayload = 
        "{\"action\": \"chat\", \"session_id\": \"example-session\", \"question\": \"Summarize the document.\", \"rank\": 5, \"strictness\": 2}\n";

    // 2. Write to the engine's Standard Input
    DWORD written;
    std::cout << "Sending question to RAG Engine...\n";
    WriteFile(hChildStdInWrite, requestPayload.c_str(), requestPayload.size(), &written, NULL);
    
    // Close the stdin write handle so the child knows we're done writing
    CloseHandle(hChildStdInWrite);

    // 3. Read the engine's Standard Output
    DWORD read;
    char buffer[4096];
    std::string response = "";

    while (ReadFile(hChildStdOutRead, buffer, sizeof(buffer) - 1, &read, NULL) && read != 0) {
        buffer[read] = '\0';
        response += buffer;
        
        // Simple string check to see if we received the final JSON block
        if (response.find("\"answer\":") != std::string::npos) {
            break;
        }
    }

    std::cout << "\n--- Engine Output ---\n";
    std::cout << response << "\n";
    std::cout << "---------------------\n";

    // Cleanup
    CloseHandle(hChildStdOutRead);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}
```

## How it Works
1. **Pipes**: We use `CreatePipe` to create two one-way communication channels (one to send data in, one to receive data out).
2. **`CreateProcess`**: We spawn the compiled `rag_engine.exe` executable, injecting our pipes into its Standard Input and Output channels.
3. **`WriteFile`**: We send our raw JSON string into the input pipe. Note that it **must** end with a newline character (`\n`) for the engine to register the command.
4. **`ReadFile`**: We listen on the output pipe for the engine's response. The engine streams logs and eventually outputs the final JSON result containing the `answer` key.
