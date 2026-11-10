# セットアップ手順 (TypeScript/Node.js)

## 前提

- Node.js がインストールされていること（LTS 推奨）。
- 作業ディレクトリ: `try-mcp-server`

## 初期化

1) `server/` に移動する。
2) `package.json` を作成する。
3) TypeScript と最低限の開発依存を追加する。

## 依存関係

- MCP SDK は `@modelcontextprotocol/sdk` を採用する。
- 依存関係は最小限に留める。

## 実行

- `MCP_SERVER_NAME` と `MCP_SERVER_PORT` を設定して起動する。
- デフォルトのポートは `3005`。

## 例（想定コマンド）

```bash
cd server
export MCP_SERVER_NAME=try-mcp-server
export MCP_SERVER_PORT=3005
npm install
npm run dev
```

## 簡易クライアントでの動作確認

- `dist/` が必要なため、事前にビルドする。
- `client/` の簡易クライアントが stdio でサーバーを起動し、`echo` と `example://readme` を確認する。

```bash
cd server
npm run build
cd ../client
npm install
npm run dev
```

## 確認

- MCP クライアントからツール/リソースにアクセスできることを確認する。
