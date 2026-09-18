#!/usr/bin/env python3
"""Render a cover letter (the repo's cover-letter.md format) to a clean PDF with headless Chromium.

Usage:
    python3 scripts/render_letter.py applications/<folder>/cover-letter.md [--out path.pdf]

Format expected (blank-line separated blocks):
    block 1  : name on line 1, contact line on line 2
    block 2  : date
    block 3  : recipient address (any lines)
    "Re: ..."   line becomes bold
    salutation, body paragraphs, sign-off ("Sincerely," + name) follow
    A block whose first line starts with "Prompts used" starts page 2 (the appendix).
    In the appendix, a block wrapped in straight quotes is rendered as a shaded prompt box.
Fonts: Bitstream Charter (body) and Liberation Sans (header), both present in the sandbox.
"""
import argparse, html, os, re, shutil, subprocess, sys, tempfile

CSS = """
@page { size: Letter; margin: 0.85in 0.95in 0.85in 0.95in; }
body { font-family: 'Bitstream Charter', 'Charter', 'Liberation Serif', Georgia, serif;
       font-size: 11pt; line-height: 1.42; color: #111; }
.name { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 20pt; font-weight: 700;
        letter-spacing: 0.5px; margin: 0; }
.contact { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 9.5pt; color: #333;
           margin: 2px 0 0 0; }
.rule { border: 0; border-top: 1.2px solid #111; margin: 10px 0 16px 0; }
.date, .addr { margin: 0 0 12px 0; white-space: pre-line; }
.re { font-weight: 700; margin: 0 0 12px 0; }
p { margin: 0 0 10px 0; text-align: left; }
a { color: #1a4d8f; text-decoration: underline; text-decoration-thickness: 0.6px; text-underline-offset: 2px; }
.contact a { color: #1a4d8f; }
.sign { margin-top: 18px; }
.appendix { page-break-before: always; }
.appendix h2 { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 12.5pt;
               font-weight: 700; margin: 0 0 12px 0; text-transform: none;
               border-bottom: 1.2px solid #111; padding-bottom: 4px; }
.prompt { background: #f2f2f0; border-left: 3px solid #999; padding: 10px 12px;
          font-family: 'Liberation Sans', Arial, sans-serif; font-size: 9.6pt; line-height: 1.38;
          margin: 6px 0 12px 0; white-space: pre-wrap; }
"""

URL_RX = re.compile(r"(?<![\w/])((?:https?://)?(?:www\.)?(?:[a-z0-9-]+\.)*(?:linkedin\.com|github\.com|[a-z0-9-]+\.(?:com|ca|io|org|net|energy|ai))(?:/[^\s<>\"')\]]*)?)(?=[\s.,;:)\]]|$)", re.I)
EMAIL_RX = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

def esc(s):
    """Escape HTML, then turn URLs and emails into links so the PDF carries clickable
    annotations (LinkedIn, the public repo, email). James's rule, 2026-09-18."""
    out = html.escape(s, quote=False)
    out = EMAIL_RX.sub(lambda m: f'<a href="mailto:{m.group(0)}">{m.group(0)}</a>', out)
    def link(m):
        u = m.group(1)
        href = u if u.lower().startswith("http") else "https://" + u
        return f'<a href="{href}">{u}</a>'
    return URL_RX.sub(link, out)

def render(md_path, out_path):
    text = open(md_path, encoding="utf-8").read().strip()
    blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", text) if b.strip()]
    head = blocks[0].split("\n")
    name, contact = head[0].strip(), " ".join(l.strip() for l in head[1:])
    parts = [f'<p class="name">{esc(name)}</p><p class="contact">{esc(contact)}</p><hr class="rule">']
    in_appendix = False
    i = 1
    if i < len(blocks): parts.append(f'<p class="date">{esc(blocks[i])}</p>'); i += 1
    if i < len(blocks): parts.append(f'<p class="addr">{esc(blocks[i])}</p>'); i += 1
    for b in blocks[i:]:
        first = b.split("\n")[0]
        if first.lower().startswith("prompts used"):
            in_appendix = True
            parts.append(f'<div class="appendix"><h2>{esc(first)}</h2>')
            rest = "\n".join(b.split("\n")[1:]).strip()
            if rest: parts.append(f"<p>{esc(rest)}</p>")
            continue
        if first.startswith("Re:"):
            parts.append(f'<p class="re">{esc(b)}</p>'); continue
        if in_appendix and b.startswith('"') and b.rstrip().endswith('"'):
            parts.append(f'<div class="prompt">{esc(b)}</div>'); continue
        if b.startswith("Sincerely") or b.startswith("Best") or b.startswith("Cheers"):
            parts.append(f'<p class="sign">{esc(b)}</p>'); continue
        if b == name:
            parts.append(f"<p>{esc(b)}</p>"); continue
        parts.append(f"<p>{esc(b)}</p>")
    if in_appendix: parts.append("</div>")
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(parts)}</body></html>"
    tmp = tempfile.mkdtemp()
    hp = os.path.join(tmp, "letter.html"); open(hp, "w", encoding="utf-8").write(doc)
    chrome = None
    for c in ["/opt/pw-browsers/chromium", "chromium", "chromium-browser", "google-chrome"]:
        if os.path.isfile(c) and os.access(c, os.X_OK): chrome = c; break
        w = shutil.which(c)
        if w: chrome = w; break
    if chrome is None:
        for root, _, files in os.walk("/opt/pw-browsers"):
            for f in files:
                if f in ("chrome", "chromium", "headless_shell"): chrome = os.path.join(root, f); break
            if chrome: break
    if chrome is None: sys.exit("no chromium found")
    cmd = [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={os.path.abspath(out_path)}", f"file://{hp}"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not os.path.exists(out_path): sys.exit(f"render failed: {r.stderr[-800:]}")
    data = open(out_path, "rb").read()
    pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
    print(f"{out_path}: {pages} page(s), {len(data)//1024} KB")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("md"); ap.add_argument("--out")
    a = ap.parse_args()
    out = a.out or os.path.join(os.path.dirname(a.md), "cover-letter.pdf")
    render(a.md, out)
