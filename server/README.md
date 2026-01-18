# try-mcp-server

TypeScript/Node.js で最小構成の MCP サーバーを自作するための実験用リポジトリ。

## ドキュメント
- `../docs/01-requirements.md` 要件定義
- `../docs/02-setup.md` セットアップ手順
- `../docs/03-spec.md` 仕様決定
- `../docs/04-system-design.md` システム設計

## 状態
- 仕様と設計は確定済み
- 最小実装の雛形まで作成済み

## 実行
```bash
cd server
npm install
npm run dev
```

## 動作確認（概要）
- MCP クライアントから `echo` ツールを呼び出し、入力がそのまま返ることを確認する
- `example://readme` リソースを読み取り、固定テキストが返ることを確認する
- `MCP_SERVER_NAME` と `MCP_SERVER_PORT` は必要に応じて設定する（デフォルトは `try-mcp-server` / `3005`）

## 動作確認（簡易クライアント）
```bash
cd server
npm run build
npm run client
```
