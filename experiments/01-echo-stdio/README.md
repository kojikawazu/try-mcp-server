# 01-echo-stdio

最初に作った最小構成の MCP サーバー。stdio で接続し、`echo` ツールと固定テキストのリソース `example://readme` を公開する。

以下のパスとコマンドは、このフォルダ（`experiments/01-echo-stdio/`）を起点とする。

## 構成

- `server/` MCP サーバー本体（`server/README.md`）
- `client/` 簡易クライアント（`client/README.md`）
- `docs/` この実験のドキュメント

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
