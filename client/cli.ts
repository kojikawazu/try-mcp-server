import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { fileURLToPath } from "node:url";
import path from "node:path";

const serverName = process.env.MCP_SERVER_NAME ?? "try-mcp-server";
const serverPort = process.env.MCP_SERVER_PORT ?? "3005";

const run = async () => {
  const client = new Client(
    {
      name: "try-mcp-client",
      version: "0.1.0",
    },
    {
      capabilities: {},
    }
  );

  const serverRoot = path.resolve(
    path.dirname(fileURLToPath(import.meta.url)),
    "..",
    "server"
  );
  const serverEntrypoint = path.join(serverRoot, "dist", "index.js");

  const transport = new StdioClientTransport({
    command: "node",
    args: [serverEntrypoint],
    cwd: serverRoot,
    env: {
      ...process.env,
      MCP_SERVER_NAME: serverName,
      MCP_SERVER_PORT: serverPort,
    },
  });

  await client.connect(transport);

  const tools = await client.listTools();
  const echoResult = await client.callTool({
    name: "echo",
    arguments: {
      text: "hello from client",
    },
  });

  const resource = await client.readResource({
    uri: "example://readme",
  });

  process.stdout.write("== tools ==\n");
  process.stdout.write(JSON.stringify(tools, null, 2) + "\n");
  process.stdout.write("== echo result ==\n");
  process.stdout.write(JSON.stringify(echoResult, null, 2) + "\n");
  process.stdout.write("== resource ==\n");
  process.stdout.write(JSON.stringify(resource, null, 2) + "\n");

  await transport.close();
};

run().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  process.stderr.write(`[client] error: ${message}\n`);
  process.exit(1);
});
