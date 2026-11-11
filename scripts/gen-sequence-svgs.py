"""MCP の通信の流れを示すアニメーション SVG（シーケンス図）を生成する。

生成物:
  docs/images/mcp-jsonrpc-stdio.svg     自作サーバー（01-echo-stdio）の JSON-RPC のやりとり
  docs/images/mcp-oauth-atlassian.svg   Atlassian MCP に OAuth で接続するまで

使い方（リポジトリのどこから実行してもよい）:
  python3 scripts/gen-sequence-svgs.py           生成して上書きする
  python3 scripts/gen-sequence-svgs.py --check   生成結果がコミット済みの SVG と一致するかを確かめる（不一致なら終了コード 1）

SVG は生成物であり、直接編集しない。手順・ラベル・色を変えるときは、このファイルの
SEQUENCES を直して再生成する（各行の keyframes と開始の遅延は手順の数から計算しているため、
SVG を手で直すと 1 行足しただけで全行の時間割を計算し直すことになる）。

方針:
- アニメーションは CSS（@keyframes）だけで書く。<script> と SMIL は使わない。
  README の <img> でもスクリプトなしで動き、prefers-reduced-motion で止められるため。
- 各メッセージは同じ周期で回り、animation-delay で自分の番だけ光る。
- ライト / ダークは prefers-color-scheme で切り替える。
- 依存は Python 標準ライブラリのみ（追加のインストールなしで実行できるようにする）。
"""

import sys
from html import escape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "docs" / "images"

FONT = "-apple-system, 'Segoe UI', 'Hiragino Sans', 'Noto Sans JP', sans-serif"
GENERATED_NOTE = "生成物: scripts/gen-sequence-svgs.py から生成している。直接編集しない"


def render(title, lifelines, messages, footnote, step_sec):
    """シーケンス図の SVG 文字列を返す。

    lifelines: [(key, 見出し 1 行目, 見出し 2 行目)]
    messages:  [(送信元 key, 送信先 key, ラベル, 種類)]  種類: req（要求）/ res（応答）/ note（通知）
    step_sec:  1 手あたりの秒数。周期は step_sec × 手数
    """
    n_life = len(lifelines)
    width = 960
    margin = 110
    span = (width - margin * 2) / (n_life - 1)
    xs = {k: margin + i * span for i, (k, _, _) in enumerate(lifelines)}

    head_y, head_h = 64, 48
    row0, row_gap = head_y + head_h + 46, 46
    n = len(messages)
    bottom = row0 + (n - 1) * row_gap + 40
    height = bottom + (44 if footnote else 16)
    cycle = step_sec * n
    slot = 100.0 / n
    travel = slot * 0.62  # 1 手の持ち時間のうち、パケットが移動する割合

    css = [
        f"svg {{ font-family: {FONT}; }}",
        # :root を併記すると単体の SVG では :root（詳細度 0,1,0）がダーク側の svg（0,0,1）に勝ち、
        # ダークに切り替わらない。両方とも svg 要素で書く
        "svg { --bg:#ffffff; --fg:#1a1a1a; --muted:#9ca3af; --box:#f3f4f6; --req:#2563eb; --res:#16a34a; --note:#7c3aed; }",
        "@media (prefers-color-scheme: dark) { svg { --bg:#0d1117; --fg:#e6edf3; --muted:#6e7681; --box:#161b22; --req:#58a6ff; --res:#3fb950; --note:#bc8cff; } }",
        ".bg { fill: var(--bg); }",
        ".title { fill: var(--fg); font-size: 17px; font-weight: 700; }",
        ".head rect { fill: var(--box); stroke: var(--fg); stroke-width: 1.2; }",
        ".head text { fill: var(--fg); font-size: 13px; text-anchor: middle; }",
        ".head .sub { fill: var(--muted); font-size: 11.5px; }",
        ".life { stroke: var(--muted); stroke-width: 1.2; stroke-dasharray: 4 5; }",
        ".row { opacity: .28; animation: hl %.3fs linear infinite; }" % cycle,
        ".row text { font-size: 13px; text-anchor: middle; }",
        # ライフラインを隠す下地。.row の中に入れると行と一緒に薄くなって透けるため、行の外に不透明で置く。
        # 文字のふちどり（stroke）は字形に沿うだけで単語間のすき間を覆えないため、幅を見積もった長方形にする
        ".halo { fill: var(--bg); }",
        ".req line { stroke: var(--req); } .req text { fill: var(--req); } .req .ah { fill: var(--req); }",
        ".res line { stroke: var(--res); } .res text { fill: var(--res); } .res .ah { fill: var(--res); }",
        ".note line { stroke: var(--note); stroke-dasharray: 6 4; } .note text { fill: var(--note); } .note .ah { fill: var(--note); }",
        ".row line { stroke-width: 1.8; }",
        ".pkt { opacity: 0; }",
        ".pkt.req { fill: var(--req); } .pkt.res { fill: var(--res); } .pkt.note { fill: var(--note); }",
        ".foot { fill: var(--muted); font-size: 11.5px; }",
        "@keyframes hl { 0%%, %.2f%% { opacity: 1; } %.2f%%, 100%% { opacity: .28; } }" % (slot * 0.98, slot * 1.05),
        "@media (prefers-reduced-motion: reduce) { .row { animation: none; opacity: 1; } .pkt { display: none; } }",
    ]

    body = [
        f'<rect class="bg" x="0" y="0" width="{width}" height="{height}"/>',
        f'<text class="title" x="24" y="34">{escape(title)}</text>',
    ]

    for k, l1, l2 in lifelines:
        x = xs[k]
        bw = 196
        body.append('<g class="head">')
        body.append(f'<rect x="{x - bw / 2:.1f}" y="{head_y}" width="{bw}" height="{head_h}" rx="8"/>')
        if l2:
            body.append(f'<text x="{x:.1f}" y="{head_y + 21}">{escape(l1)}</text>')
            body.append(f'<text class="sub" x="{x:.1f}" y="{head_y + 38}">{escape(l2)}</text>')
        else:
            body.append(f'<text x="{x:.1f}" y="{head_y + 29}">{escape(l1)}</text>')
        body.append("</g>")
        body.append(f'<line class="life" x1="{x:.1f}" y1="{head_y + head_h}" x2="{x:.1f}" y2="{bottom}"/>')

    for i, (src, dst, label, kind) in enumerate(messages):
        y = row0 + i * row_gap
        x1, x2 = xs[src], xs[dst]
        d = 1 if x2 > x1 else -1
        tip = x2 - d * 2
        base = tip - d * 10
        delay = i * step_sec
        text = f"{i + 1}. {label}"
        cx = (x1 + x2) / 2
        # 13px の文字幅の見積もり: 全角 ≒ 13px、半角 ≒ 7.4px（下地が足りなくならないよう多めに見る）
        est = sum(13.0 if ord(ch) > 0x2E7F else 7.4 for ch in text) + 10
        body.append(f'<rect class="halo" x="{cx - est / 2:.1f}" y="{y - 23}" width="{est:.1f}" height="19" rx="3"/>')
        body.append(f'<g class="row {kind}" style="animation-delay:{delay:.3f}s">')
        body.append(f'<line x1="{x1:.1f}" y1="{y}" x2="{base:.1f}" y2="{y}"/>')
        body.append(f'<path class="ah" d="M{tip:.1f},{y} L{base:.1f},{y - 5} L{base:.1f},{y + 5} Z"/>')
        body.append(f'<text x="{cx:.1f}" y="{y - 8}">{escape(text)}</text>')
        body.append("</g>")
        # パケット: 行ごとに移動量が違うため keyframes を行ごとに生成する
        name = f"mv{i}"
        dx = x2 - x1 - d * 8
        css.append(
            "@keyframes %s { 0%% { transform: translateX(0); opacity: 1; } %.2f%% { transform: translateX(%.1fpx); opacity: 1; } %.2f%%, 100%% { transform: translateX(%.1fpx); opacity: 0; } }"
            % (name, travel, dx, travel + 2, dx)
        )
        body.append(
            f'<circle class="pkt {kind}" cx="{x1:.1f}" cy="{y}" r="6" '
            f'style="animation: {name} {cycle:.3f}s linear {delay:.3f}s infinite"/>'
        )

    if footnote:
        body.append(f'<text class="foot" x="24" y="{height - 18}">{escape(footnote)}</text>')

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"<!-- {GENERATED_NOTE} -->\n"
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{escape(title)}">\n'
        f"<title>{escape(title)}</title>\n"
        "<style>\n" + "\n".join(css) + "\n</style>\n" + "\n".join(body) + "\n</svg>\n"
    )


SEQUENCES = {
    "mcp-jsonrpc-stdio.svg": dict(
        title="自作サーバー（01-echo-stdio）の JSON-RPC のやりとり（stdio）",
        lifelines=[("c", "client/cli.ts", "簡易クライアント"), ("s", "server（自作）", "StdioServerTransport")],
        messages=[
            ("c", "s", "initialize（protocolVersion / clientInfo）", "req"),
            ("s", "c", "result: capabilities（tools / resources）", "res"),
            ("c", "s", "notifications/initialized（応答なし）", "note"),
            ("c", "s", "tools/list", "req"),
            ("s", "c", "result: tools = [ echo ]", "res"),
            ("c", "s", 'tools/call  echo { text: "hello" }', "req"),
            ("s", "c", 'result: content = [ "hello" ]', "res"),
        ],
        footnote="青: リクエスト / 緑: 応答 / 紫の破線: 通知（応答を返さない）。stdio では 1 行 1 メッセージの JSON-RPC が標準入出力を流れる",
        step_sec=2.0,
    ),
    "mcp-oauth-atlassian.svg": dict(
        title="Atlassian MCP に OAuth で接続するまで（リモート HTTP）",
        lifelines=[
            ("c", "MCP クライアント", "Claude Code / Copilot CLI"),
            ("b", "ブラウザ", "利用者"),
            ("a", "認可サーバー", "Atlassian の OAuth"),
            ("m", "MCP サーバー", "mcp.atlassian.com/v2/mcp"),
        ],
        messages=[
            ("c", "m", "initialize（トークンなし）", "req"),
            ("m", "c", "401  WWW-Authenticate: resource_metadata=…", "res"),
            ("c", "m", "GET /.well-known/oauth-protected-resource", "req"),
            ("m", "c", "authorization_servers（認可サーバーの場所）", "res"),
            ("c", "b", "認可画面を開く（PKCE の code_challenge 付き）", "req"),
            ("b", "a", "利用者がログインして承認", "req"),
            ("a", "c", "認可コード（リダイレクトで戻る）", "res"),
            ("c", "a", "トークン要求（認可コード + code_verifier）", "req"),
            ("a", "c", "アクセストークン", "res"),
            ("c", "m", "initialize（Authorization: Bearer …）", "req"),
            ("m", "c", "200  接続完了 → tools/list …", "res"),
        ],
        footnote="1〜2 は curl で実際に確認した応答。3 以降は MCP 仕様（2025-06-18）の認可フロー。初回はクライアント登録（DCR）が入ることがある",
        step_sec=1.6,
    ),
}


def main(argv):
    check = "--check" in argv[1:]
    unknown = [a for a in argv[1:] if a != "--check"]
    if unknown:
        print(f"不明な引数: {' '.join(unknown)}", file=sys.stderr)
        return 2
    if not SEQUENCES:
        # 対象 0 件を成功扱いにしない
        print("生成対象が 0 件です", file=sys.stderr)
        return 1

    stale = []
    for name, spec in SEQUENCES.items():
        path = OUT_DIR / name
        svg = render(**spec)
        if check:
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current != svg:
                stale.append(name)
            print(f"{'NG' if current != svg else 'OK'}: docs/images/{name}")
        else:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            path.write_text(svg, encoding="utf-8")
            print(f"生成: docs/images/{name}")

    if stale:
        print(
            f"生成結果と一致しない SVG が {len(stale)} 件あります。"
            "SVG を直接編集した可能性があります。python3 scripts/gen-sequence-svgs.py で再生成してください",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
