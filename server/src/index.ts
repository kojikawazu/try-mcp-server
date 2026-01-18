import { createServer, connectStdio } from "./server.js";

const serverName = process.env.MCP_SERVER_NAME ?? "try-mcp-server";
const serverPort = process.env.MCP_SERVER_PORT ?? "3005";

const log = (message: string) => {
  process.stdout.write(`[mcp] ${message}\n`);
};

const main = async () => {
  log(`starting server: name=${serverName} port=${serverPort}`);

  const server = createServer({ name: serverName });
  await connectStdio(server);

  log("server connected via stdio");
};

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  process.stderr.write(`[mcp] error: ${message}\n`);
  process.exit(1);
});
