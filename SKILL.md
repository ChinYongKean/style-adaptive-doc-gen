---
type: Agent Skill
title: "Style-Adaptive Document Generation — Master Skill"
description: "Entry point that routes requests to style analysis, generation, or cost estimation based on user intent."
tags: [routing, orchestration, document-generation, master]
timestamp: 2026-06-29T12:00:00+08:00
version: "1.0"
---

# Style-Adaptive Document Generation — Master Skill

## Activation Triggers
- User asks to generate a document matching a reference style
- User provides a reference document and asks for style analysis
- User requests a report, diagram, task list, or technical doc with specific styling
- User asks to estimate cost/tokens for document generation

## Workflow Decision Tree

```
User Request
│
├─ "Analyze this document's style"
│  → Run style-analyzer.md
│  → Output: style-profile.yaml
│
├─ "Generate [doc type] using [style profile]"
│  → Check if style profile exists
│  → Route to appropriate generator:
│     ├─ Architecture diagram → generators/diagrams.md
│     ├─ Task list           → generators/task-lists.md
│     ├─ Report (DR/usage)   → generators/reports.md
│     └─ Technical doc       → generators/technical-docs.md
│
├─ "Generate [doc type] matching [reference doc]"
│  → Run style-analyzer.md first (extract profile)
│  → Then route to generator with profile
│
├─ "Estimate cost for [doc type]"
│  → Run token-calculator.md
│
└─ Large/complex document (>10 pages, multi-source)
   → Run orchestrator.md (sub-agent decomposition)
```

## Style Profile Format

Every generator consumes a `style-profile.yaml` with this structure:

```yaml
meta:
  extracted_from: "reference-document-name.docx"
  extraction_date: "2026-06-29"
  confidence: 0.92

brand:
  primary_color: "#5B2D8E"
  secondary_color: "#3C78D8"
  accent_color: "#ED7100"
  heading_font: "Arial"
  body_font: "Arial"
  logo_position: "bottom-center"
  company_info: "Company Name | Registration | Address"

document:
  cover_page: true
  version_history: true
  table_of_contents: true
  page_margins: {top: 2.54, bottom: 2.54, left: 3.0, right: 3.0}

headings:
  h1: {size: 14, bold: true, color: "$primary_color"}
  h2: {size: 13, bold: true, color: "$primary_color"}
  h3: {size: 11, bold: true, color: "$primary_color"}

body:
  font_size: 12
  color: "#1F1F1F"
  alignment: "justified"
  line_spacing: 1.15

tables:
  header_bg: "$secondary_color"
  header_text: "#FFFFFF"
  header_bold: true
  border_style: "grid"
  status_colors:
    good: "#C6EFCE"
    warn: "#FFF2CC"
    bad: "#F4CCCC"

callouts:
  info: {border_color: "#4472C4", bg: "#F5F5F5"}
  warning: {border_color: "#E6B800", bg: "#F5F5F5"}
  error: {border_color: "#CC0000", bg: "#F5F5F5"}

prose:
  voice: "active"
  formality: "high"
  max_sentence_length: 30
  contractions: false
  filler_phrases: false
  emoji: false

diagrams:
  icon_format: "productIcon"
  icon_size: 40
  canvas_width: 2400
  canvas_height: 1400
  flow_direction: "top-down"
  subnet_fills: {public: "#E9F3E6", private: "#E6F6F7"}
  edge_style: "orthogonal"
  numbered_flow: true
  legend: true
  title_block: true
```

## Rules

1. **Never generate without a style profile** — if none exists, extract one first or ask the user for a reference document.

2. **Style profiles are reusable** — once extracted, save and reference by name. Do not re-extract from the same document.

3. **Generators never hardcode visual values** — all colors, fonts, sizes come from the profile.

4. **For large documents (>10 pages)**, always use the orchestrator to decompose into sub-agent tasks.

5. **Always estimate tokens before generating** if the user has not explicitly said to proceed.

6. **Validate output against profile** — after generation, check that visual styling matches. Flag any deviations.

## File References

| File | Purpose |
|------|---------|
| `style-analyzer.md` | Extracts style from reference documents |
| `orchestrator.md` | Decomposes large tasks into sub-agents |
| `token-calculator.md` | Estimates cost before generation |
| `generators/diagrams.md` | Architecture diagram generation |
| `generators/task-lists.md` | Task list generation (xlsx) |
| `generators/reports.md` | Report generation (docx) |
| `generators/technical-docs.md` | Technical documentation |
