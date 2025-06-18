# ADK - Agent Development Kit

This repository contains examples of agents built using the Google ADK.

## Dependencies

The following dependencies are required to run the agents in this repository:

```
google-adk==1.2.1
yfinance==0.2.56
```

You can install these dependencies by running:

```bash
pip install -r requirements.txt
```

## Running the ADK Web UI

To run the ADK web UI for any of the agents, use the following command:

```bash
adk web ADK_agents/3-multi_agent/
```

After running the command, open your web browser and navigate to the localhost URL provided in the terminal (usually http://localhost:8000).

## Agent Examples

The example agents (1 through 6) are located in the `ADK_agents/` directory.

This repository includes the following examples of agents:

* **1-Basic Agent:** A simple agent that demonstrates the basic functionality of the ADK.
* **2-Tool Agent:** An agent that uses tools to perform actions.
* **3-Multi-Agent:** A system of multiple agents that have different funtionalities.s
* **4-Structured Output Agent:** An agent (`shortstory_writer`) that takes a user's request and writes a short story, outputting the result in a structured JSON format.
* **5-Sessions and Memory Agent:** An agent (`question_answering_agent`) that answers questions based on user preferences and can remember information across sessions.
* **6-Persistent Storage Agent:** An agent (`remainder_agent`) that manages user reminders (add, view, update, delete) and stores them persistently.

## Using Local Ollama Model in you Agent

To use a local Ollama model in your agent, follow these steps:

1. Import the LiteLlm wrapper using:
```python
from google.adk.models.lite_llm import LiteLlm
```

2. Use the LiteLlm wrapper in your agent's code:
```python
agent = Agent(
    name = "Your Agent Name",
    model = LiteLlm("ollama_chat/you_model_name")
)
```

You can get your model name by using "ollama list" in your terminal.

** Important **: 
 - If your agent is relying on tools, please make sure that you select a model with tool support from Ollama website. You can check if your model supports tools by using "ollama show <model_name>". "tools" should appear under capabilities.

 - If the model supports "thinking", it is better to disable it for quicker responses. To do that use "/no_think" or "/set nothink" at the beginning of the agent's Instruction.

Check **'ADK+MCP/ollama_adk.py'** for an example of using a local Ollama model in an agent.

