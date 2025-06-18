# Agent Examples

This repository contains examples of agents built using the Google ADK.

## Running the ADK Web UI

To run the ADK web UI for any of the agents, use the following command:

```bash
adk web multi_agent/
```

After running the command, open your web browser and navigate to the localhost URL provided in the terminal (usually http://localhost:8000).

## Agent Examples

This repository includes the following examples of agents:

* **1-Basic Agent:** A simple agent that demonstrates the basic functionality of the ADK.
* **2-Tool Agent:** An agent that uses tools to perform actions.
* **3-Multi-Agent:** A system of multiple agents that have different funtionalities.
* **4-Structured Output Agent:** An agent (`shortstory_writer`) that takes a user's request and writes a short story, outputting the result in a structured JSON format.
* **5-Sessions and Memory Agent:** An agent (`question_answering_agent`) that answers questions based on user preferences and can remember information across sessions.
* **6-Persistent Storage Agent:** An agent (`remainder_agent`) that manages user reminders (add, view, update, delete) and stores them persistently.

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
