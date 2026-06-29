---
type: Agent Skill
title: "Style Analyzer — Core Extraction Engine"
description: "Extracts visual, structural, and prose styling rules from any reference document into a portable YAML style profile."
tags: [style-extraction, YAML, analysis, core]
timestamp: 2026-06-29T12:00:00+08:00
version: "1.0"
---

# Style Analyzer — Core Extraction Engine

## Purpose
Extract every visual, structural, and prose styling rule from a reference document into a portable YAML style profile. This profile drives all downstream generation.

## When to Use
- User provides a reference document (DOCX, PDF, HTML, screenshot, or markdown)
- User says "match this style" or "use this format"
- First-time generation for a new client/brand

## Input Types & Extraction Methods

| Input | Method |
|-------|--------|
| DOCX file | Parse with python-docx: extract styles, colors, fonts, spacing programmatically |
| PDF file | Convert to images → visual analysis; or extract text structure |
| Screenshot/PNG | Visual analysis: identify colors, layout, fonts from pixels |
| HTML (saved webpage) | Parse DOM structure, extract CSS values |
| Markdown | Analyze heading levels, table patterns, prose style |
| Existing style profile | Load directly, skip extraction |

## Extraction Checklist

When analyzing a reference document, extract ALL of the following. Miss nothing.

### 1. Brand Identity
```
□ Primary color (headings, accents)
□ Secondary color (table headers, links)
□ Accent color (callouts, highlights)
□ Logo placement (top-left, bottom-center, etc.)
□ Company name/info line format
□ Cover page layout (title position, subtitle, version)
```

### 2. Typography
```
□ Heading font family + sizes for H1, H2, H3
□ Body font family + size
□ Bold/italic patterns (when are they used?)
□ Font colors (body, headings, sub-headings, labels)
□ Line spacing / paragraph spacing
□ Alignment (justified, left, center)
```

### 3. Page Layout
```
□ Margins (top, bottom, left, right)
□ Header content (logo? page number?)
□ Footer content (page number? company info?)
□ Cover page present? Version history page?
□ Table of contents format
□ Page orientation (portrait/landscape)
```

### 4. Table Styling
```
□ Header row background color
□ Header text color + weight
□ Border style (full grid, horizontal only, minimal)
□ Alternating row fills?
□ Status indicator colors (green/yellow/red for values)
□ Cell padding
□ Column alignment patterns
```

### 5. Callout/Highlight Boxes
```
□ Background color
□ Border style (left-bar, full border, none)
□ Border color by type (info/warning/error)
□ Icon usage (emoji? symbol? none?)
□ Font style inside callouts (italic? smaller?)
```

### 6. Prose Style
```
□ Voice (active/passive)
□ Formality level (high/medium/casual)
□ Sentence length tendency (short <15, medium 15-25, long 25+)
□ Contractions used? (don't vs do not)
□ Filler phrases present? (it is important to note...)
□ Transition words frequency
□ Technical depth (service names? instance IDs? or high-level?)
□ Audience targeting (technical/executive/mixed)
```

### 7. Content Structure
```
□ Section numbering format (1.1, 1.1.1, or unnumbered)
□ Typical section order for this doc type
□ Use of tables vs prose vs bullet points ratio
□ Summary/overview sections present?
□ Appendix/reference sections?
□ Metric/KPI presentation format (inline, dashboard boxes, tables)
```

### 8. Diagram Style (if diagrams present)
```
□ Icon set (AWS official, generic, custom)
□ Flow direction (top-down, left-right)
□ Numbered flow steps? (①②③)
□ Color zones (green=public, blue=private, pink=account)
□ Title block present?
□ Legend/key present?
□ Edge style (orthogonal, curved, straight)
□ Annotation/callout boxes on diagrams?
□ Canvas size tendency
```

## Extraction Prompts by Input Type

### For DOCX (programmatic)
```python
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document('reference.docx')

# Extract heading styles
for style in doc.styles:
    if style.type == 1:  # Paragraph style
        font = style.font
        print(f"{style.name}: {font.name}, {font.size}, {font.color.rgb}, bold={font.bold}")

# Extract table styles
for table in doc.tables:
    first_row = table.rows[0]
    for cell in first_row.cells:
        shading = cell._element.find('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}shd')
        if shading is not None:
            fill = shading.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fill')
            print(f"Table header fill: #{fill}")
```

### For Screenshot/Image (visual analysis)
When reading an image of a document, answer these questions:
1. What colors dominate headings? (extract hex approximation)
2. What font appears to be used? (serif/sans-serif, approximate family)
3. How are tables styled? (header color, borders)
4. What is the page layout? (margins, columns)
5. Are there callout boxes? What color/style?
6. Is the tone formal or casual? (from visible text)
7. Are diagrams present? What style?

### For HTML (parse directly)
```python
from bs4 import BeautifulSoup
import re

with open('reference.html') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Extract inline styles and CSS classes
for heading in soup.find_all(['h1','h2','h3']):
    style = heading.get('style', '')
    color_match = re.search(r'color:\s*(#[0-9a-fA-F]{6})', style)
    if color_match:
        print(f"{heading.name}: {color_match.group(1)}")
```

## Output Format

Always output as YAML. Use this exact structure:

```yaml
meta:
  extracted_from: "[filename or description]"
  extraction_date: "[ISO date]"
  confidence: [0.0-1.0]  # How confident are you in the extraction?
  notes: "[any ambiguities or assumptions]"

brand:
  primary_color: "#XXXXXX"
  secondary_color: "#XXXXXX"
  accent_color: "#XXXXXX"
  heading_font: "[font family]"
  body_font: "[font family]"
  logo_position: "[position]"
  company_info: "[format string]"

document:
  cover_page: [true/false]
  version_history: [true/false]
  table_of_contents: [true/false]
  page_margins:
    top_cm: [number]
    bottom_cm: [number]
    left_cm: [number]
    right_cm: [number]
  orientation: "[portrait/landscape]"

headings:
  h1: {size_pt: [n], bold: [bool], color: "[hex]"}
  h2: {size_pt: [n], bold: [bool], color: "[hex]"}
  h3: {size_pt: [n], bold: [bool], color: "[hex]"}
  numbering: "[1.1|1.1.1|none]"

body:
  font_size_pt: [n]
  color: "[hex]"
  alignment: "[justified|left|center]"
  line_spacing: [number]

tables:
  header_bg: "[hex]"
  header_text_color: "#FFFFFF"
  header_bold: true
  border: "[grid|horizontal|minimal|none]"
  alternating_rows: [true/false]
  status_colors:
    good: "[hex]"
    warn: "[hex]"
    bad: "[hex]"

callouts:
  style: "[left-bar|full-border|background-only]"
  info: {border: "[hex]", bg: "[hex]"}
  warning: {border: "[hex]", bg: "[hex]"}
  error: {border: "[hex]", bg: "[hex]"}

prose:
  voice: "[active|passive|mixed]"
  formality: "[high|medium|casual]"
  max_sentence_length: [number]
  contractions: [true/false]
  filler_phrases: [true/false]
  emoji_allowed: [true/false]
  audience: "[technical|executive|mixed]"

structure:
  sections_numbered: [true/false]
  content_ratio:
    tables: [0-100]%
    prose: [0-100]%
    bullets: [0-100]%
  has_summary_boxes: [true/false]
  has_appendix: [true/false]

diagrams:
  icon_set: "[aws-official|generic|custom]"
  icon_format: "[productIcon|resourceIcon|mixed]"
  icon_size_px: [number]
  flow_direction: "[top-down|left-right]"
  numbered_flow: [true/false]
  legend: [true/false]
  title_block: [true/false]
  subnet_fills:
    public: "[hex]"
    private: "[hex]"
  edge_style: "[orthogonal|curved|straight]"
  callout_boxes: [true/false]
  canvas_width: [number]
  canvas_height: [number]
```

## Confidence Scoring

Rate your extraction confidence:
- **0.9-1.0**: Programmatic extraction from DOCX/HTML with explicit values
- **0.7-0.9**: Clear visual analysis from high-res screenshot
- **0.5-0.7**: Inference from low-res image or partial document
- **<0.5**: Mostly guessing — flag to user and ask for clarification

## Rules
1. **Extract, do not invent** — if you cannot determine a value, mark it as `null` with a note
2. **Hex colors must be exact** — do not approximate unless from image analysis (note confidence)
3. **Test with a small generation** — after extraction, generate one paragraph + one table to verify the profile looks correct before full generation
4. **One profile per client/brand** — do not mix styles from different sources into one profile
