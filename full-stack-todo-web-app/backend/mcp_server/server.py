import asyncio
from typing import Dict, Any, List
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.routing import Route
import uvicorn
import mcp.types as types

class MCPServer:
    def __init__(self):
        self.server = Server("todo-chatbot-mcp")
        self.transport = SseServerTransport("/messages")
        self.app = FastAPI(title="MCP Task Server")
        self.tools = {}
        self._setup_mcp_handlers()
        self._setup_routes()

        # Register tools on startup
        @self.app.on_event("startup")
        async def startup_event():
            from mcp_server.tools.task_operations import register_task_operation_tools
            await register_task_operation_tools()
            print(f"MCP Tools registered successfully: {list(self.tools.keys())}")

    def _setup_mcp_handlers(self):
        """Setup MCP protocol handlers"""
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name=name,
                    description=tool_data["description"],
                    inputSchema=tool_data["parameters"]
                )
                for name, tool_data in self.tools.items()
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            if name not in self.tools:
                raise ValueError(f"Unknown tool: {name}")
            
            tool_func = self.tools[name]["func"]
            try:
                result = await tool_func(**(arguments or {}))
                return [types.TextContent(type="text", text=str(result))]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    def _setup_routes(self):
        """Setup FastAPI routes for SSE"""
        @self.app.get("/sse")
        async def sse(request: Request):
            async with self.transport.connect_sse(request.scope, request.receive, request._send) as streams:
                await self.server.run(
                    streams[0],
                    streams[1],
                    self.server.create_initialization_options()
                )

        self.app.mount("/messages", self.transport.handle_post_message)

    def register_tool(self, name: str, description: str, parameters: Dict[str, Any]):
        """Decorator to register MCP tools"""
        def decorator(func):
            self.tools[name] = {
                "func": func,
                "description": description,
                "parameters": parameters
            }
            return func
        return decorator
    
    def run(self, host: str = "localhost", port: int = 8080):
        """Start the FastAPI server holding the MCP server"""
        print(f"MCP Server (SSE) starting on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


# Global server instance
mcp_server_instance = MCPServer()


def get_mcp_server():
    """Get the global MCP server instance"""
    return mcp_server_instance


if __name__ == "__main__":
    mcp_server_instance.run(port=8080)