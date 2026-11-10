import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

type ServerConfig = {
  name: string;
};

const EXAMPLE_RESOURCE_URI = "example://readme";

export const createServer = (config: ServerConfig) => {
  const server = new Server(
    {
      name: config.name,
      version: "0.1.0",
    },
    {
      capabilities: {
        tools: {},
        resources: {},
      },
    }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: "echo",
          description: "入力文字列をそのまま返す",
          inputSchema: {
            type: "object",
            properties: {
              text: {
                type: "string",
                description: "返却する文字列",
              },
            },
            required: ["text"],
          },
        },
      ],
    };
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    if (request.params.name !== "echo") {
      throw new Error(`Unknown tool: ${request.params.name}`);
    }

    const text = request.params.arguments?.text;
    if (typeof text !== "string") {
      throw new Error("text is required and must be a string");
    }

    return {
      content: [
        {
          type: "text",
          text,
        },
      ],
    };
  });

  server.setRequestHandler(ListResourcesRequestSchema, async () => {
    return {
      resources: [
        {
          uri: EXAMPLE_RESOURCE_URI,
          name: "Example Readme",
          description: "固定テキストのサンプルリソース",
          mimeType: "text/plain",
        },
      ],
    };
  });

  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    if (request.params.uri !== EXAMPLE_RESOURCE_URI) {
      throw new Error(`Unknown resource: ${request.params.uri}`);
    }

    return {
      contents: [
        {
          uri: EXAMPLE_RESOURCE_URI,
          mimeType: "text/plain",
          text: "Hello from try-mcp-server. This is a sample resource.",
        },
      ],
    };
  });

  return server;
};

export const connectStdio = async (server: Server) => {
  const transport = new StdioServerTransport();
  await server.connect(transport);
};
