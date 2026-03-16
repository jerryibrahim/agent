#!/usr/bin/env python3
"""SVG infographic slides for the Agent codebase — a Claude Code skills toolkit.

Zero external dependencies — uses only Python stdlib.
"""

import os
from xml.sax.saxutils import escape

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS — shared SVG primitives (do not modify)
# ═══════════════════════════════════════════════════════════════════════════════

def write_svg(filename, content, width=1200, height=900):
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<defs>
  <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#0f172a"/>
    <stop offset="100%" stop-color="#0a0e1a"/>
  </linearGradient>
</defs>
<rect width="{width}" height="{height}" fill="url(#bgGrad)"/>
{content}
</svg>'''
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)

def title_bar(title, subtitle, width=1200, accent="#3b82f6"):
    return f'''<rect x="0" y="0" width="{width}" height="80" fill="#0a0e1a" opacity="0.7"/>
<text x="40" y="38" font-family="system-ui, sans-serif" font-size="24" font-weight="700" fill="{accent}">{escape(title)}</text>
<text x="40" y="62" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">{escape(subtitle)}</text>
<line x1="40" y1="76" x2="{width - 40}" y2="76" stroke="#1e293b" stroke-width="1"/>'''

def text_block(lines, x, y, font_size=16, color="#e2e8f0", line_height=24, font_family="system-ui, sans-serif"):
    parts = []
    for i, line in enumerate(lines):
        parts.append(
            f'<text x="{x}" y="{y + i * line_height}" font-family="{font_family}" '
            f'font-size="{font_size}" fill="{color}">{escape(line)}</text>'
        )
    return "\n".join(parts)

def rounded_rect(x, y, w, h, fill="#111827", stroke="#1e293b", rx=10, stroke_width=1.5):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')

def box_with_label(x, y, w, h, label, sub="", fill="#111827", stroke="#3b82f6", text_color="#3b82f6"):
    parts = [rounded_rect(x, y, w, h, fill=fill, stroke=stroke)]
    parts.append(
        f'<text x="{x + w/2}" y="{y + h/2 - (6 if sub else 0)}" '
        f'font-family="system-ui, sans-serif" font-size="14" font-weight="600" '
        f'fill="{text_color}" text-anchor="middle">{escape(label)}</text>'
    )
    if sub:
        parts.append(
            f'<text x="{x + w/2}" y="{y + h/2 + 14}" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="10" '
            f'fill="#94a3b8" text-anchor="middle">{escape(sub)}</text>'
        )
    return "\n".join(parts)

def arrow(x1, y1, x2, y2, color="#94a3b8", dashed=False):
    dash = ' stroke-dasharray="6,4"' if dashed else ''
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="1.5"{dash} marker-end="url(#arrow-{color.replace("#","")})"/>\n'
            f'<defs><marker id="arrow-{color.replace("#","")}" markerWidth="10" markerHeight="7" '
            f'refX="10" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="{color}"/></marker></defs>')

def arrow_simple(x1, y1, x2, y2, color="#94a3b8", label=""):
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    parts = [
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" stroke-dasharray="6,4"/>',
        f'<circle cx="{x2}" cy="{y2}" r="3" fill="{color}"/>',
    ]
    if label:
        parts.append(
            f'<text x="{mid_x}" y="{mid_y - 8}" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="10" fill="#94a3b8" text-anchor="middle">{escape(label)}</text>'
        )
    return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE RENDERERS — data-driven layout functions (do not modify)
# ═══════════════════════════════════════════════════════════════════════════════

def render_eli5(d):
    """Slide 01: ELI5 — 50,000 ft overview with analogy + feature cards."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#3b82f6"))

    # Main analogy box
    content += rounded_rect(40, 100, 1120, 160, fill="#111827", stroke=d.get("accent", "#3b82f6"))
    content += text_block(d["analogy_lines"], 70, 135, font_size=16, color="#cbd5e1", line_height=26)

    # Feature/concept cards — 3 columns, auto-rows
    cards = d["cards"]  # list of (name, metaphor, description, color, path_hint)
    y_start = 300
    for i, card in enumerate(cards):
        name, metaphor, desc, color = card[0], card[1], card[2], card[3]
        path_hint = card[4] if len(card) > 4 else ""
        col = i % 3
        row = i // 3
        x = 40 + col * 380
        y = y_start + row * 180
        content += rounded_rect(x, y, 360, 150, fill="#111827", stroke=color)
        content += f'<circle cx="{x + 35}" cy="{y + 40}" r="18" fill="{color}" opacity="0.2"/>'
        content += f'<circle cx="{x + 35}" cy="{y + 40}" r="8" fill="{color}"/>'
        content += (f'<text x="{x + 65}" y="{y + 35}" font-family="system-ui, sans-serif" '
                    f'font-size="18" font-weight="700" fill="{color}">{escape(name)}</text>')
        content += (f'<text x="{x + 65}" y="{y + 55}" font-family="system-ui, sans-serif" '
                    f'font-size="13" fill="#94a3b8">{escape(metaphor)}</text>')
        content += (f'<text x="{x + 30}" y="{y + 90}" font-family="system-ui, sans-serif" '
                    f'font-size="14" fill="#cbd5e1">{escape(desc)}</text>')
        if path_hint:
            content += (f'<text x="{x + 30}" y="{y + 120}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="11" fill="#475569">{escape(path_hint)}</text>')

    # Bottom note
    if d.get("bottom_note"):
        content += (f'<text x="600" y="840" font-family="system-ui, sans-serif" font-size="14" '
                    f'fill="#475569" text-anchor="middle">{escape(d["bottom_note"])}</text>')

    write_svg("slide_01_eli5.svg", content)


def render_system_context(d):
    """Slide 02: System context — actors, systems, and connections."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#10b981"))

    # Render actor/system boxes
    for box in d["boxes"]:
        content += box_with_label(
            box["x"], box["y"], box.get("w", 160), box.get("h", 70),
            box["label"], box.get("sub", ""),
            stroke=box["color"], text_color=box["color"]
        )

    # Render connections
    for conn in d.get("connections", []):
        fx, fy = conn["from_xy"]
        tx, ty = conn["to_xy"]
        content += arrow_simple(fx, fy, tx, ty, color=conn.get("color", "#94a3b8"), label=conn.get("label", ""))

    # Bottom note
    if d.get("bottom_note"):
        content += (f'<text x="600" y="830" font-family="system-ui, sans-serif" font-size="13" '
                    f'fill="#475569" text-anchor="middle">{escape(d["bottom_note"])}</text>')

    write_svg("slide_02_system_context.svg", content)


def render_architecture_layers(d):
    """Slide 03: Architecture layers — stacked horizontal bars with arrows."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#8b5cf6"))

    layers = d["layers"]
    layer_height = 80
    gap = 30
    start_y = 120
    width = 1040
    x_start = 80

    for i, (label, desc, color) in enumerate(layers):
        y = start_y + i * (layer_height + gap)
        content += rounded_rect(x_start, y, width, layer_height, stroke=color)
        content += (f'<text x="{x_start + 40}" y="{y + 35}" font-family="system-ui, sans-serif" font-size="18" '
                    f'font-weight="600" fill="{color}">{escape(label)}</text>')
        content += (f'<text x="{x_start + 40}" y="{y + 58}" font-family="system-ui, sans-serif" font-size="13" '
                    f'fill="#94a3b8">{escape(desc)}</text>')

    for i in range(len(layers) - 1):
        y1 = start_y + i * (layer_height + gap) + layer_height
        y2 = start_y + (i + 1) * (layer_height + gap)
        content += (f'<line x1="600" y1="{y1}" x2="600" y2="{y2}" '
                    f'stroke="#334155" stroke-width="1.5" stroke-dasharray="4,4"/>')
        content += f'<polygon points="595,{y2 - 5} 600,{y2} 605,{y2 - 5}" fill="#334155"/>'

    mid_y = start_y + (len(layers) * (layer_height + gap)) / 2
    content += (f'<text x="1140" y="{mid_y}" font-family="system-ui, sans-serif" font-size="11" '
                f'fill="#475569" text-anchor="end" transform="rotate(-90, 1140, {mid_y})">'
                f'{escape(d.get("side_label", "Request Flow"))}</text>')

    total_height = max(900, start_y + len(layers) * (layer_height + gap) + 40)
    write_svg("slide_03_architecture_layers.svg", content, height=total_height)


def render_domain_model(d):
    """Slide 04: Domain model — entity boxes with fields and relationships."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#ec4899"))

    for entity in d["entities"]:
        x, y = entity["x"], entity["y"]
        w, h = entity.get("w", 280), entity.get("h", 120)
        color = entity["color"]
        content += rounded_rect(x, y, w, h, stroke=color)
        content += (f'<text x="{x + w/2}" y="{y + 30}" font-family="system-ui, sans-serif" font-size="18" '
                    f'font-weight="700" fill="{color}" text-anchor="middle">{escape(entity["name"])}</text>')
        for i, field in enumerate(entity.get("fields", [])):
            content += (f'<text x="{x + 20}" y="{y + 55 + i * 18}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="11" fill="#94a3b8">{escape(field)}</text>')

    for rel in d.get("relationships", []):
        fx, fy = rel["from_xy"]
        tx, ty = rel["to_xy"]
        content += arrow_simple(fx, fy, tx, ty, color=rel.get("color", "#94a3b8"), label=rel.get("label", ""))

    if d.get("examples"):
        y_ex = d.get("examples_y", 520)
        content += rounded_rect(80, y_ex, 1040, 20 + len(d["examples"]) * 18 + 30, fill="#0a0e1a", stroke="#1e293b")
        content += (f'<text x="100" y="{y_ex + 25}" font-family="system-ui, sans-serif" font-size="13" '
                    f'font-weight="600" fill="#94a3b8">Concrete Examples:</text>')
        for i, ex in enumerate(d["examples"]):
            content += (f'<text x="120" y="{y_ex + 48 + i * 18}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="11" fill="#cbd5e1">{escape(ex)}</text>')

    write_svg("slide_04_domain_model.svg", content)


def render_request_lifecycle(d):
    """Slide 05: Request lifecycle — numbered steps with connector lines."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#ef4444"))

    steps = d["steps"]
    step_height = 70
    gap = 20
    start_y = 120

    for i, (label, desc, color) in enumerate(steps):
        y = start_y + i * (step_height + gap)
        num = str(i + 1)

        content += f'<circle cx="80" cy="{y + 25}" r="20" fill="{color}" opacity="0.15"/>'
        content += (f'<text x="80" y="{y + 30}" font-family="system-ui, sans-serif" font-size="16" '
                    f'font-weight="700" fill="{color}" text-anchor="middle">{num}</text>')

        content += (f'<text x="120" y="{y + 22}" font-family="system-ui, sans-serif" font-size="16" '
                    f'font-weight="600" fill="#e2e8f0">{escape(label)}</text>')
        content += (f'<text x="120" y="{y + 44}" font-family="system-ui, sans-serif" font-size="13" '
                    f'fill="#94a3b8">{escape(desc)}</text>')

        if i < len(steps) - 1:
            content += f'<line x1="80" y1="{y + 50}" x2="80" y2="{y + step_height + gap - 5}" stroke="#334155" stroke-width="1.5"/>'

    if d.get("side_note"):
        mid_y = start_y + (len(steps) * (step_height + gap)) / 2
        content += (f'<text x="1100" y="{mid_y}" font-family="system-ui, sans-serif" font-size="12" '
                    f'fill="#475569" text-anchor="end" transform="rotate(-90, 1100, {mid_y})">'
                    f'{escape(d["side_note"])}</text>')

    total_height = max(900, start_y + len(steps) * (step_height + gap) + 40)
    write_svg("slide_05_request_lifecycle.svg", content, height=total_height)


def render_routing(d):
    """Slide 06: Routing/dispatch — input -> matcher -> routes + detail panels."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#eab308"))

    content += rounded_rect(40, 120, 300, 60, stroke="#3b82f6")
    content += (f'<text x="190" y="156" font-family="\'JetBrains Mono\', monospace" font-size="14" '
                f'fill="#3b82f6" text-anchor="middle">{escape(d.get("input_label", "User Input"))}</text>')

    content += f'<line x1="190" y1="180" x2="190" y2="220" stroke="#334155" stroke-width="1.5"/>'
    content += f'<polygon points="185,218 190,225 195,218" fill="#334155"/>'

    content += rounded_rect(40, 225, 300, 60, stroke="#eab308")
    content += (f'<text x="190" y="261" font-family="system-ui, sans-serif" font-size="14" '
                f'font-weight="600" fill="#eab308" text-anchor="middle">{escape(d.get("matcher_label", "Pattern Matching"))}</text>')

    y = 340
    for route in d["routes"]:
        content += f'<line x1="190" y1="285" x2="190" y2="{y + 25}" stroke="#1e293b" stroke-width="1"/>'
        content += rounded_rect(40, y, 300, 55, stroke=route["color"])
        content += (f'<text x="60" y="{y + 25}" font-family="system-ui, sans-serif" font-size="14" '
                    f'font-weight="600" fill="{route["color"]}">{escape(route["name"])}</text>')
        triggers_text = ", ".join(route.get("triggers", [])[:3])
        content += (f'<text x="60" y="{y + 42}" font-family="\'JetBrains Mono\', monospace" font-size="10" '
                    f'fill="#94a3b8">{escape(triggers_text)}</text>')
        y += 90

    panel_y = 120
    for panel in d.get("detail_panels", []):
        panel_h = 40 + len(panel["lines"]) * 22
        content += rounded_rect(450, panel_y, 700, panel_h, fill="#0a0e1a", stroke="#1e293b")
        content += (f'<text x="480" y="{panel_y + 30}" font-family="system-ui, sans-serif" font-size="16" '
                    f'font-weight="600" fill="#e2e8f0">{escape(panel["title"])}</text>')
        for i, line in enumerate(panel["lines"]):
            content += (f'<text x="500" y="{panel_y + 60 + i * 22}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="12" fill="#cbd5e1">{escape(line)}</text>')
        panel_y += panel_h + 30

    total_height = max(900, max(y + 40, panel_y + 40))
    write_svg("slide_06_routing.svg", content, height=total_height)


def render_state_machines(d):
    """Slide 07: State machines — multiple state machine diagrams stacked vertically."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#06b6d4"))

    y_cursor = 100
    for machine in d["machines"]:
        content += (f'<text x="60" y="{y_cursor}" font-family="system-ui, sans-serif" font-size="18" '
                    f'font-weight="600" fill="{machine["color"]}">{escape(machine["name"])}</text>')

        state_y = y_cursor + 30
        state_h = machine.get("state_h", 50)
        state_w = machine.get("state_w", 140)

        for state in machine["states"]:
            label = state[0]
            sub = state[1] if len(state) > 1 else ""
            sx = state[2] if len(state) > 2 else 0
            sc = state[3] if len(state) > 3 else "#94a3b8"
            sh = state_h + (15 if sub else 0)
            content += rounded_rect(sx, state_y, state_w, sh, stroke=sc)
            content += (f'<text x="{sx + state_w/2}" y="{state_y + (20 if sub else state_h/2 + 5)}" '
                        f'font-family="system-ui, sans-serif" font-size="{"13" if sub else "14"}" '
                        f'font-weight="600" fill="{sc}" text-anchor="middle">{escape(label)}</text>')
            if sub:
                content += (f'<text x="{sx + state_w/2}" y="{state_y + 40}" '
                            f'font-family="\'JetBrains Mono\', monospace" font-size="10" '
                            f'fill="#94a3b8" text-anchor="middle">{escape(sub)}</text>')

        arrow_y = state_y + state_h / 2
        for trans in machine.get("transitions", []):
            x1, x2 = trans[0], trans[1]
            lbl = trans[2] if len(trans) > 2 else ""
            content += arrow_simple(x1, arrow_y, x2, arrow_y, color="#334155", label=lbl)

        if machine.get("outcomes"):
            last_state = machine["states"][-1]
            ox = last_state[2] + state_w / 2
            oy = state_y + state_h + 10
            content += f'<line x1="{ox}" y1="{state_y + state_h}" x2="{ox}" y2="{oy}" stroke="#334155" stroke-width="1.5"/>'
            for outcome in machine["outcomes"]:
                content += (f'<text x="{ox - 50}" y="{oy + 5}" font-family="\'JetBrains Mono\', monospace" '
                            f'font-size="12" font-weight="600" fill="{outcome[1]}">{escape(outcome[0])}</text>')
                oy += 20

        if machine.get("details"):
            det = machine["details"]
            det_y = state_y + state_h + 10
            det_h = 30 + len(det["items"]) * 16
            content += rounded_rect(60, det_y, 700, det_h, fill="#0a0e1a", stroke="#1e293b")
            content += (f'<text x="80" y="{det_y + 22}" font-family="system-ui, sans-serif" font-size="14" '
                        f'font-weight="600" fill="#94a3b8">{escape(det["title"])}</text>')
            for i, (lbl, desc, clr) in enumerate(det["items"]):
                content += (f'<text x="100" y="{det_y + 42 + i * 16}" font-family="\'JetBrains Mono\', monospace" '
                            f'font-size="11" fill="{clr}">{escape(lbl)}: {escape(desc)}</text>')
            y_cursor = det_y + det_h + 30
        elif machine.get("outcomes"):
            y_cursor = oy + 30
        else:
            y_cursor = state_y + state_h + 50

    write_svg("slide_07_state_machines.svg", content, height=max(900, y_cursor + 40))


def render_database_schema(d):
    """Slide 08: Database/persistence schema — tables with columns."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#06b6d4"))

    if d.get("header_note"):
        content += rounded_rect(40, 110, 1120, 80, fill="#0a0e1a", stroke="#1e293b")
        content += (f'<text x="60" y="145" font-family="system-ui, sans-serif" font-size="16" '
                    f'fill="#eab308">{escape(d["header_note"][0])}</text>')
        if len(d["header_note"]) > 1:
            content += (f'<text x="60" y="170" font-family="system-ui, sans-serif" font-size="13" '
                        f'fill="#94a3b8">{escape(d["header_note"][1])}</text>')

    for table in d["tables"]:
        x, y = table["x"], table["y"]
        w, h = table.get("w", 340), table.get("h", 200)
        color = table["color"]
        content += rounded_rect(x, y, w, h, stroke=color)
        content += (f'<text x="{x + 15}" y="{y + 25}" font-family="\'JetBrains Mono\', monospace" '
                    f'font-size="13" font-weight="600" fill="{color}">{escape(table["name"])}</text>')
        content += f'<line x1="{x + 10}" y1="{y + 35}" x2="{x + w - 15}" y2="{y + 35}" stroke="#1e293b" stroke-width="1"/>'
        for i, field in enumerate(table["fields"]):
            content += (f'<text x="{x + 15}" y="{y + 55 + i * 18}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="11" fill="#94a3b8">{escape(field)}</text>')

    if d.get("artifacts"):
        y_art = d.get("artifacts_y", 720)
        content += (f'<text x="60" y="{y_art}" font-family="system-ui, sans-serif" font-size="16" '
                    f'font-weight="600" fill="#e2e8f0">Generated Output Artifacts</text>')
        for i, (name, desc, color) in enumerate(d["artifacts"]):
            y = y_art + 25 + i * 28
            content += (f'<text x="80" y="{y}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="12" fill="{color}">{escape(name)}</text>')
            content += (f'<text x="320" y="{y}" font-family="system-ui, sans-serif" '
                        f'font-size="12" fill="#94a3b8">{escape(desc)}</text>')

    write_svg("slide_08_database_schema.svg", content)


def render_api_routes(d):
    """Slide 09: API routes/commands — grouped endpoint list + optional triggers."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#10b981"))

    y = 110
    for group in d["groups"]:
        content += (f'<text x="60" y="{y}" font-family="system-ui, sans-serif" font-size="16" '
                    f'font-weight="600" fill="{group["color"]}">{escape(group["name"])}</text>')
        y += 8
        for cmd, desc in group["routes"]:
            y += 24
            content += (f'<text x="80" y="{y}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="12" fill="#e2e8f0">{escape(cmd)}</text>')
            content += (f'<text x="{d.get("desc_x", 520)}" y="{y}" font-family="system-ui, sans-serif" '
                        f'font-size="12" fill="#94a3b8">{escape(desc)}</text>')
        y += 24

    if d.get("extra_section"):
        sec = d["extra_section"]
        sec_h = sec.get("height", 180)
        content += rounded_rect(40, y + 10, 1120, sec_h, fill="#0a0e1a", stroke="#1e293b")
        content += (f'<text x="60" y="{y + 40}" font-family="system-ui, sans-serif" font-size="14" '
                    f'font-weight="600" fill="#94a3b8">{escape(sec["title"])}</text>')
        for i, item in enumerate(sec["items"]):
            col = i % 2
            row = i // 2
            tx = 80 + col * 540
            ty = y + 65 + row * 22
            content += (f'<text x="{tx}" y="{ty}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="11" fill="#cbd5e1">{escape(item[0])}</text>')
            content += (f'<text x="{tx + 310}" y="{ty}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="11" fill="{item[2]}">{escape(item[1])}</text>')

    total_height = max(900, y + 220)
    write_svg("slide_09_api_routes.svg", content, height=total_height)


def render_code_structure(d):
    """Slide 10: Code structure — directory tree with descriptions."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#3b82f6"))

    y = 105
    for entry in d["tree"]:
        name, desc, color, indent = entry
        y += 22
        x_offset = 60 + indent * 20
        content += (f'<text x="{x_offset}" y="{y}" font-family="\'JetBrains Mono\', monospace" '
                    f'font-size="12" fill="{color}">{escape(name)}</text>')
        content += (f'<text x="{d.get("desc_x", 550)}" y="{y}" font-family="system-ui, sans-serif" '
                    f'font-size="11" fill="#94a3b8">{escape(desc)}</text>')

    if d.get("stats"):
        y += 30
        content += rounded_rect(60, y, 1080, 100, fill="#0a0e1a", stroke="#1e293b")
        content += (f'<text x="80" y="{y + 30}" font-family="system-ui, sans-serif" font-size="14" '
                    f'font-weight="600" fill="#e2e8f0">{escape(d.get("stats_title", "Codebase Statistics"))}</text>')
        for i, (stat, color) in enumerate(d["stats"]):
            sx = 100 + (i % 3) * 350
            sy = y + 55 + (i // 3) * 20
            content += (f'<text x="{sx}" y="{sy}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="12" fill="{color}">{escape(stat)}</text>')

    write_svg("slide_10_code_structure.svg", content, height=max(900, y + 160))


def render_config(d):
    """Slide 11: Config & environment — panels for settings + conventions."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#94a3b8"))

    for panel in d.get("panels", []):
        px, py = panel["x"], panel["y"]
        pw, ph = panel.get("w", 540), panel.get("h", 300)
        content += rounded_rect(px, py, pw, ph, fill="#0a0e1a", stroke=panel["color"])
        content += (f'<text x="{px + 20}" y="{py + 30}" font-family="system-ui, sans-serif" font-size="14" '
                    f'font-weight="600" fill="{panel["color"]}">{escape(panel["title"])}</text>')
        for i, item in enumerate(panel["items"]):
            content += (f'<text x="{px + 40}" y="{py + 55 + i * 22}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="11" fill="#cbd5e1">{escape(item)}</text>')

    if d.get("conventions"):
        conv_y = d.get("conventions_y", 490)
        content += (f'<text x="60" y="{conv_y}" font-family="system-ui, sans-serif" font-size="18" '
                    f'font-weight="600" fill="#3b82f6">{escape(d.get("conventions_title", "Key Conventions"))}</text>')

        for i, (name, desc, color) in enumerate(d["conventions"]):
            y = conv_y + 30 + i * 42
            content += rounded_rect(40, y, 1120, 36, stroke="#1e293b")
            content += (f'<text x="60" y="{y + 23}" font-family="system-ui, sans-serif" font-size="13" '
                        f'font-weight="600" fill="{color}">{escape(name)}</text>')
            content += (f'<text x="240" y="{y + 23}" font-family="system-ui, sans-serif" font-size="12" '
                        f'fill="#94a3b8">{escape(desc)}</text>')

    write_svg("slide_11_config.svg", content)


# ═══════════════════════════════════════════════════════════════════════════════
# RENDERER DISPATCH — maps slide numbers to render functions
# ═══════════════════════════════════════════════════════════════════════════════

RENDERERS = {
    1: render_eli5,
    2: render_system_context,
    3: render_architecture_layers,
    4: render_domain_model,
    5: render_request_lifecycle,
    6: render_routing,
    7: render_state_machines,
    8: render_database_schema,
    9: render_api_routes,
    10: render_code_structure,
    11: render_config,
}


# ═══════════════════════════════════════════════════════════════════════════════
# #### PROJECT DATA ####
# Agent — a Claude Code skills toolkit for structured thinking,
# adversarial review, rapid learning, and codebase visualization.
# ═══════════════════════════════════════════════════════════════════════════════

DATA = {
    1: {
        "title": "ELI5 -- What is Agent?",
        "subtitle": "50,000 ft -- The Big Picture",
        "accent": "#3b82f6",
        "analogy_lines": [
            "Imagine a master craftsman's toolbox -- not the kind you build things with,",
            "but the kind that teaches OTHER craftsmen how to think, analyze, and document.",
            "",
            "Agent is a collection of reusable skills for Claude Code that provide structured",
            "methodologies: adversarial review, rapid learning, and visual documentation.",
        ],
        "cards": [
            ("Debate", "The War Room", "Three-mode adversarial analysis: review, red-team, steelman", "#ef4444", ".claude/skills/debate/"),
            ("JIT Learning", "The Speed Reader", "Five-step Bloom's Taxonomy framework for rapid tech grokking", "#10b981", ".claude/skills/jit-learning/"),
            ("Visualize", "The Cartographer", "Generate SVG infographics + GSAP walkthroughs from any codebase", "#8b5cf6", ".claude/skills/visualize-codebase/"),
            ("Propose", "The Advisor", "Deep-analyze topics and propose 2-4 options with pros/cons/risk", "#eab308", ".claude/skills/propose/"),
            ("Commit", "The Scribe", "Automate structured multiline git commits with smart staging", "#06b6d4", ".claude/skills/commit/"),
            ("Gallery Index", "The Librarian", "Build multi-project visualization galleries with shared nav", "#ec4899", ".claude/skills/visualize-index/"),
        ],
        "bottom_note": "Not an application -- a methodology toolkit that extends Claude Code's capabilities.",
    },

    2: {
        "title": "System Context",
        "subtitle": "30,000 ft -- Actors and Interactions",
        "accent": "#10b981",
        "boxes": [
            {"id": "developer", "label": "Developer", "sub": "Human user", "x": 80, "y": 250, "w": 160, "h": 80, "color": "#3b82f6"},
            {"id": "claude", "label": "Claude Code", "sub": "IDE / CLI agent", "x": 350, "y": 250, "w": 200, "h": 80, "color": "#10b981"},
            {"id": "skills", "label": "Agent Skills", "sub": ".claude/skills/", "x": 350, "y": 450, "w": 200, "h": 80, "color": "#8b5cf6"},
            {"id": "codebase", "label": "Target Codebase", "sub": "Any project", "x": 700, "y": 250, "w": 200, "h": 80, "color": "#eab308"},
            {"id": "filesystem", "label": "Filesystem", "sub": "SVG, HTML, MD output", "x": 700, "y": 450, "w": 200, "h": 80, "color": "#94a3b8"},
            {"id": "gsap", "label": "GSAP CDN", "sub": "Animation library", "x": 950, "y": 350, "w": 160, "h": 70, "color": "#06b6d4"},
        ],
        "connections": [
            {"from_xy": [240, 290], "to_xy": [350, 290], "color": "#3b82f6", "label": "natural language"},
            {"from_xy": [450, 330], "to_xy": [450, 450], "color": "#8b5cf6", "label": "loads SKILL.md"},
            {"from_xy": [550, 290], "to_xy": [700, 290], "color": "#eab308", "label": "reads source"},
            {"from_xy": [550, 490], "to_xy": [700, 490], "color": "#94a3b8", "label": "writes artifacts"},
            {"from_xy": [900, 490], "to_xy": [950, 385], "color": "#06b6d4", "label": "CDN script"},
        ],
        "bottom_note": "Zero external dependencies except GSAP from CDN for interactive HTML animations.",
    },

    3: {
        "title": "Architecture Layers",
        "subtitle": "20,000 ft -- How Skills Execute",
        "accent": "#8b5cf6",
        "layers": [
            ("User Intent", "Developer invokes skill via natural language or /command", "#3b82f6"),
            ("Skill Dispatcher", "Claude Code matches intent to SKILL.md, parses $ARGUMENTS", "#10b981"),
            ("Reference Loader", "Reads methodology docs from references/ (review.md, red-team.md, etc.)", "#eab308"),
            ("Exploration Phase", "Subagents scan codebase: structure, types, routes, state machines", "#8b5cf6"),
            ("Generation Phase", "Produces artifacts: SVG slides, HTML walkthroughs, analysis reports", "#ec4899"),
            ("Validation Phase", "xmllint SVGs, template conformance, content completeness checks", "#ef4444"),
        ],
        "side_label": "Execution Flow",
    },

    4: {
        "title": "Domain Model",
        "subtitle": "15,000 ft -- Core Concepts and Relationships",
        "accent": "#ec4899",
        "entities": [
            {"name": "Skill", "fields": ["name: string", "description: string", "argument-hint: string", "allowed-tools: list"], "x": 80, "y": 120, "w": 300, "h": 130, "color": "#3b82f6"},
            {"name": "Reference", "fields": ["methodology: markdown", "framework: string", "evidence-patterns: list"], "x": 80, "y": 340, "w": 300, "h": 120, "color": "#10b981"},
            {"name": "Template", "fields": ["type: html | py | md | js", "placeholders: list", "structural-skeleton: DOM"], "x": 460, "y": 120, "w": 300, "h": 120, "color": "#8b5cf6"},
            {"name": "Visualization", "fields": ["slides: SVG[11]", "interactive: HTML", "deep-dive: HTML + MD", "gallery: HTML"], "x": 460, "y": 340, "w": 300, "h": 130, "color": "#eab308"},
            {"name": "Settings", "fields": ["permissions.allow: list", "permissions.deny: list"], "x": 830, "y": 200, "w": 280, "h": 100, "color": "#ef4444"},
        ],
        "relationships": [
            {"from_xy": [230, 250], "to_xy": [230, 340], "label": "has references", "color": "#10b981"},
            {"from_xy": [380, 180], "to_xy": [460, 180], "label": "uses templates", "color": "#8b5cf6"},
            {"from_xy": [610, 240], "to_xy": [610, 340], "label": "produces", "color": "#eab308"},
            {"from_xy": [380, 160], "to_xy": [830, 250], "label": "governed by", "color": "#ef4444"},
        ],
        "examples": [
            "Skill: /debate  ->  Reference: review.md  ->  Output: structured three-pass analysis",
            "Skill: /visualize-codebase  ->  Template: generate_visuals.py  ->  Visualization: 11 SVG slides + HTML",
        ],
        "examples_y": 530,
    },

    5: {
        "title": "Request Lifecycle",
        "subtitle": "10,000 ft -- Tracing a Codebase Visualization End-to-End",
        "accent": "#ef4444",
        "steps": [
            ("User triggers /visualize-codebase", "Developer invokes skill via natural language or slash command", "#3b82f6"),
            ("SKILL.md loaded", "Claude Code reads skill definition, parses arguments (all|static|interactive|deep-dive)", "#10b981"),
            ("Phase 0: Explore", "Subagents scan in parallel: README, entry points, types, routes, state machines, schema", "#eab308"),
            ("Phase 1: Static SVGs", "Python script generates 11 slides (50,000 ft to ground level), validated with xmllint", "#8b5cf6"),
            ("Phase 2: Interactive HTML", "GSAP-animated walkthrough with scenario tabs, actor SVGs, state inspector", "#ec4899"),
            ("Phase 3: Deep-Dive", "Markdown + HTML analysis of design decisions, invariants, failure modes", "#06b6d4"),
            ("Phase 4: Validate", "Template conformance check, content completeness, open in browser", "#ef4444"),
            ("Artifacts delivered", "visualizations/<project>/ contains index.html, interactive.html, deep-dive.html, 11 SVGs", "#94a3b8"),
        ],
        "side_note": "Sequential phases -- each builds on the previous",
    },

    6: {
        "title": "Skill Dispatch",
        "subtitle": "5,000 ft -- How Skills Get Matched and Executed",
        "accent": "#eab308",
        "input_label": "User Input (text or /command)",
        "matcher_label": "Claude Code Skill Dispatcher",
        "routes": [
            {"name": "/debate", "triggers": ["review", "red-team", "steelman"], "color": "#ef4444"},
            {"name": "/jit-learning", "triggers": ["learn", "research", "grok"], "color": "#10b981"},
            {"name": "/visualize-codebase", "triggers": ["visualize", "architecture diagrams"], "color": "#8b5cf6"},
            {"name": "/propose", "triggers": ["propose", "analyze options"], "color": "#eab308"},
            {"name": "/commit", "triggers": ["commit", "commit this"], "color": "#06b6d4"},
            {"name": "/visualize-index", "triggers": ["build the index", "rebuild index"], "color": "#ec4899"},
        ],
        "detail_panels": [
            {
                "title": "Debate Mode Selection",
                "lines": [
                    "/debate review <target>  ->  Three-pass Advocate/Critic/Judge",
                    "/debate red-team <target>  ->  5-vector attack analysis + 10th Man",
                    "/debate steelman <position>  ->  Strongest counter-argument",
                ],
            },
            {
                "title": "Visualize Phase Selection",
                "lines": [
                    "/visualize-codebase  ->  all phases (default)",
                    "/visualize-codebase static  ->  SVG infographics only",
                    "/visualize-codebase interactive  ->  GSAP walkthrough only",
                    "/visualize-codebase deep-dive  ->  analysis report only",
                ],
            },
            {
                "title": "JIT Learning Five-Step Pipeline",
                "lines": [
                    "Step 1: JIT Filter (define learning boundary)",
                    "Step 2: Macro Scan (read docs, identify pain points)",
                    "Step 3: Happy Path (execute quickstart, map lifecycle)",
                    "Step 4: Functional Decomposition (break into components)",
                    "Step 5: ELI5 Translation (mental model analogy)",
                ],
            },
        ],
    },

    7: {
        "title": "Methodological State Machines",
        "subtitle": "3,000 ft -- Lifecycle States Within Each Skill",
        "accent": "#06b6d4",
        "machines": [
            {
                "name": "Debate Review (Three-Pass)",
                "color": "#ef4444",
                "state_w": 160,
                "states": [
                    ("Pass 1: Advocate", "steelman the artifact", 60, "#10b981"),
                    ("Pass 2: Critic", "find real problems", 300, "#eab308"),
                    ("Pass 3: Judge", "dialectical synthesis", 540, "#ef4444"),
                ],
                "transitions": [
                    (220, 300, "hand off"),
                    (460, 540, "resolve"),
                ],
                "outcomes": [
                    ("SHIP", "#10b981"),
                    ("SHIP WITH FIXES", "#eab308"),
                    ("REDESIGN", "#ef4444"),
                ],
            },
            {
                "name": "Red Team (Attack Vectors)",
                "color": "#8b5cf6",
                "state_w": 160,
                "states": [
                    ("Input Bounds", "nil/max/malformed", 60, "#3b82f6"),
                    ("State/Concur.", "race/TOCTOU", 260, "#10b981"),
                    ("Failure Cascade", "retry storms", 460, "#eab308"),
                    ("Security", "injection/auth", 660, "#ef4444"),
                    ("Operational", "observability", 860, "#8b5cf6"),
                ],
                "transitions": [
                    (220, 260, ""),
                    (420, 460, ""),
                    (620, 660, ""),
                    (820, 860, ""),
                ],
                "details": {
                    "title": "Severity Classification",
                    "items": [
                        ("P0", "Critical: exploitable in production, data loss, security breach", "#ef4444"),
                        ("P1", "High: likely to cause incidents under load or edge cases", "#eab308"),
                        ("P2", "Medium: correctness issue with workaround", "#3b82f6"),
                        ("P3", "Low: style, maintainability, or theoretical concern", "#94a3b8"),
                    ],
                },
            },
            {
                "name": "JIT Learning (Bloom's Taxonomy Progression)",
                "color": "#10b981",
                "state_w": 160,
                "states": [
                    ("JIT Filter", "Remember", 60, "#94a3b8"),
                    ("Macro Scan", "Understand", 260, "#3b82f6"),
                    ("Happy Path", "Apply", 460, "#10b981"),
                    ("Decompose", "Analyze", 660, "#eab308"),
                    ("ELI5", "Evaluate", 860, "#ec4899"),
                ],
                "transitions": [
                    (220, 260, ""),
                    (420, 460, ""),
                    (620, 660, ""),
                    (820, 860, ""),
                ],
            },
        ],
    },

    8: {
        "title": "Persistence Schema",
        "subtitle": "1,000 ft -- File-Based Data Structures (No Database)",
        "accent": "#06b6d4",
        "header_note": [
            "Agent has no database -- all state is file-based.",
            "Skills read from .claude/ and write to visualizations/ or stdout.",
        ],
        "tables": [
            {
                "name": "SKILL.md (Frontmatter)",
                "fields": [
                    "name: string (skill identifier)",
                    "description: string (trigger patterns)",
                    "argument-hint: string (usage hint)",
                    "allowed-tools: list (tool whitelist)",
                ],
                "color": "#3b82f6", "x": 40, "y": 220, "w": 360, "h": 140,
            },
            {
                "name": "settings.json",
                "fields": [
                    "permissions.allow: string[] (Bash patterns)",
                    "permissions.deny: string[] (Bash patterns)",
                ],
                "color": "#ef4444", "x": 420, "y": 220, "w": 360, "h": 100,
            },
            {
                "name": "DATA dict (generate_visuals.py)",
                "fields": [
                    "1-11: dict (one per slide)",
                    "title, subtitle, accent: string",
                    "cards | boxes | layers | entities: list",
                    "connections | relationships | steps: list",
                ],
                "color": "#8b5cf6", "x": 40, "y": 400, "w": 360, "h": 140,
            },
            {
                "name": "SCENARIOS array (interactive.html)",
                "fields": [
                    "id: string, label: string, color: hex",
                    "actors: [{id, label, sub, x, y, color}]",
                    "steps: [{from, to, label, narration,",
                    "         detail, state}]",
                ],
                "color": "#eab308", "x": 420, "y": 400, "w": 360, "h": 140,
            },
        ],
        "artifacts": [
            ("slide_01..11.svg", "SVG infographics (11 altitude-descent slides)", "#8b5cf6"),
            ("index.html", "Slideshow viewer with thumbnail sidebar", "#3b82f6"),
            ("interactive.html", "GSAP-animated scenario walkthrough", "#10b981"),
            ("deep-dive.html", "Styled analysis report (design decisions, invariants, failures)", "#eab308"),
            ("deep-dive.md", "Markdown source for deep-dive analysis", "#94a3b8"),
        ],
        "artifacts_y": 590,
    },

    9: {
        "title": "Skill Command Map",
        "subtitle": "500 ft -- Every Skill Entry Point and Its Triggers",
        "accent": "#10b981",
        "desc_x": 520,
        "groups": [
            {
                "name": "Adversarial Analysis",
                "color": "#ef4444",
                "routes": [
                    ("/debate review <target>", "Three-pass Advocate/Critic/Judge review"),
                    ("/debate red-team <target>", "5-vector attack analysis with 10th Man Rule"),
                    ("/debate steelman <position>", "Strongest counter-argument construction"),
                ],
            },
            {
                "name": "Learning & Analysis",
                "color": "#10b981",
                "routes": [
                    ("/jit-learning <topic>", "Five-step Bloom's Taxonomy learning framework"),
                    ("/propose <topic>", "2-4 implementation options with pros/cons/risk"),
                ],
            },
            {
                "name": "Visualization",
                "color": "#8b5cf6",
                "routes": [
                    ("/visualize-codebase", "All phases: SVG + interactive + deep-dive"),
                    ("/visualize-codebase static", "SVG infographics only (11 slides)"),
                    ("/visualize-codebase interactive", "GSAP animated walkthrough only"),
                    ("/visualize-codebase deep-dive", "Analysis report only"),
                    ("/visualize-index", "Build gallery index for all projects"),
                ],
            },
            {
                "name": "Git Operations",
                "color": "#06b6d4",
                "routes": [
                    ("/commit <message>", "Multiline commit with auto-generated bullet body"),
                ],
            },
        ],
        "extra_section": {
            "title": "Natural Language Triggers (also match these skills)",
            "height": 140,
            "items": [
                ('"review this code"', "/debate review", "#ef4444"),
                ('"break this"', "/debate red-team", "#ef4444"),
                ('"argue against this"', "/debate steelman", "#ef4444"),
                ('"learn X" / "grok X"', "/jit-learning", "#10b981"),
                ('"how should we implement"', "/propose", "#eab308"),
                ('"visualize this codebase"', "/visualize-codebase", "#8b5cf6"),
                ('"build the index"', "/visualize-index", "#ec4899"),
                ('"commit this"', "/commit", "#06b6d4"),
            ],
        },
    },

    10: {
        "title": "Code Structure",
        "subtitle": "100 ft -- Every Directory and Its Purpose",
        "accent": "#3b82f6",
        "desc_x": 550,
        "tree": [
            (".claude/", "Claude Code configuration root", "#3b82f6", 0),
            ("  CLAUDE.md", "Operating principles, workflow, conventions", "#3b82f6", 1),
            ("  CLAUDE_lessons.md", "Postmortem insights and prevention rules", "#ef4444", 1),
            ("  settings.json", "Bash permission allow/deny whitelist", "#ef4444", 1),
            ("  skills/", "All skill definitions", "#8b5cf6", 1),
            ("    commit/", "Git commit automation", "#06b6d4", 2),
            ("      SKILL.md", "Multiline commit + staged file handling", "#06b6d4", 3),
            ("    debate/", "Adversarial analysis toolkit", "#ef4444", 2),
            ("      SKILL.md", "Three modes: review, red-team, steelman", "#ef4444", 3),
            ("      references/", "Methodology docs (3 files)", "#ef4444", 3),
            ("    jit-learning/", "Rapid technology learning", "#10b981", 2),
            ("      SKILL.md", "Five-step Bloom's Taxonomy framework", "#10b981", 3),
            ("      references/", "JIT learning theory (1 file)", "#10b981", 3),
            ("    propose/", "Implementation option analysis", "#eab308", 2),
            ("      SKILL.md", "Deep-analyze + propose 2-4 options", "#eab308", 3),
            ("    visualize-codebase/", "Codebase visualization generator", "#8b5cf6", 2),
            ("      SKILL.md", "4-phase: explore, static, interactive, deep-dive", "#8b5cf6", 3),
            ("      templates/", "4 files: py, 3x html", "#8b5cf6", 3),
            ("    visualize-index/", "Multi-project gallery builder", "#ec4899", 2),
            ("      SKILL.md", "Discover folders, extract metadata, build gallery", "#ec4899", 3),
            ("      templates/", "5 files: html, js, md", "#ec4899", 3),
            ("Makefile", "Copy targets for distributing .claude/ assets", "#94a3b8", 0),
            ("README.md", "Project overview and installation instructions", "#94a3b8", 0),
            ("RELEASE_NOTES.md", "Version history (v1.0.0)", "#94a3b8", 0),
        ],
        "stats": [
            ("6 skills", "#3b82f6"),
            ("18 files total", "#10b981"),
            ("~2,500 lines (skills + templates)", "#8b5cf6"),
            ("0 external pip/npm deps", "#ef4444"),
            ("1 CDN dependency (GSAP)", "#eab308"),
            ("Apache 2.0 license", "#94a3b8"),
        ],
        "stats_title": "Repository Statistics",
    },

    11: {
        "title": "Config & Environment",
        "subtitle": "Ground Level -- Operational Knobs",
        "accent": "#94a3b8",
        "panels": [
            {
                "title": "Bash Permission Allow List (settings.json)",
                "color": "#10b981",
                "x": 40, "y": 120, "w": 540, "h": 340,
                "items": [
                    "Bash(grep *) -- file content search",
                    "Bash(find *) -- file discovery",
                    "Bash(python3 */generate_visuals.py) -- SVG generation",
                    "Bash(open */visualizations/*) -- open HTML in browser",
                    "Bash(xmllint *) -- SVG XML validation",
                    "Bash(go build/test/vet) -- Go toolchain",
                    "Bash(make build/test/lint) -- Makefile targets",
                    "Bash(git status/diff/log) -- read-only git",
                    "Bash(kubectl *) -- Kubernetes read-only",
                    "Bash(helm list/status/show) -- Helm read-only",
                ],
            },
            {
                "title": "Bash Permission Deny List (settings.json)",
                "color": "#ef4444",
                "x": 620, "y": 120, "w": 540, "h": 200,
                "items": [
                    "Bash(git push *) -- no remote pushes",
                    "Bash(git reset --hard *) -- no destructive resets",
                    "Bash(rm -rf *) -- no recursive deletes",
                    "Bash(helm install/upgrade/uninstall) -- no cluster changes",
                    "Bash(make docker-reset) -- no container resets",
                ],
            },
            {
                "title": "Makefile Distribution Targets",
                "color": "#eab308",
                "x": 620, "y": 340, "w": 540, "h": 120,
                "items": [
                    "make copy-claude-all -- copy entire .claude/ to ~/.claude/",
                    "make copy-claude-skill SKILL=<name> -- copy one skill",
                    "make copy-claude-skills -- copy all skills",
                ],
            },
        ],
        "conventions": [
            ("Zero Dependencies", "Python SVG generation uses only stdlib; no pip install needed", "#10b981"),
            ("Template Fidelity", "Generated HTML must match canonical template skeleton exactly", "#3b82f6"),
            ("XML Escape", "All SVG text goes through xml.sax.saxutils.escape()", "#eab308"),
            ("Skill Isolation", "Each skill is self-contained; can be installed independently", "#8b5cf6"),
            ("Permission Model", "Deny-by-default; only explicit allows in settings.json execute", "#ef4444"),
        ],
        "conventions_y": 500,
        "conventions_title": "Key Conventions",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — generate all slides
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    count = 0
    for slide_num in sorted(RENDERERS.keys()):
        if slide_num in DATA:
            RENDERERS[slide_num](DATA[slide_num])
            count += 1
    print(f"Generated {count} slides in {OUTPUT_DIR}/")
