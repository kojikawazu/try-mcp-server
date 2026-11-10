# システム設計 (MCP サーバー)

## 全体構成

- Node.js + TypeScript で MCP サーバーを実装する。
- 伝送方式は `stdio` を採用する。
- 最小構成でツール 1 件、リソース 1 件を提供する。

## ディレクトリ構成

```text
.
├── docs/
│   ├── 01-requirements.md
│   ├── 02-setup.md
│   ├── 03-spec.md
│   └── 04-system-design.md
├── src/
│   ├── index.ts
│   └── server.ts
├── package.json
├── tsconfig.json
└── README.md
```

## 主要コンポーネント

- `src/index.ts`
  - エントリポイント。
  - 環境変数を読み込み、サーバー初期化を行う。
- `src/server.ts`
  - MCP SDK を用いたサーバー実装。
  - ツール/リソースの登録。
  - stdio トランスポートの接続。

## データフロー

1) クライアントが stdio 経由でリクエストを送信する。
2) サーバーがツールまたはリソースの要求を解釈する。
3) `echo` ツールは入力をそのまま返す。
4) `example://readme` は固定テキストを返す。
5) 応答を stdio 経由で返却する。

## 設定

- `MCP_SERVER_NAME`（デフォルト: `try-mcp-server`）
- `MCP_SERVER_PORT`（デフォルト: `3005`）
  - stdio でも保持しておく（将来 HTTP へ切り替える可能性を考慮）。

## ロギング

- リクエスト受信、処理開始、処理完了を stdout に出力する。
- 例: `received`, `handled`, `error` の3分類程度を想定。
