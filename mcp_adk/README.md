# MCP ADK Agent

This directory contains an example of an agent that utilizes the Model Content Protocol (MCP) to interact with external tools.

## Functionality

The agent (`stock_agent`) is designed to communicate with an MCP server. This server provides a set of tools that the agent can then use to fulfill user queries.

In the provided example, the `stock_agent` uses tools from an MCP server to fetch current stock prices for companies. This demonstrates how agents can leverage external capabilities exposed through the MCP.

The core idea is to separate tool implementation (managed by the MCP server) from the agent's logic, allowing for flexible and powerful tool usage.
