---
type: Generator
title: "Task Lists"
description: "Generates styled .xlsx task lists via openpyxl with profile-driven colors."
tags: [task-list, xlsx, openpyxl, project-management]
timestamp: 2026-06-29T12:00:00+08:00
---

# Generator: Task Lists

## Output Format
`.xlsx` via Python openpyxl — styled spreadsheet with tabs, colors, merged cells

## Input Required
1. **Style profile** — `tables` + `brand` sections (colors, fonts)
2. **Content** — phases, sections, tasks with owners/dates/dependencies

## Generation Rules

### Structure (adapt from style profile)
- Tab structure determined by project complexity (discuss with user first)
- Column headers use `tables.header_bg` and `tables.header_text_color`
- Section headers use bold + light fill from profile
- Task numbering: hierarchical (1.1, 1.2, 2.1, etc.)

### Visual Styling (from profile)
```python
# Apply from style profile:
header_fill = PatternFill(fgColor=profile['tables']['header_bg'].strip('#'))
header_font = Font(name=profile['brand']['heading_font'], size=12, bold=True,
                   color=profile['tables']['header_text_color'].strip('#'))
body_font = Font(name=profile['brand']['body_font'], size=12)
section_fill = PatternFill(fgColor=profile['brand']['secondary_color'].strip('#'))
```

### Task Description Rules
1. Start with action verb (Create, Deploy, Configure, Validate, Test)
2. Concise imperative sentences
3. Include technical specifics (service names, IPs, configs)
4. No period at end
5. Placeholder format: XXX or X.X.X.X for values to be filled

### Column Patterns
Standard columns (adapt based on project):
```
| # | Task | Owner | Org | Status | Start | End | Remarks | Dependencies |
```

### Tab Patterns
- **Pre-work** — preparation, prerequisites, information gathering
- **Implementation** — main build/deploy tasks
- **Cutover** — go-live steps with rollback plan
- **Post-implementation** — validation, monitoring, handover

## Python Generation Pattern

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def generate_task_list(profile, content, output_path):
    wb = Workbook()
    
    # Apply profile styling
    hdr_fill = PatternFill('solid', fgColor=profile['tables']['header_bg'].lstrip('#'))
    hdr_font = Font(name=profile['brand']['heading_font'], size=12, bold=True,
                    color=profile['tables']['header_text_color'].lstrip('#'))
    
    for tab in content['tabs']:
        ws = wb.create_sheet(tab['name'])
        # Header row
        for col, header in enumerate(tab['columns'], 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.fill = hdr_fill
            cell.font = hdr_font
        # Task rows
        for row_idx, task in enumerate(tab['tasks'], 2):
            for col, value in enumerate(task.values(), 1):
                ws.cell(row=row_idx, column=col, value=value)
    
    wb.remove(wb['Sheet'])  # Remove default
    wb.save(output_path)
```
