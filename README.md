# try-mcp-server

MCP サーバーを TypeScript/Node.js で自作するための実験用リポジトリ。

## 構成
- `server/` MCP サーバー本体（`server/README.md`）
- `client/` 簡易クライアント（`client/README.md`）
- `docs/` ドキュメント

## ドキュメント
- `docs/01-requirements.md` 要件定義
- `docs/02-setup.md` セットアップ手順
- `docs/03-spec.md` 仕様決定
- `docs/04-system-design.md` システム設計

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
