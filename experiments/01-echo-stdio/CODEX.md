# Codex Notes

このリポジトリは MCP サーバーを TypeScript/Node.js で試作するための実験用です。

## 構成

- `server/` MCP サーバー本体
- `client/` 簡易クライアント
- `docs/` ドキュメント

## 実行

```bash
cd server
npm install
npm run dev
```

## 動作確認（簡易クライアント）

```bash
cd server
npm run build
cd ../client
npm install
npm run dev
```

## 仕様（抜粋）

- 伝送方式: stdio
- SDK: @modelcontextprotocol/sdk
- ツール: echo
- リソース: example://readme
- デフォルトポート: 3005
