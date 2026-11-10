# try-mcp-server

MCP（Model Context Protocol）サーバーを TypeScript/Node.js で自作して試すためのお試し用リポジトリ。

## 概要

- MCP の伝送方式（stdio / Streamable HTTP など）・ツール・リソース・プロンプトなどを、小さな実験単位で試す
- 実験は `experiments/` 配下に **1 実験 1 フォルダ**（`NN-<テーマ>/`）で置き、それぞれが独立して動く
- 実験の一覧は [experiments/README.md](experiments/README.md) を参照

```text
.
├── CLAUDE.md / AGENTS.md   AI エージェント向けの入口
├── .claude/rules/          開発ルールの正本
├── docs/                   リポジトリ全体の仕様書（README.md が目次）
├── experiments/            MCP サーバーの実験（1 実験 1 フォルダ）
│   └── 01-echo-stdio/      最初に作った最小構成のサーバー（stdio / echo / 固定リソース）
└── scripts/                検査スクリプト（markdownlint / shellcheck / 秘匿ファイル検出）
```

## セットアップ

前提:

- Node.js（LTS 推奨）
- 検査スクリプトを動かす場合: `npx` が使えること、shellcheck 0.11.0 または Docker

各実験のセットアップ手順は、その実験フォルダの `README.md` に書く。

## 使い方

### 実験を動かす

```bash
cd experiments/01-echo-stdio/server
npm install
npm run build
npm run client   # 簡易クライアントから echo ツールと example://readme リソースを呼び出す
```

### 新しい実験を追加する

1. `experiments/NN-<テーマ>/` を作る（連番は既存の最大値 + 1）
2. その中に `README.md`（目的・実行手順・確認できること）とコードを置く
3. [experiments/README.md](experiments/README.md) の一覧に 1 行追加する

### 検査

```bash
./scripts/lint-docs.sh            # Markdown の検査（--fix で自動修正）
./scripts/lint-shell.sh           # シェルスクリプトの検査
./scripts/check-secret-files.sh   # 鍵・.env などの混入検出
```

## AI エージェント向けルール

開発ルールの正本は `.claude/rules/` です。Claude Code は `CLAUDE.md`、Codex は `AGENTS.md` からこのルールを参照します。ルール本文は各入口へ複製しません。
