#!/bin/bash
# Startup script for the MCP server

# Navigate to the backend directory
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Start the MCP server
echo "Starting MCP Server..."
python -m uvicorn mcp_server.server:mcp_server_instance.app --host 0.0.0.0 --port 8080

echo "MCP Server stopped."