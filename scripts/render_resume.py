#!/usr/bin/env python3
"""Render resumes/RESUME.md to a one-page PDF with headless Chromium, same typography as the letter.

Format:
    # NAME
    contact line
    ## SECTION
    ### Title | Right side (location)
    *Subtitle | Right side (dates)*
    - bullet
    **Label:** text          (skills lines)
Shrinks the font in steps until the result is one page.
"""
import html, os, re, subprocess, sys, tempfile

CSS = """
@page {{ size: Letter; margin: 0.45in 0.6in 0.4in 0.6in; }}
body {{ font-family: 'Bitstream Charter','Charter','Liberation Serif',Georgia,serif; font-size: {fs}pt; line-height: 1.22; color: #111; }}
.name {{ font-family: 'Liberation Sans', Arial, sans-serif; font-size: {name}pt; font-weight: 700; letter-spacing: 1px; text-align: center; margin: 0; }}
.contact {{ font-family: 'Liberation Sans', Arial, sans-serif; font-size: {small}pt; color: #333; text-align: center; margin: 2px 0 0 0; }}
h2 {{ font-family: 'Liberation Sans', Arial, sans-serif; font-size: {h2}pt; font-weight: 700; letter-spacing: 0.6px; margin: 6px 0 2px 0; padding-bottom: 2px; border-bottom: 1.1px solid #111; }}
.row {{ display: flex; justify-content: space-between; align-items: baseline; margin: 3px 0 0 0; }}
.title {{ font-weight: 700; }}
.sub {{ display: flex; justify-content: space-between; font-style: italic; margin: 0 0 1px 0; }}
.right {{ font-weight: 400; white-space: nowrap; margin-left: 12px; }}
ul {{ margin: 1px 0 0 0; padding-left: 15px; }}
li {{ margin: 0 0 0.5px 0; }}
p.skill {{ margin: 0 0 2px 0; }}
a {{ color: #1a4d8f; text-decoration: none; }}
"""
URL_RX = re.compile(r"(?<![\w/])((?:https?://)?(?:www\.)?(?:linkedin\.com|github\.com|rosslogic\.com)(?:/[^\s<>\"')\]]*)?)(?=[\s.,;:)\]]|$)", re.I)
EMAIL_RX = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

def esc(s):
    out = html.escape(s, quote=False)
    out = EMAIL_RX.sub(lambda m: f'<a href="mailto:{m.group(0)}">{m.group(0)}</a>', out)
    def link(m):
        u = m.group(1); trail = ""
        while u and u[-1] in ".,;:)]": trail = u[-1] + trail; u = u[:-1]
        href = u if u.lower().startswith("http") else "https://" + u
        return f'<a href="{href}">{u}</a>{trail}'
    out = URL_RX.sub(link, out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    return out

def build(md):
    parts, in_ul = [], False
    def close_ul():
        nonlocal in_ul
        if in_ul: parts.append("</ul>"); in_ul = False
    lines = md.split("\n")
    for i, line in enumerate(lines):
        s = line.rstrip()
        if not s: continue
        if s.startswith("# "):
            parts.append(f'<p class="name">{esc(s[2:])}</p>')
            if i + 1 < len(lines) and lines[i+1].strip() and not lines[i+1].startswith("#"):
                parts.append(f'<p class="contact">{esc(lines[i+1].strip())}</p>'); lines[i+1] = ""
        elif s.startswith("## "):
            close_ul(); parts.append(f"<h2>{esc(s[3:])}</h2>")
        elif s.startswith("### "):
            close_ul(); t, _, r = s[4:].partition(" | ")
            parts.append(f'<div class="row"><span class="title">{esc(t)}</span><span class="right">{esc(r)}</span></div>')
        elif s.startswith("*") and s.endswith("*") and not s.startswith("**"):
            t, _, r = s[1:-1].partition(" | ")
            parts.append(f'<div class="sub"><span>{esc(t)}</span><span class="right">{esc(r)}</span></div>')
        elif s.startswith("- "):
            if not in_ul: parts.append("<ul>"); in_ul = True
            parts.append(f"<li>{esc(s[2:])}</li>")
        elif s.startswith("**"):
            close_ul(); parts.append(f'<p class="skill">{esc(s)}</p>')
        else:
            close_ul(); parts.append(f"<p>{esc(s)}</p>")
    close_ul()
    return "".join(parts)

def find_chrome():
    for c in ["/opt/pw-browsers/chromium", "chromium", "chromium-browser", "google-chrome"]:
        if os.path.isfile(c) and os.access(c, os.X_OK): return c
    for root, _, files in os.walk("/opt/pw-browsers"):
        for f in files:
            if f in ("chrome", "chromium", "headless_shell"): return os.path.join(root, f)
    sys.exit("no chromium found")

def render(md_path, out_path):
    body = build(open(md_path, encoding="utf-8").read())
    chrome = find_chrome(); tmp = tempfile.mkdtemp()
    for fs in (10.0, 9.8, 9.6, 9.4, 9.2, 9.0, 8.8):
        css = CSS.format(fs=fs, name=fs+9, small=fs-0.8, h2=fs+0.6)
        hp = os.path.join(tmp, "resume.html")
        open(hp, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>")
        subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={os.path.abspath(out_path)}", f"file://{hp}"], capture_output=True, text=True, timeout=120)
        data = open(out_path, "rb").read()
        pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
        if pages == 1:
            print(f"{out_path}: 1 page at {fs}pt, {len(data)//1024} KB"); return
    print(f"{out_path}: still {pages} pages at {fs}pt; trim content")

if __name__ == "__main__":
    md = sys.argv[1] if len(sys.argv) > 1 else "resumes/RESUME.md"
    out = sys.argv[2] if len(sys.argv) > 2 else "resumes/James_Ross_Resume.pdf"
    render(md, out)
