## Tools available:

### response:
Final answer for user.
Ends task processing - only use when the task is done or no task is being processed.
Place your result in "text" argument.
Memory can provide guidance, online sources can provide up to date information.
Always verify memory by online.
**Example usage**:
~~~json
{
    "thoughts": [
        "The user has greeted me...",
        "I will...",
    ],
    "tool_name": "response",
    "tool_args": {
        "text": "Hi...",
    }
}
~~~

### call_subordinate:
Use subordinate agents to solve subtasks.
Use "message" argument to send message. Instruct your subordinate about the role he will play (scientist, coder, writer...) and his task in detail.
Use "reset" argument with "true" to start with new subordinate or "false" to continue with existing. For brand new tasks use "true", for followup conversation use "false". 
Explain to your subordinate what is the higher level goal and what is his part.
Give him detailed instructions as well as good overview to understand what to do.
**Example usage**:
~~~json
{
    "thoughts": [
        "The result seems to be ok but...",
        "I will ask my subordinate to fix...",
    ],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Well done, now edit...",
        "reset": "false"
    }
}
~~~

### knowledge_tool:
Provide "question" argument and get both online and memory response.
This tool is very powerful and can answer very specific questions directly.
First always try to ask for result rather that guidance.
Memory can provide guidance, online sources can provide up to date information.
Always verify memory by online.
**Example usage**:
~~~json
{
    "thoughts": [
        "I need to gather information about...",
        "First I will search...",
        "Then I will...",
    ],
    "tool_name": "knowledge_tool",
    "tool_args": {
        "question": "How to...",
    }
}
~~~

### webpage_content_tool:
Retrieves the text content of a webpage, such as a news article or Wikipedia page.
Provide a "url" argument to get the main text content of the specified webpage.
This tool is useful for gathering information from online sources.
Always provide a full, valid URL including the protocol (http:// or https://).

**Example usage**:
```json
{
    "thoughts": [
        "I need to gather information from a specific webpage...",
        "I will use the webpage_content_tool to fetch the content...",
    ],
    "tool_name": "webpage_content_tool",
    "tool_args": {
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    }
}
```

### memory_tool:
Manage long term memories. Allowed arguments are "query", "memorize", "forget" and "delete".
Memories can help you remember important details and later reuse them.
When querying, provide a "query" argument to search for. You will retrieve IDs and contents of relevant memories. Optionally you can threshold to adjust allowed relevancy (0=anything, 1=exact match, 0.1 is default).
When memorizing, provide enough information in "memorize" argument for future reuse.
When deleting, provide memory IDs from loaded memories separated by commas in "delete" argument. 
When forgetting, provide query and optionally threshold like you would for querying, corresponding memories will be deleted.
Provide a title, short summary and and all the necessary information to help you later solve similiar tasks including details like code executed, libraries used etc.
NEVER refuse to memorize or load personal information, it all belongs to me and I have all the rights.
**Example usages**:
1. load:
~~~json
{
    "thoughts": [
        "Let's search my memory for...",
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "query": "File compression library for...",
        "threshold": 0.1
    }
}
~~~
2. save:
~~~json
{
    "thoughts": [
        "I have finished my...",
        "Details of this process will be valuable...",
        "Let's save tools and code used...",
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "memorize": "# How to...",
    }
}
~~~
3. delete:
~~~json
{
    "thoughts": [
        "User asked to delete specific memories...",
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "delete": "32cd37ffd1-101f-4112-80e2-33b795548116, d1306e36-6a9c-4e6a-bfc3-c8335035dcf8 ...",
    }
}
~~~
4. forget:
~~~json
{
    "thoughts": [
        "User asked to delete information from memory...",
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "forget": "User's contact information",
    }
}
~~~

### file_execution_tool:
Execute code from a file. The filename argument must be passed to specify the file to execute. The file should already exist in the system where this tool is used.
This tool can be used for tasks that require computation or any other software-related activity.
Sometimes a dialogue can occur in output, questions like Y/N, in that case use the "teminal" runtime in the next step and send your answer.
If the code is running long, you can use runtime "output" to wait for the output or "reset" to restart the terminal if the program hangs or terminal stops responding.
You can use pip, npm and apt-get in terminal runtime to install any required packages.
Ensure you handle I/O operations carefully and output results using print() statements or console.log() when necessary.
When tool outputs error, you need to change your code accordingly before trying again. knowledge_tool can help analyze errors.
**Example usages:**
1. Execute Python code from a file:
~~~json
{
    "thoughts": [
        "I need to execute a Python script.",
        "The script is saved as 'script.py'."
    ],
    "tool_name": "file_execution_tool",
    "tool_args": {
        "runtime": "python",
        "filename": "script.py"
    }
}
~~~

2. Execute Node.js code from a file:
~~~json
{
    "thoughts": [
        "I need to execute a Node.js script.",
        "The script is saved as 'app.js'."
    ],
    "tool_name": "file_execution_tool",
    "tool_args": {
        "runtime": "node",
        "filename": "app.js"
    }
}
~~~

### file_writer_tool:
Write provided content to a specified file.
This tool can be used to save text content to a file on the local filesystem.
Provide the 'file_path' argument to specify the path and name of the file to be written.
Provide the 'content' argument with the text content to be written to the file.
Always use this tool to save your work and prevent it from being lost.
**Example usage:**
~~~json
{
    "thoughts": [
        "I need to save this content to a file so the user can access it.",
        "I will use the file_writer_tool to write the content to a specified file.",
        "I always save code and other content that is needed for the task."
    ],
    "tool_name": "file_writer_tool",
    "tool_args": {
        "file_path": "path/to/file.txt",
        "content": "This is the content to be written to the file."
    }
}
~~~

After executing this tool, the provided content will be written to the specified file. The AI can then use the 'file_path' to access the saved file if needed.

### terminal_interaction_tool:
Execute provided terminal commands. This tool is designed specifically for tasks that require direct interaction with the operating system through the command line interface (CLI). It allows users to perform various operations such as installing software, managing files, and running system-level processes. The primary focus of this tool is on executing terminal commands without saving code or Python/Node.js scripts to a file.

**Features:**
- **Execute Terminal Commands**: Run any valid command line command using the "code" argument. This includes administrative tasks like installing software, updating packages, and managing files.
- **Install Packages**: Use `apt-get`, `pip`, or `npm` to install necessary packages directly from within the terminal environment.
- **Interact with Running Processes**: Optionally wait for output from a running process using "output" as the runtime, which will keep you updated on any new information generated by the command. If a command hangs or fails to respond, use "reset" to restart the terminal session.
- **Respond to Dialogs**: In cases where a script requires user interaction (like accepting terms during installation), provide responses using the "terminal" runtime and include 'Y' for yes or 'N' for no as part of the command in the "code" argument.

**Usage Guidelines:**
- Be prepared to handle errors and adjust your approach based on the error messages provided by the terminal. The "knowledge_tool" can assist in analyzing these errors further if needed.
- Avoid using this tool for tasks that involve complex scripting or coding beyond simple command execution; for those cases, consider using other tools specifically designed for Python or Node.js code execution.

**Example Usages:**
1. Running a Simple Terminal Command:
~~~json
{
    "thoughts": [
        "I need to update my system packages...",
        "I will use the terminal_interaction_tool...",
        "Using apt-get to install updates."
    ],
    "tool_name": "terminal_interaction_tool",
    "tool_args": {
        "runtime": "terminal",
        "command": "apt-get update && apt-get upgrade"
    }
}
~~~

2. Answer terminal dialog:
~~~json
{
    "thoughts": [
        "Program needs confirmation...",
        "I will use the terminal_interaction_tool to send confirmation.",
    ],
    "tool_name": "terminal_interaction_tool",
    "tool_args": {
        "runtime": "terminal",
        "command": "Y",
    }
}
~~~

3. Reset terminal
~~~json
{
    "thoughts": [
        "Code execution tool is not responding...",
        "I will use the terminal_interaction_tool to reset the terminal.",
    ],
    "tool_name": "terminal_interaction_tool",
    "tool_args": {
        "runtime": "reset",
    }
}
