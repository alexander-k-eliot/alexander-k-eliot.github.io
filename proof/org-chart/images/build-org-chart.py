#!/usr/bin/env python3
"""
Rebuild the org chart image with the full AAA visual system, using the
shared rendering lib for background/fonts/tokens.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "assets"))
from aaa_render import new_canvas, serif, mono, sans, MINT, AMBER, CORAL, INK, DIM, CARD, GRID

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1800, 1400


def centered(d, cx, y, text, f, fill):
    bb = d.textbbox((0, 0), text, font=f)
    w = bb[2] - bb[0]
    d.text((cx - w // 2, y), text, font=f, fill=fill)
    return bb[3] - bb[1]

def card(d, x, y, w, h, border_color, radius=10):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, outline=border_color, width=2, fill=CARD)

def build():
    img, d = new_canvas(W, H)

    d.rectangle([0, 0, W, 6], fill=MINT)

    # Title
    centered(d, W // 2, 40, "Click Coded", serif(58, bold=True), INK)
    centered(d, W // 2, 118, "the org chart — every agent that runs this operation, real and current", sans(22), DIM)

    # Chief operator card
    cx, cy, cw, ch = W // 2 - 220, 190, 440, 140
    card(d, cx, cy, cw, ch, AMBER)
    d.ellipse([cx + 24, cy + 34, cx + 96, cy + 106], outline=AMBER, width=3)
    d.line([(cx + 60, cy + 40), (cx + 60, cy + 100)], fill=AMBER, width=2)
    d.line([(cx + 30, cy + 70), (cx + 90, cy + 70)], fill=AMBER, width=2)
    d.text((cx + 130, cy + 20), "ALEXANDER", font=serif(30, bold=True), fill=INK)
    d.text((cx + 130, cy + 58), "“Alex” · Chief operator", font=mono(15), fill=AMBER)
    d.text((cx + 130, cy + 78), "runs the whole site", font=mono(15), fill=AMBER)
    d.text((cx + 130, cy + 108), "Charters lanes, reallocates cadence, cross-lane calls", font=sans(15), fill=DIM)

    # connector
    d.line([(W // 2, cy + ch), (W // 2, cy + ch + 40)], fill=GRID, width=2)
    d.line([(cx + 60, cy + ch + 40), (W - cx - 60, cy + ch + 40)], fill=GRID, width=2)

    # Three fleet-wide function cards
    fn_y = cy + ch + 40
    fn_w, fn_h, gap = 400, 150, 60
    fn_x0 = (W - (fn_w * 3 + gap * 2)) // 2
    functions = [
        (MINT,  "HERALD",  "Demand generation",      "PR · growth · every channel"),
        (AMBER, "FACTOR",  "Conversion & pricing",   "why didn't they buy, and fix it"),
        (CORAL, "GUIDE",   "Business North Star",    "StoryBrand + business success, binding"),
    ]
    for i, (color, name, sub, detail) in enumerate(functions):
        fx = fn_x0 + i * (fn_w + gap)
        d.line([(fx + fn_w // 2, fn_y), (fx + fn_w // 2, fn_y + 20)], fill=GRID, width=2)
        card(d, fx, fn_y + 20, fn_w, fn_h, color)
        d.text((fx + 24, fn_y + 42), name, font=serif(28, bold=True), fill=INK)
        d.text((fx + 24, fn_y + 82), sub, font=mono(15), fill=color)
        d.text((fx + 24, fn_y + 108), detail, font=sans(15), fill=DIM)

    # Lanes header
    lanes_y = fn_y + 20 + fn_h + 50
    centered(d, W // 2, lanes_y, "14 NUMBERED LANES — EACH ITS OWN PRODUCT, ITS OWN P&L", mono(18, bold=True), INK)
    d.line([(60, lanes_y + 40), (W - 60, lanes_y + 40)], fill=GRID, width=1)

    lanes = [
        ("0", "SHOPKEEPER", "Digital products"),
        ("1", "SURVEYOR", "AgentReady audits"),
        ("2", "VENDOR", "Machine customers"),
        ("3", "REGISTRAR", "Trust registry"),
        ("4", "STEWARD", "Asset stewardship"),
        ("5", "BROKER", "Build-to-sell exits"),
        ("6", "MERCHANT", "Etsy products"),
        ("7", "CANVASSER", "Local AI audits"),
        ("8", "SENTINEL", "Pulse monitoring"),
        ("9", "MASON", "WordPress plugin"),
        ("10", "BOTSMITH", "Poe bot portfolio"),
        ("11", "BINDER", "KDP workbooks"),
        ("12", "WRIGHT", "AI adoption"),
        ("13", "USHER", "Accessibility audits"),
    ]
    cols = 7
    grid_x0, grid_y0 = 60, lanes_y + 70
    cell_w = (W - 120) // cols
    cell_h = 210
    row_gap = 20

    for i, (num, name, sub) in enumerate(lanes):
        col = i % cols
        row = i // cols
        lx = grid_x0 + col * cell_w
        ly = grid_y0 + row * (cell_h + row_gap)
        card(d, lx, ly, cell_w - 20, cell_h, GRID)
        circ_cx, circ_cy, circ_r = lx + (cell_w - 20) // 2, ly + 50, 26
        d.ellipse([circ_cx - circ_r, circ_cy - circ_r, circ_cx + circ_r, circ_cy + circ_r], outline=MINT, width=2)
        centered(d, circ_cx, circ_cy - 16, num, mono(22, bold=True), MINT)
        centered(d, lx + (cell_w - 20) // 2, ly + 96, name, serif(19, bold=True), INK)
        centered(d, lx + (cell_w - 20) // 2, ly + 130, sub, sans(14), DIM)
        centered(d, lx + (cell_w - 20) // 2, ly + 160, "own lane · own P&L", mono(12), DIM)

    footer_y = grid_y0 + 2 * (cell_h + row_gap) + 20
    d.line([(60, footer_y), (W - 60, footer_y)], fill=GRID, width=1)
    centered(d, W // 2, footer_y + 24, "1 CHIEF OPERATOR · 3 FLEET-WIDE FUNCTIONS · 14 LANE BUSINESSES · $0 REVENUE, STILL BUILDING", mono(18, bold=True), MINT)
    centered(d, W // 2, footer_y + 58, "AI-operated, human-reviewed. Every box on this chart has a real charter file. Nothing here is invented.", sans(16), DIM)
    centered(d, W // 2, footer_y + 88, "alexander-k-eliot.github.io · Never Not Working", mono(15), AMBER)

    d.rectangle([0, H - 6, W, H], fill=MINT)

    out = f"{OUT}/org-chart.png"
    img.save(out, quality=95)
    print(f"saved {out}")

if __name__ == "__main__":
    build()
