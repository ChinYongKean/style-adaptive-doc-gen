---
type: Generator
title: "Architecture Diagrams"
description: "Generates .drawio XML diagrams with bombastic visual standards."
tags: [diagram, drawio, architecture, visual]
timestamp: 2026-06-29T12:00:00+08:00
---

# Generator: Architecture Diagrams

## Output Format
`.drawio` XML — editable in draw.io, VS Code extension, or diagrams.net

## Input Required
1. **Style profile** — `diagrams` section (icon format, flow direction, colors, canvas size)
2. **Content** — components list, connections, groupings

## Generation Rules

### Layout (from style profile)
- `flow_direction`: top-down or left-right determines primary axis
- `numbered_flow`: if true, add circled number labels on edges (① ② ③)
- `legend`: if true, add a step-by-step explanation panel on the right side
- `title_block`: if true, add bold title + subtitle at top of canvas

### Visual Quality Standards ("Bombastic" Level)

**Modern Professional Style — Monochrome + Single Accent:**

Color palette:
```
DARK    = #1B2838   (headings, primary text)
MID     = #4A5568   (numbered circles, secondary)
LIGHT   = #A0AEC0   (labels, arrows, borders)
SURFACE = #F7FAFC   (container backgrounds)
BORDER  = #E2E8F0   (card borders, dividers)
ACCENT  = #2B6CB0   (highlighted step, primary arrows)
CARD_BG = #FFFFFF   (component cards)
```

Rules:
1. **Big numbered circles** — 50-55px dark circles with white 18px bold numbers
2. **Highlighted step** — ONE key step gets accent color circle + border (the "hero")
3. **White cards** — rounded rects with subtle #E2E8F0 borders
4. **Monochrome arrows** — #A0AEC0 for normal, #2B6CB0 accent for primary path
5. **Dashed containers** — group boundaries use dashed light borders, NOT solid fills
6. **Phase labels** — tiny 8px caps in #A0AEC0: "PARALLEL", "SEQUENTIAL"
7. **Minimal text** — bold title + small gray subtitle, no verbose descriptions
8. **Right-side legend** — clean ① ② ③ step list in #4A5568
9. **Key insight box** — accent-bordered card with one core takeaway
10. **No rainbow** — ONE accent color, rest is grayscale. Never multiple saturated colors.

For **AWS infrastructure diagrams** specifically, use color-coded zones (green/blue/pink) as they follow AWS official conventions. The modern monochrome style is for product/flow/system diagrams.

### Icon Rendering
Apply from style profile `diagrams.icon_format`:
- `productIcon`: `shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.<service>`
- `resourceIcon`: `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<service>`
- For generic (non-cloud) diagrams: use standard draw.io shapes

### Mandatory Elements
```
Every diagram MUST include:
□ Title block (name + date + version)
□ Background rectangle (light gray, prevents black PNG export)
□ Proper icon fill colors by category
□ Edge labels (short, 1-2 words)
□ Boundary containers with labels
□ No XML comments (causes parse errors)
□ Unique cell IDs
□ Every edge has <mxGeometry relative="1" as="geometry" />
```

### Canvas Sizing
```
Simple (5-10 components):  pageWidth="1600" pageHeight="1200"
Medium (10-20 components): pageWidth="2400" pageHeight="1600"
Complex (20+ components):  pageWidth="3200" pageHeight="2000"
```

## Template

```xml
<mxfile host="app.diagrams.net">
  <diagram id="diagram-1" name="[TITLE]">
    <mxGraphModel dx="2800" dy="1600" grid="1" gridSize="10" guides="1"
      tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1"
      pageWidth="2400" pageHeight="1400" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Background -->
        <mxCell id="bg" value="" style="rounded=1;whiteSpace=wrap;fillColor=#F5F5F5;strokeColor=#E0E0E0;arcSize=2;" vertex="1" parent="1">
          <mxGeometry x="0" y="0" width="2400" height="1400" as="geometry" />
        </mxCell>
        <!-- Title Block -->
        <mxCell id="title" value="&lt;b&gt;[DIAGRAM TITLE]&lt;/b&gt;&lt;br&gt;[Author] | [Date] | [Version]" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=14;spacing=8;" vertex="1" parent="1">
          <mxGeometry x="40" y="30" width="420" height="60" as="geometry" />
        </mxCell>
        <!-- Components and edges here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Validation
After generation, verify:
1. Parse XML with ElementTree (must not throw)
2. Count icons, edges, containers
3. Check all edge source/target reference valid cell IDs
4. Verify no empty `value=""` on edges

## MANDATORY: Visualize and Trace Every Arrow

After generating ANY .drawio file, you MUST:

1. **Export or render to PNG** (resize to 1200px max if needed for agent reading)
2. **Visually inspect the rendered image** using the Image read tool
3. **Trace every arrow** and verify:
   - Arrow does NOT pass through/over any icon
   - Arrow does NOT merge or overlap with another arrow
   - Arrow connects the correct source → target
   - Arrow exits from the correct side of the source (right for horizontal flow, bottom for vertical)
   - Arrow enters the correct side of the target
4. **If arrows overlap icons**: fix by using explicit `exitX/exitY` + `entryX/entryY` with offset values AND add `<Array as="points">` waypoints to route around icons
5. **If image tool fails** (large image): resize first using PIL → /tmp/resized.png, THEN read

### Arrow Routing Rules (Prevent Overlap)
```
HORIZONTAL flow (left→right): exitX=1;exitY=0.5 → entryX=0;entryY=0.5
VERTICAL flow (top→down):     exitX=0.5;exitY=1 → entryX=0.5;entryY=0
MULTIPLE to same target:      Offset entryY (0.3, 0.5, 0.7) to separate
LOOP-BACK arrows:             Route via right/left side with explicit waypoints
NEVER let auto-routing decide for cross-component edges
```

### Image Reading for Verification
```python
# If drawio export produces large PNG (>4000px), resize first:
from PIL import Image
img = Image.open('diagram.png')
if img.size[0] > 1200:
    ratio = 1200 / img.size[0]
    img = img.resize((1200, int(img.size[1] * ratio)), Image.LANCZOS)
    img.save('/tmp/diagram_check.png')
# Then use Image read tool on /tmp/diagram_check.png
```
