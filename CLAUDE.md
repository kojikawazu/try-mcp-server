# try-mcp-server

MCP（Model Context Protocol）サーバーを TypeScript/Node.js で自作して試すためのお試し用リポジトリ。実験は `experiments/` 配下に 1 実験 1 フォルダで置く。

開発ルールの唯一の正本は `.claude/rules/` です。Claude Code はこのファイルから、Codex は `AGENTS.md` から同じルールを参照します。ルール本文は各入口へ複製しません。

## Rules

明示的な指示がなくても、`.claude/rules/` 内のルールを常に守ってください。

| ファイル | スコープ | 内容 |
|---------|---------|------|
| shortcuts.md | 全体 | 指示ショートカット（PR出して、PR承認しました 等） |
| workflow.md | 全体 | 開発フロー（ブランチ運用・テスト必須） |
| quality-gate.md | 全体 | 品質ゲート（セルフレビュー・設計/実装レビュー） |
| documentation.md | 全体 | ドキュメント更新ルール |
| git.md | 全体 | GitHub Flow・ブランチ命名・push 禁止物 |
| github-issue.md | 全体 | GitHub issue 運用（ブランチと対で issue 作成・open/close 管理） |
| testing.md | 全体 | テスト分類・原則 |
| codex.md | 全体 | Codex 利用時の AGENTS.md・Claude 固有機能の読み替え・GitHub 操作ルール |
| lessons-learned.md | 全体 | 教訓の記録（docs/lessons-learned.md への追記トリガー・フォーマット） |
| pr-description.md | 全体 | PR 本文の必須セクション（変更種別ごと。バグ修正 / 仕様変更 / 仕様追加 / 新規開発 / ドキュメント） |
| static-analysis.md | 全体 | 静的解析の運用（markdownlint の設定とコマンドの正本・抑制の作法・`--fix` の扱い） |
