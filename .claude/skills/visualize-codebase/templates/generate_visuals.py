#!/usr/bin/env python3
"""Template for generating SVG infographic slides for any codebase visualization.

USAGE FOR LLM:
  1. Copy this file to visualizations/<project>/generate_visuals.py
  2. Replace the DATA dict at the bottom (marked with #### PROJECT DATA ####)
     with project-specific content from Phase 0 exploration.
  3. Run: python3 generate_visuals.py

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
        # box: {id, label, sub, x, y, w, h, color}
        content += box_with_label(
            box["x"], box["y"], box.get("w", 160), box.get("h", 70),
            box["label"], box.get("sub", ""),
            stroke=box["color"], text_color=box["color"]
        )

    # Render connections
    for conn in d.get("connections", []):
        # conn: {from_xy, to_xy, color, label}
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

    layers = d["layers"]  # list of (label, description, color)
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

    # Downward arrows between layers
    for i in range(len(layers) - 1):
        y1 = start_y + i * (layer_height + gap) + layer_height
        y2 = start_y + (i + 1) * (layer_height + gap)
        content += (f'<line x1="600" y1="{y1}" x2="600" y2="{y2}" '
                    f'stroke="#334155" stroke-width="1.5" stroke-dasharray="4,4"/>')
        content += f'<polygon points="595,{y2 - 5} 600,{y2} 605,{y2 - 5}" fill="#334155"/>'

    # Side annotation
    mid_y = start_y + (len(layers) * (layer_height + gap)) / 2
    content += (f'<text x="1140" y="{mid_y}" font-family="system-ui, sans-serif" font-size="11" '
                f'fill="#475569" text-anchor="end" transform="rotate(-90, 1140, {mid_y})">'
                f'{escape(d.get("side_label", "Request Flow"))}</text>')

    total_height = max(900, start_y + len(layers) * (layer_height + gap) + 40)
    write_svg("slide_03_architecture_layers.svg", content, height=total_height)


def render_domain_model(d):
    """Slide 04: Domain model — entity boxes with fields and relationships."""
    content = title_bar(d["title"], d["subtitle"], accent=d.get("accent", "#ec4899"))

    # Render entities
    for entity in d["entities"]:
        # entity: {name, fields: [str], x, y, w, h, color}
        x, y = entity["x"], entity["y"]
        w, h = entity.get("w", 280), entity.get("h", 120)
        color = entity["color"]
        content += rounded_rect(x, y, w, h, stroke=color)
        content += (f'<text x="{x + w/2}" y="{y + 30}" font-family="system-ui, sans-serif" font-size="18" '
                    f'font-weight="700" fill="{color}" text-anchor="middle">{escape(entity["name"])}</text>')
        for i, field in enumerate(entity.get("fields", [])):
            content += (f'<text x="{x + 20}" y="{y + 55 + i * 18}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="11" fill="#94a3b8">{escape(field)}</text>')

    # Render relationships
    for rel in d.get("relationships", []):
        # rel: {from_xy, to_xy, label, color}
        fx, fy = rel["from_xy"]
        tx, ty = rel["to_xy"]
        content += arrow_simple(fx, fy, tx, ty, color=rel.get("color", "#94a3b8"), label=rel.get("label", ""))

    # Optional examples box
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

    steps = d["steps"]  # list of (label, description, color)
    step_height = 70
    gap = 20
    start_y = 120

    for i, (label, desc, color) in enumerate(steps):
        y = start_y + i * (step_height + gap)
        num = str(i + 1)

        # Step number circle
        content += f'<circle cx="80" cy="{y + 25}" r="20" fill="{color}" opacity="0.15"/>'
        content += (f'<text x="80" y="{y + 30}" font-family="system-ui, sans-serif" font-size="16" '
                    f'font-weight="700" fill="{color}" text-anchor="middle">{num}</text>')

        # Step content
        content += (f'<text x="120" y="{y + 22}" font-family="system-ui, sans-serif" font-size="16" '
                    f'font-weight="600" fill="#e2e8f0">{escape(label)}</text>')
        content += (f'<text x="120" y="{y + 44}" font-family="system-ui, sans-serif" font-size="13" '
                    f'fill="#94a3b8">{escape(desc)}</text>')

        # Connector line
        if i < len(steps) - 1:
            content += f'<line x1="80" y1="{y + 50}" x2="80" y2="{y + step_height + gap - 5}" stroke="#334155" stroke-width="1.5"/>'

    # Side annotation
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

    # Input box
    content += rounded_rect(40, 120, 300, 60, stroke="#3b82f6")
    content += (f'<text x="190" y="156" font-family="\'JetBrains Mono\', monospace" font-size="14" '
                f'fill="#3b82f6" text-anchor="middle">{escape(d.get("input_label", "User Input"))}</text>')

    # Arrow to matcher
    content += f'<line x1="190" y1="180" x2="190" y2="220" stroke="#334155" stroke-width="1.5"/>'
    content += f'<polygon points="185,218 190,225 195,218" fill="#334155"/>'

    # Matcher box
    content += rounded_rect(40, 225, 300, 60, stroke="#eab308")
    content += (f'<text x="190" y="261" font-family="system-ui, sans-serif" font-size="14" '
                f'font-weight="600" fill="#eab308" text-anchor="middle">{escape(d.get("matcher_label", "Pattern Matching"))}</text>')

    # Route entries (left column)
    y = 340
    for route in d["routes"]:
        # route: {name, triggers: [str], color}
        content += f'<line x1="190" y1="285" x2="190" y2="{y + 25}" stroke="#1e293b" stroke-width="1"/>'
        content += rounded_rect(40, y, 300, 55, stroke=route["color"])
        content += (f'<text x="60" y="{y + 25}" font-family="system-ui, sans-serif" font-size="14" '
                    f'font-weight="600" fill="{route["color"]}">{escape(route["name"])}</text>')
        triggers_text = ", ".join(route.get("triggers", [])[:3])
        content += (f'<text x="60" y="{y + 42}" font-family="\'JetBrains Mono\', monospace" font-size="10" '
                    f'fill="#94a3b8">{escape(triggers_text)}</text>')
        y += 90

    # Detail panels (right side)
    panel_y = 120
    for panel in d.get("detail_panels", []):
        # panel: {title, lines: [str]}
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
        # machine: {name, color, states: [(label, sub, x, color)], transitions: [(from_x, to_x, label)],
        #           outcomes: [(label, color)] (optional), details: {title, items: [(label, desc, color)]} (optional)}
        content += (f'<text x="60" y="{y_cursor}" font-family="system-ui, sans-serif" font-size="18" '
                    f'font-weight="600" fill="{machine["color"]}">{escape(machine["name"])}</text>')

        state_y = y_cursor + 30
        state_h = machine.get("state_h", 50)
        state_w = machine.get("state_w", 140)

        # Draw states
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

        # Draw transitions (horizontal arrows between consecutive states)
        arrow_y = state_y + state_h / 2
        for trans in machine.get("transitions", []):
            x1, x2 = trans[0], trans[1]
            lbl = trans[2] if len(trans) > 2 else ""
            content += arrow_simple(x1, arrow_y, x2, arrow_y, color="#334155", label=lbl)

        # Outcomes (optional, below last state)
        if machine.get("outcomes"):
            last_state = machine["states"][-1]
            ox = last_state[2] + state_w / 2
            oy = state_y + state_h + 10
            content += f'<line x1="{ox}" y1="{state_y + state_h}" x2="{ox}" y2="{oy}" stroke="#334155" stroke-width="1.5"/>'
            for outcome in machine["outcomes"]:
                content += (f'<text x="{ox - 50}" y="{oy + 5}" font-family="\'JetBrains Mono\', monospace" '
                            f'font-size="12" font-weight="600" fill="{outcome[1]}">{escape(outcome[0])}</text>')
                oy += 20

        # Detail box (optional)
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

    # Optional header note
    if d.get("header_note"):
        content += rounded_rect(40, 110, 1120, 80, fill="#0a0e1a", stroke="#1e293b")
        content += (f'<text x="60" y="145" font-family="system-ui, sans-serif" font-size="16" '
                    f'fill="#eab308">{escape(d["header_note"][0])}</text>')
        if len(d["header_note"]) > 1:
            content += (f'<text x="60" y="170" font-family="system-ui, sans-serif" font-size="13" '
                        f'fill="#94a3b8">{escape(d["header_note"][1])}</text>')

    # Render tables
    for table in d["tables"]:
        # table: {name, fields: [str], color, x, y, w, h}
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

    # Output artifacts section (optional)
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
        # group: {name, color, routes: [(command, description)]}
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

    # Optional natural language triggers or secondary section
    if d.get("extra_section"):
        sec = d["extra_section"]
        sec_h = sec.get("height", 180)
        content += rounded_rect(40, y + 10, 1120, sec_h, fill="#0a0e1a", stroke="#1e293b")
        content += (f'<text x="60" y="{y + 40}" font-family="system-ui, sans-serif" font-size="14" '
                    f'font-weight="600" fill="#94a3b8">{escape(sec["title"])}</text>')
        for i, item in enumerate(sec["items"]):
            # item: (left_text, right_text, color)
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
        # entry: (name, description, color, indent_level)
        name, desc, color, indent = entry
        y += 22
        x_offset = 60 + indent * 20
        content += (f'<text x="{x_offset}" y="{y}" font-family="\'JetBrains Mono\', monospace" '
                    f'font-size="12" fill="{color}">{escape(name)}</text>')
        content += (f'<text x="{d.get("desc_x", 550)}" y="{y}" font-family="system-ui, sans-serif" '
                    f'font-size="11" fill="#94a3b8">{escape(desc)}</text>')

    # Stats box (optional)
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

    # Config panels (side-by-side or stacked)
    for panel in d.get("panels", []):
        # panel: {title, color, x, y, w, h, items: [str]}
        px, py = panel["x"], panel["y"]
        pw, ph = panel.get("w", 540), panel.get("h", 300)
        content += rounded_rect(px, py, pw, ph, fill="#0a0e1a", stroke=panel["color"])
        content += (f'<text x="{px + 20}" y="{py + 30}" font-family="system-ui, sans-serif" font-size="14" '
                    f'font-weight="600" fill="{panel["color"]}">{escape(panel["title"])}</text>')
        for i, item in enumerate(panel["items"]):
            content += (f'<text x="{px + 40}" y="{py + 55 + i * 22}" font-family="\'JetBrains Mono\', monospace" '
                        f'font-size="11" fill="#cbd5e1">{escape(item)}</text>')

    # Conventions section (optional)
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
# Replace everything below this line with project-specific data from Phase 0.
# Each key (1-11) maps to the data dict for that slide's renderer.
# ═══════════════════════════════════════════════════════════════════════════════

DATA = {
    1: {
        "title": "ELI5 — What is ProjectName?",
        "subtitle": "50,000 ft — The Big Picture",
        "accent": "#3b82f6",
        "analogy_lines": [
            "Imagine a ... (real-world analogy explaining what the system does).",
            "It works by ...",
            "",
            '  "Key insight one."  "Key insight two."',
        ],
        "cards": [
            # (name, metaphor, description, color, optional_path_hint)
            ("Feature A", "The Analogy", "What it does in one line", "#ef4444", "src/feature_a/"),
            ("Feature B", "The Analogy", "What it does in one line", "#10b981", "src/feature_b/"),
            ("Feature C", "The Analogy", "What it does in one line", "#eab308", "src/feature_c/"),
        ],
        "bottom_note": "One-line summary of the project's nature or key constraint.",
    },

    2: {
        "title": "System Context",
        "subtitle": "30,000 ft — Actors and Interactions",
        "accent": "#10b981",
        "boxes": [
            # {id, label, sub, x, y, w, h, color}
            {"id": "user", "label": "User", "sub": "Human", "x": 80, "y": 350, "w": 160, "h": 80, "color": "#3b82f6"},
            {"id": "api", "label": "API Server", "sub": "Go / Node", "x": 350, "y": 350, "w": 200, "h": 80, "color": "#10b981"},
            {"id": "db", "label": "Database", "sub": "PostgreSQL", "x": 350, "y": 550, "w": 200, "h": 70, "color": "#94a3b8"},
        ],
        "connections": [
            # {from_xy, to_xy, color, label}
            {"from_xy": [240, 390], "to_xy": [350, 390], "color": "#3b82f6", "label": "HTTP"},
            {"from_xy": [450, 430], "to_xy": [450, 550], "color": "#94a3b8", "label": "SQL"},
        ],
        "bottom_note": "Summary of external dependencies and protocol choices.",
    },

    3: {
        "title": "Architecture Layers",
        "subtitle": "20,000 ft — How Requests Flow",
        "accent": "#8b5cf6",
        "layers": [
            # (label, description, color)
            ("HTTP Layer", "Routing, middleware, request parsing", "#3b82f6"),
            ("Handler", "HTTP concerns: status codes, serialization", "#10b981"),
            ("Service", "Business logic, validation, orchestration", "#eab308"),
            ("Store", "Database queries, data access", "#8b5cf6"),
        ],
        "side_label": "Request Flow",
    },

    4: {
        "title": "Domain Model",
        "subtitle": "15,000 ft — Core Concepts and Relationships",
        "accent": "#ec4899",
        "entities": [
            # {name, fields, x, y, w, h, color}
            {"name": "EntityA", "fields": ["id: uuid", "name: string", "status: enum"], "x": 450, "y": 130, "w": 280, "h": 120, "color": "#eab308"},
            {"name": "EntityB", "fields": ["id: uuid", "entity_a_id: uuid"], "x": 80, "y": 320, "w": 280, "h": 100, "color": "#8b5cf6"},
        ],
        "relationships": [
            # {from_xy, to_xy, label, color}
            {"from_xy": [450, 250], "to_xy": [220, 320], "label": "has many", "color": "#8b5cf6"},
        ],
        "examples": [
            "EntityA: order  ->  EntityB: line_item  ->  Product: widget",
        ],
        "examples_y": 520,
    },

    5: {
        "title": "Request Lifecycle",
        "subtitle": "10,000 ft — Tracing the Primary Use Case End-to-End",
        "accent": "#ef4444",
        "steps": [
            # (label, description, color)
            ("Step one", "Description of what happens", "#3b82f6"),
            ("Step two", "Description of what happens", "#10b981"),
            ("Step three", "Description of what happens", "#eab308"),
        ],
        "side_note": "Single synchronous flow — no async, no queuing",
    },

    6: {
        "title": "Routing / Dispatch",
        "subtitle": "5,000 ft — How Requests Get Matched",
        "accent": "#eab308",
        "input_label": "User Input (text or /command)",
        "matcher_label": "Pattern Matching",
        "routes": [
            # {name, triggers, color}
            {"name": "route-a", "triggers": ["GET /api/a", "POST /api/a"], "color": "#ef4444"},
            {"name": "route-b", "triggers": ["GET /api/b"], "color": "#10b981"},
        ],
        "detail_panels": [
            # {title, lines}
            {
                "title": "Example: Route A Detail",
                "lines": [
                    "GET /api/a -> handler.ListA()",
                    "POST /api/a -> handler.CreateA()",
                ],
            },
        ],
    },

    7: {
        "title": "State Machines",
        "subtitle": "3,000 ft — Lifecycle States and Transitions",
        "accent": "#06b6d4",
        "machines": [
            # Each machine: {name, color, states, transitions, outcomes (optional), details (optional)}
            {
                "name": "Order Lifecycle",
                "color": "#ef4444",
                "states": [
                    # (label, sub, x, color)
                    ("Created", "", 80, "#94a3b8"),
                    ("Processing", "", 300, "#3b82f6"),
                    ("Complete", "", 520, "#10b981"),
                ],
                "transitions": [
                    # (from_right_edge_x, to_left_edge_x, label)
                    (220, 300, "submit"),
                    (440, 520, "fulfill"),
                ],
                "outcomes": [
                    # (label, color)
                    ("SUCCESS", "#10b981"),
                    ("FAILED", "#ef4444"),
                ],
            },
        ],
    },

    8: {
        "title": "Database Schema",
        "subtitle": "1,000 ft — Tables, Columns, and Indexes",
        "accent": "#06b6d4",
        "header_note": None,  # or ["Title line", "Subtitle line"]
        "tables": [
            # {name, fields, color, x, y, w, h}
            {"name": "orders", "fields": ["id: uuid PK", "status: text", "created_at: timestamptz"], "color": "#eab308", "x": 40, "y": 120, "w": 340, "h": 120},
            {"name": "line_items", "fields": ["id: uuid PK", "order_id: uuid FK", "product: text", "qty: int"], "color": "#8b5cf6", "x": 420, "y": 120, "w": 340, "h": 140},
        ],
        "artifacts": None,  # or list of (name, desc, color)
        "artifacts_y": 720,
    },

    9: {
        "title": "API Route Map",
        "subtitle": "500 ft — Every Endpoint Grouped by Concern",
        "accent": "#10b981",
        "desc_x": 520,
        "groups": [
            # {name, color, routes: [(command, description)]}
            {
                "name": "Orders",
                "color": "#eab308",
                "routes": [
                    ("GET    /api/v1/orders", "List orders with pagination"),
                    ("POST   /api/v1/orders", "Create a new order"),
                    ("GET    /api/v1/orders/{id}", "Get order by ID"),
                ],
            },
        ],
        "extra_section": None,  # or {title, height, items: [(left, right, color)]}
    },

    10: {
        "title": "Code Structure",
        "subtitle": "100 ft — Every Directory and Its Purpose",
        "accent": "#3b82f6",
        "desc_x": 550,
        "tree": [
            # (name, description, color, indent_level)
            ("cmd/", "Application entry points", "#eab308", 0),
            ("  api/", "HTTP server main.go", "#eab308", 1),
            ("internal/", "Private application code", "#3b82f6", 0),
            ("  handler/", "HTTP handlers", "#10b981", 1),
            ("  service/", "Business logic", "#8b5cf6", 1),
            ("  store/", "Database queries", "#ec4899", 1),
        ],
        "stats": [
            # (stat_text, color)
            ("12 packages", "#eab308"),
            ("~5000 lines Go", "#10b981"),
            ("85% test coverage", "#3b82f6"),
        ],
        "stats_title": "Codebase Statistics",
    },

    11: {
        "title": "Config & Environment",
        "subtitle": "Ground Level — Operational Knobs",
        "accent": "#94a3b8",
        "panels": [
            # {title, color, x, y, w, h, items}
            {
                "title": "Environment Variables",
                "color": "#10b981",
                "x": 40, "y": 140, "w": 540, "h": 300,
                "items": [
                    "DATABASE_URL — PostgreSQL connection string",
                    "PORT — HTTP listen port (default: 8080)",
                    "LOG_LEVEL — slog level (debug/info/warn/error)",
                ],
            },
        ],
        "conventions": [
            # (name, description, color)
            ("Error handling", "fmt.Errorf(\"context: %w\", err) — always wrap", "#ef4444"),
            ("Testing", "Collocated *_test.go, integration tests hit real DB", "#8b5cf6"),
        ],
        "conventions_y": 490,
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
