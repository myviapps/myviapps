"""Generate the SVG artwork for the GitHub profile README.

Run:  python build.py      (writes ./assets/*.svg)

GitHub strips CSS from READMEs, so every designed element is an SVG image.
Sizes are in real pixels: the README column is ~846px wide, cards sit on a
412px module so two fit per row on desktop and wrap to one on a phone.
Only system fonts are used; GitHub blocks web fonts inside SVG images.
"""
import os
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Palette and type, taken from the portfolio site (src/story.css).
BG, CARD, BR = "#0a0a0a", "#141412", "#24231f"
FG, SOFT, MUTED = "#f2f0eb", "#c9c6bf", "#8d8a83"
ACC, ACC_LIT, DOT_OFF, PILL_BR = "#ff7a3d", "#ffd2b8", "#262522", "#3a3834"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
MONO_W = 0.62  # monospace advance per em, rounded up so chips never clip

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(w, h, body, style="", label=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(label)}">\n<style>{style}{REDUCED}</style>\n{body}\n</svg>\n'
    )


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def chips(items, x0, y0, max_w, size=10, h=22, pad=8, gap=6, row_gap=8):
    """Lay out monospace chips left to right, wrapping at max_w. Returns (svg, rows)."""
    out, x, y, rows = [], x0, y0, 1
    for label in items:
        w = round(len(label) * size * MONO_W + pad * 2)
        if x + w > x0 + max_w:
            x, y, rows = x0, y + h + row_gap, rows + 1
        out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="none" stroke="{PILL_BR}"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + size * 0.36}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="{size}" fill="{SOFT}">{esc(label)}</text>'
        )
        x += w + gap
    return "\n".join(out), rows


# ── Header ───────────────────────────────────────────────────────────────────
def header():
    w, h = 828, 320
    cols, rows, pitch, r = 25, 20, 11, 2.8
    gx, gy = w - 40 - (cols - 1) * pitch, 50
    dots = []
    for c in range(cols):
        col = "".join(
            f'<circle cx="{gx + c * pitch}" cy="{gy + rw * pitch}" r="{r}" fill="{ACC}"/>' for rw in range(rows)
        )
        anim = f'<animate attributeName="opacity" values="0.55;1;0.55" dur="3.6s" begin="{c * 0.12:.2f}s" repeatCount="indefinite"/>'
        dots.append(f'<g class="col" style="animation-delay:{c * 0.12:.2f}s">{anim}{col}</g>')
    last_x, last_y = gx + (cols - 1) * pitch, gy + (rows - 1) * pitch
    style = (
        f".col{{fill:{ACC};animation:wave 3.6s ease-in-out infinite}}"
        f"@keyframes wave{{0%,100%{{fill:{ACC};opacity:.6}}50%{{fill:{ACC_LIT};opacity:1}}}}"
        f".now{{animation:pulse 2.4s ease-in-out infinite}}"
        f"@keyframes pulse{{50%{{opacity:.25}}}}"
    )
    body = f"""<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{BG}" stroke="{BR}"/>
<circle class="now" cx="44" cy="50" r="4" fill="{ACC}"/>
<text x="58" y="54" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="{SOFT}">OPEN TO FORWARD DEPLOYED ENGINEER ROLES</text>
<text x="38" y="132" font-family="{SERIF}" font-size="58" fill="{FG}">Vijay Sundar</text>
<text x="38" y="194" font-family="{SERIF}" font-size="58" font-style="italic" fill="{ACC}">Nagamalla.</text>
<text x="40" y="236" font-family="{SANS}" font-size="15" fill="{SOFT}">Eight years teaching 50,000+ learners to code.</text>
<text x="40" y="258" font-family="{SANS}" font-size="15" fill="{FG}">Now I build the software I used to teach about.</text>
<text x="40" y="294" font-family="{MONO}" font-size="10.5" letter-spacing="1.2" fill="{MUTED}">AI SOLUTIONS  /  FULL-STACK  /  TECHNICAL ENABLEMENT</text>
{''.join(dots)}
<circle cx="{last_x}" cy="{last_y}" r="{r + 1}" fill="{BG}"/>
<circle class="now" cx="{last_x}" cy="{last_y}" r="{r + 1}" fill="{ACC_LIT}"/>
<text x="{w - 40}" y="294" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="1.2" fill="{ACC}">50,000 LEARNERS <tspan fill="{MUTED}">· 1 DOT = 100</tspan></text>"""
    write("header.svg", svg(w, h, body, style, "Vijay Sundar Nagamalla. Open to Forward Deployed Engineer roles. 50,000 learners trained."))


# ── Buttons ──────────────────────────────────────────────────────────────────
def buttons():
    for name, label, primary in [
        ("btn-resume", "Résumé (PDF)", True),
        ("btn-portfolio", "Portfolio", False),
        ("btn-linkedin", "LinkedIn", False),
        ("btn-call", "Book a call", False),
        ("btn-email", "Email", False),
    ]:
        w, h = 160, 40
        fill, stroke, color = (ACC, ACC, BG) if primary else (CARD, PILL_BR, FG)
        body = (
            f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="19.5" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{w / 2}" y="25" text-anchor="middle" font-family="{SANS}" font-size="13" '
            f'font-weight="600" fill="{color}">{esc(label)}</text>'
        )
        write(f"{name}.svg", svg(w, h, body, label=label))


# ── Chapter headings (sit on the page background, so light and dark variants) ─
def chapters():
    themes = {
        "light": dict(title="#1f2328", sub="#59636e", rule="#d1d9e0", acc="#c2410c"),
        "dark": dict(title=FG, sub=MUTED, rule="#30363d", acc=ACC),
    }
    for n, title, sub in [
        ("01", "Teach", "where it started"),
        ("02", "Build", "six applications, end to end"),
        ("03", "Stack", "what I reach for"),
        ("04", "Connect", "let's talk"),
    ]:
        for theme, c in themes.items():
            w, h = 828, 76
            body = f"""<text x="2" y="16" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="{c['acc']}">CHAPTER {n}</text>
<text x="0" y="56" font-family="{SERIF}" font-size="36" fill="{c['title']}">{title}<tspan fill="{c['acc']}">.</tspan><tspan dx="12" font-size="22" font-style="italic" fill="{c['sub']}">{esc(sub)}</tspan></text>
<rect x="0" y="74" width="{w}" height="1" fill="{c['rule']}"/>"""
            write(f"ch-{n}-{theme}.svg", svg(w, h, body, label=f"Chapter {n}: {title}"))


# ── Stat tiles ───────────────────────────────────────────────────────────────
def stats():
    for i, (num, plus, label) in enumerate(
        [("50K", "+", "LEARNERS TRAINED"), ("40", "+", "INSTITUTIONS"),
         ("6", "", "APPLICATIONS BUILT"), ("8", "+", "YEARS TEACHING")], 1
    ):
        w, h = 204, 112
        body = f"""<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{CARD}" stroke="{BR}"/>
<text x="20" y="64" font-family="{SERIF}" font-size="46" fill="{FG}">{num}<tspan fill="{ACC}">{plus}</tspan></text>
<text x="21" y="90" font-family="{MONO}" font-size="10" letter-spacing="1.2" fill="{MUTED}">{label}</text>"""
        write(f"stat-{i}.svg", svg(w, h, body, label=f"{num}{plus} {label.lower()}"))


# ── Project cards ────────────────────────────────────────────────────────────
PROJECTS = [
    ("PropIQ", "PUBLIC REPO", "AI loan intelligence · RAG + MCP tool calling",
     ["Simulated commercial real-estate loan servicing with", "a RAG pipeline over loan documents and an AI copilot",
      "that routes questions to four structured tools."],
     ["LangChain", "FAISS", "FastAPI", "MySQL", "NVIDIA NIM"]),
    ("Vukti", "LIVE", "Academic platform and student OS",
     ["Nine modules for technical institutions: exams on a", "self-hosted Judge0, gamified practice with 1,000+",
      "problems, and sync from six coding platforms."],
     ["React", "FastAPI", "PostgreSQL", "Docker", "Judge0"]),
    ("Almaanac", "LIVE", "Classroom coding analytics",
     ["One educator dashboard for coding activity across", "eight platforms, with per-platform async workers,",
      "leaderboards, at-risk cohorts, and 365-day heatmaps."],
     ["TanStack Start", "Supabase", "TypeScript", "Recharts"]),
    ("FDE Flow Atlas", "LIVE", "Interactive AI engineering curriculum",
     ["133 topics on RAG, tool calling, and agent workflows,", "each taught through an animated flow diagram, with",
      "quizzes and 11 hands-on projects."],
     ["JavaScript", "SVG Animation", "GitHub Pages"]),
    ("ILFU", "IN DEVELOPMENT", "Open-source local meeting transcriber",
     ["Runs fully on your machine: no API keys, no accounts,", "no bot in the call. Loopback audio capture, on-device",
      "speech-to-text, and local LLM summaries."],
     ["Python", "faster-whisper", "whisper.cpp", "WASAPI"]),
    ("Forward", "LOCAL INSTALL", "Presenter and live-teaching copilot",
     ["Live transcription and AI speaker notes in a private", "presenter-only window, with a five-provider fallback",
      "chain and Whisper running on an AMD NPU."],
     ["C# WPF", ".NET 8", "Claude API", "Whisper ONNX"]),
]


def projects():
    w, h = 412, 236
    for i, (name, status, tag, desc, stack) in enumerate(PROJECTS, 1):
        live = status in ("LIVE", "PUBLIC REPO")
        pw = round(len(status) * 9.5 * MONO_W + 20)
        px = w - 24 - pw
        chip_svg, rows = chips(stack, 24, 190, w - 48)
        assert rows == 1, f"{name}: stack chips overflow one row"
        lines = "\n".join(
            f'<text x="24" y="{128 + j * 18}" font-family="{SANS}" font-size="12.5" fill="{SOFT}">{esc(t)}</text>'
            for j, t in enumerate(desc)
        )
        body = f"""<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{CARD}" stroke="{BR}"/>
<text x="24" y="37" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="{ACC}">0{i}</text>
<rect x="{px}" y="22" width="{pw}" height="22" rx="11" fill="none" stroke="{ACC if live else PILL_BR}"/>
<text x="{px + pw / 2}" y="36.5" text-anchor="middle" font-family="{MONO}" font-size="9.5" letter-spacing="0.6" fill="{ACC if live else MUTED}">{status}</text>
<text x="24" y="78" font-family="{SERIF}" font-size="28" fill="{FG}">{esc(name)}</text>
<text x="24" y="100" font-family="{SANS}" font-size="12.5" font-style="italic" fill="{ACC_LIT}">{esc(tag)}</text>
{lines}
{chip_svg}"""
        write(f"proj-{i}.svg", svg(w, h, body, label=f"{name}: {tag}. {' '.join(desc)}"))


# ── Stack cards ──────────────────────────────────────────────────────────────
STACK = [
    ("AI / LLM", ["RAG Pipelines", "Embeddings", "FAISS", "MCP Tool Calling", "LangChain", "Claude API",
                  "NVIDIA NIM", "Whisper"]),
    ("BUILD", ["Python", "TypeScript", "JavaScript", "Java", "C#", "SQL", "React", "TanStack Start",
               "Tailwind CSS", "FastAPI", "Node.js", ".NET 8"]),
    ("DATA / DEVOPS", ["PostgreSQL", "MySQL", "Redis", "Supabase", "Docker", "GitHub Actions", "Vercel", "Power BI"]),
    ("CLIENT ENABLEMENT", ["Technical Training", "Workshops", "Live Demos", "Curriculum Design",
                           "Technical Writing", "Stakeholder Management"]),
]


def stack():
    w, top = 412, 58
    laid = [chips(items, 24, top, w - 48, size=11, h=26, pad=10) for _, items in STACK]
    h = top + max(rows for _, rows in laid) * 34 - 8 + 24  # one height so rows of cards align
    for i, ((title, _), (chip_svg, _)) in enumerate(zip(STACK, laid), 1):
        body = f"""<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{CARD}" stroke="{BR}"/>
<text x="24" y="37" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="{ACC}">{esc(title)}</text>
{chip_svg}"""
        write(f"stack-{i}.svg", svg(w, h, body, label=f"{title}: {', '.join(STACK[i - 1][1])}"))


# ── Footer ───────────────────────────────────────────────────────────────────
def footer():
    w, h = 828, 156
    body = f"""<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{BG}" stroke="{BR}"/>
<text x="38" y="70" font-family="{SERIF}" font-size="36" fill="{FG}">Let's build something <tspan font-style="italic" fill="{ACC}">together.</tspan></text>
<text x="40" y="100" font-family="{SANS}" font-size="14" fill="{SOFT}">Open to Forward Deployed Engineer, AI Solutions, and Technical Enablement roles.</text>
<text x="40" y="126" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{MUTED}">vijaysundarn@gmail.com</text>
<rect x="{w - 40 - 150}" y="56" width="150" height="44" rx="22" fill="{ACC}"/>
<text x="{w - 40 - 75}" y="83" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="{BG}">Book a call</text>"""
    write("footer.svg", svg(w, h, body, label="Let's build something together. Book a call."))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for build in (header, buttons, chapters, stats, projects, stack, footer):
        build()
    print("wrote", len(os.listdir(OUT)), "files to", OUT)
