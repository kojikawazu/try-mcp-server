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
├── .mcp.json               MCP クライアント（Claude Code / Copilot CLI）向けのサーバー設定（Playwright / Atlassian）
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

### MCP クライアントから既製のサーバーを使う

リポジトリ直下の `.mcp.json` に、既製の MCP サーバーを登録している。

| 名前 | サーバー | 方式 | 認証 |
|---|---|---|---|
| `playwright` | [Playwright MCP](https://github.com/microsoft/playwright-mcp)（`@playwright/mcp`、版固定） | stdio（手元で `npx` が起動する） | 不要 |
| `atlassian` | [Atlassian Rovo MCP Server](https://support.atlassian.com/atlassian-rovo-mcp-server/)（Jira / Confluence） | リモート HTTP（`https://mcp.atlassian.com/v2/mcp`） | OAuth（クライアントごとにブラウザでログインする） |

同じファイルを次の 2 つのクライアントが読む（`<名前>` は上の表の名前）。

| クライアント | `.mcp.json` の扱い | 確認コマンド | OAuth のログイン |
|---|---|---|---|
| Claude Code | project スコープ。初回は使用の承認を求められる。承認後は、同名のサーバーがユーザー設定にあってもこのリポジトリ内では `.mcp.json` 側が優先される（**承認前はユーザー設定側が使われる**） | `claude mcp get <名前>`（`Scope: Project config` と表示される）。Claude Code 内では `/mcp` | Claude Code 内で `/mcp` → サーバーを選んで認証 |
| GitHub Copilot CLI | Workspace 設定。初回はフォルダの信頼を求められる（信頼していないフォルダでは読み飛ばされる） | `copilot mcp get <名前>`（`Source: Workspace` と表示される） | 初回の利用時に案内が出る。やり直しは Copilot CLI 内で `/mcp auth <名前>` |

- **リポジトリに認証情報を書かない。** リモートのサーバーは OAuth でログインし、トークンは各クライアントが利用者ごとに保持する。`.mcp.json` には URL だけを書く。ログインは Claude Code と Copilot CLI で共有されないため、それぞれで行う。
- Playwright MCP の版を上げるときは `.mcp.json` の `@playwright/mcp@<版>` を書き換える。`@latest` にすると起動のたびに版が変わり、挙動が再現しなくなるため使わない。
- Playwright MCP のスナップショットやスクリーンショットは `.playwright-mcp/` に出力される（`.gitignore` 済み）。
- Claude Code で claude.ai の Atlassian コネクタも有効にしている場合、Claude Code はコネクタと `.mcp.json` のサーバーを **URL で同一か判定する**。コネクタが廃止予定の V1（`/v1/mcp`）のままだと別のサーバーとして両方が起動し、同じツールが 2 組並ぶ。コネクタを V2 で接続し直すと、このリポジトリでは `.mcp.json` 側だけが使われる。
- Copilot CLI で実行するには、GitHub の Copilot 設定（<https://github.com/settings/copilot>）で MCP サーバーの利用が許可されている必要がある。許可されていないと、設定は読まれても `Third-party MCP servers are disabled by your organization's Copilot policy` で実行が拒否される。
- Codex は `.mcp.json` を読まない（設定の形式が別）。

### 検査

```bash
./scripts/lint-docs.sh            # Markdown の検査（--fix で自動修正）
./scripts/lint-shell.sh           # シェルスクリプトの検査
./scripts/check-secret-files.sh   # 鍵・.env などの混入検出
```

## AI エージェント向けルール

開発ルールの正本は `.claude/rules/` です。Claude Code は `CLAUDE.md`、Codex は `AGENTS.md` からこのルールを参照します。ルール本文は各入口へ複製しません。
