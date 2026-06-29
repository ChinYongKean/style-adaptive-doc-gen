---
type: Generator
title: "Reports"
description: "Generates styled .docx reports (infrastructure, DR, usage, assessment) via python-docx."
tags: [report, docx, infrastructure, DR]
timestamp: 2026-06-29T12:00:00+08:00
---

# Generator: Reports (Infrastructure, DR, Usage, Assessment)

## Output Format
`.docx` via python-docx — styled Word document with cover page, TOC, tables, callouts

## Input Required
1. **Style profile** — full profile (brand, headings, body, tables, callouts, prose)
2. **Content** — metrics, findings, architecture data, recommendations

## Generation Rules

### Document Structure (from profile)
```
1. Cover page (if profile.document.cover_page = true)
2. Version history (if profile.document.version_history = true)
3. Table of contents (if profile.document.table_of_contents = true)
4. Body sections (from content)
5. Summary/Conclusion
```

### Apply Profile to Every Element

**Headings:**
```python
heading = doc.add_heading(title, level=1)
run = heading.runs[0]
run.font.name = profile['brand']['heading_font']
run.font.size = Pt(profile['headings']['h1']['size_pt'])
run.font.color.rgb = RGBColor.from_string(profile['headings']['h1']['color'].lstrip('#'))
```

**Body:**
```python
para = doc.add_paragraph(text)
para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY  # from profile.body.alignment
run = para.runs[0]
run.font.name = profile['brand']['body_font']
run.font.size = Pt(profile['body']['font_size_pt'])
```

**Tables:**
```python
table = doc.add_table(rows=len(data)+1, cols=len(headers))
# Header row
for i, header in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = header
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), profile['tables']['header_bg'].lstrip('#'))
    cell._element.get_or_add_tcPr().append(shading)
```

### Prose Rules (from profile)
When writing body text, enforce:
- `prose.voice`: use active voice if "active"
- `prose.formality`: no contractions if "high"
- `prose.max_sentence_length`: split sentences exceeding limit
- `prose.filler_phrases`: remove "it is important to note that", etc.
- `prose.emoji_allowed`: strip emoji if false

### Callout Boxes
```python
def add_callout(doc, text, callout_type, profile):
    """Add a styled callout box (info/warning/error)."""
    colors = profile['callouts'][callout_type]
    # Create table with 1 row, colored left border
    table = doc.add_table(rows=1, cols=1)
    cell = table.rows[0].cells[0]
    cell.text = text
    # Apply border color and background from profile
```

### Report Types & Section Patterns

**Infrastructure Usage Report:**
```
1. Architecture Diagram
2. Account Information
3. Infrastructure Overview (KPI summary box)
4. Per-Service Sections (Lambda, DynamoDB, S3, EC2, etc.)
   - Each: description paragraph + data table + analysis paragraph
5. Recommendations
```

**DR/RTO Report:**
```
1. Overview & Scope
2. Account Information
3. Architecture Summary (service × AZ redundancy table)
4. Service Availability RTO/RPO
5. Data Recovery RTO/RPO
6. Consolidated Summary Table
```

**Security Assessment:**
```
1. Executive Summary
2. Scope & Methodology
3. Findings (per-service tables with severity)
4. Recommendations (prioritized)
5. Appendix (raw data, screenshots)
```

## Validation
After generation:
1. Open DOCX and verify heading colors match profile
2. Verify table header fills match profile
3. Check prose passes style rules (no filler, sentence length)
4. Verify cover page elements present if configured
