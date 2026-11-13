#!/usr/bin/env python3
"""Builds a one-page website from a JSON config into <out>/index.html.

    python3 templates/website/build.py templates/website/configs/salon.json --out templates/website/dist/salon

Sections are optional: include only the keys the business needs
(services, steps, about, hours, testimonials, contact).
"""
import argparse, html, json, os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
e = lambda s: html.escape(str(s or ""))


def section(id_, title, lead, body, soft=False):
    style = ' style="background:var(--soft)"' if soft else ""
    lead_html = f'<p class="lead">{e(lead)}</p>' if lead else ""
    return f'<section id="{id_}"{style}><div class="wrap"><h2>{e(title)}</h2>{lead_html}{body}</div></section>'


def build(cfg):
    parts, nav = [], []
    soft = False
    if s := cfg.get("services"):
        cards = "".join(
            f'<div class="card"><h3>{e(i["name"])}</h3><p>{e(i.get("text"))}</p>'
            + (f'<span class="price">{e(i["price"])}</span>' if i.get("price") else "") + "</div>"
            for i in s["items"])
        parts.append(section("services", s.get("title", "Services"), s.get("lead"), f'<div class="grid">{cards}</div>', soft)); soft = not soft
        nav.append(("services", s.get("nav", "Services")))
    if s := cfg.get("steps"):
        items = "".join(f'<li><strong>{e(i["name"])}</strong><br><span class="who">{e(i.get("text"))}</span></li>' for i in s["items"])
        parts.append(section("how", s.get("title", "How it works"), s.get("lead"), f'<ol class="steps">{items}</ol>', soft)); soft = not soft
        nav.append(("how", s.get("nav", "How it works")))
    if cfg.get("about") or cfg.get("hours"):
        a = cfg.get("about") or {}
        left = "".join(f"<p>{e(p)}</p>" for p in a.get("paragraphs", []))
        right = ""
        if h := cfg.get("hours"):
            rows = "".join(f"<tr><td>{e(d)}</td><td>{e(t)}</td></tr>" for d, t in h.items())
            right = f'<h3>Opening hours</h3><table class="hours">{rows}</table>'
        parts.append(section("about", a.get("title", "About us"), None, f'<div class="split"><div>{left}</div><div>{right}</div></div>', soft)); soft = not soft
        nav.append(("about", a.get("nav", "About")))
    if t := cfg.get("testimonials"):
        cards = "".join(f'<div class="card"><p class="quote">“{e(i["quote"])}”</p><span class="who">{e(i["who"])}</span></div>' for i in t)
        parts.append(section("reviews", "What clients say", None, f'<div class="grid">{cards}</div>', soft)); soft = not soft
    c = cfg["contact"]
    lines = []
    if c.get("phone"): lines.append(f'Phone: <a href="tel:{e(c["phone"].replace(" ", ""))}">{e(c["phone"])}</a>')
    if c.get("email"): lines.append(f'Email: <a href="mailto:{e(c["email"])}">{e(c["email"])}</a>')
    if c.get("address"): lines.append(f'Address: {e(c["address"])}')
    map_link = f'<p><a href="https://www.google.com/maps/search/?api=1&query={e(c["address"])}">Get directions</a></p>' if c.get("address") else ""
    parts.append(section("contact", "Contact", c.get("lead"), "<p>" + "<br>".join(lines) + "</p>" + map_link, soft))
    nav.append(("contact", "Contact"))

    sec = cfg.get("secondary_cta")
    values = {
        "title": cfg.get("title") or cfg["name"], "description": cfg["description"],
        "brand": cfg.get("brand_colour", "#2f5d50"), "name": cfg["name"],
        "nav": "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in nav),
        "cta_url": cfg["cta"]["url"], "cta_label": cfg["cta"]["label"],
        "secondary_cta": f'<a class="btn ghost" href="{e(sec["url"])}">{e(sec["label"])}</a>' if sec else "",
        "headline": cfg["headline"], "subheadline": cfg["subheadline"],
        "sections": "\n".join(parts),
        "closing_title": cfg.get("closing_title", "Ready when you are"), "closing_text": cfg.get("closing_text", ""),
        "year": date.today().year, "legal_name": cfg.get("legal_name", cfg["name"]),
        "footer_contact": " · ".join(x for x in [c.get("phone"), c.get("email")] if x),
    }
    out = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    raw = {"nav", "sections", "secondary_cta"}
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", str(v) if k in raw else e(v))
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("config")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "index.html"), "w", encoding="utf-8") as f:
        f.write(build(cfg))
    print(f"Built {os.path.join(a.out, 'index.html')}")
