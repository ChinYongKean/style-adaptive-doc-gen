---
type: Generator
title: "Technical Documentation"
description: "Generates system technical documentation with 11-section standard structure."
tags: [technical-doc, system-doc, documentation]
timestamp: 2026-06-29T12:00:00+08:00
---

# Generator: Technical Documentation

## Output Format
`.docx` (formal delivery) or `.md` (internal/GitHub) — determined by user preference

## Input Required
1. **Style profile** — full profile (brand, headings, body, tables, prose)
2. **Content** — system architecture, components, APIs, configs, flows

## Generation Rules

### Standard Section Structure
```
1. Introduction (Overview, Scope, Audience)
2. System Architecture (diagram + tech stack)
3. Application Architecture (components, directory structure)
4. Integration Architecture (per external system)
5. Data Architecture (per data store: schema, access patterns)
6. Technical Architecture (per module: functions, classes, configs)
7. API Specification (endpoints, params, responses)
8. Security (auth, network, secrets)
9. Backend Processing (per feature: flow, error handling)
10. Operations (install, config, health checks, troubleshooting)
11. Limitations & Roadmap
```

### Content Patterns

**Per-Component Section:**
- 1-2 sentence overview
- Function/method reference table: `| Function | Parameters | Returns | Description |`
- Key code patterns (short inline snippets)
- Configuration constants table

**Per-Feature Flow:**
- Numbered step-by-step sequence
- Branching logic as indented sub-steps
- Error paths documented separately
- References to specific function names

**Per-Integration:**
- Protocol + auth method
- Base URL/connection details
- Request/response examples
- Data format specification

### Tables vs Prose Decision
| Content Type | Format |
|---|---|
| Function references | Table |
| Configuration params | Table |
| API endpoints | Table |
| Troubleshooting | Table (problem → cause → solution) |
| Architecture decisions | Prose |
| Flow descriptions | Numbered steps |
| Design rationale | Prose |
| Warnings/important notes | Callout box |

### Prose Rules for Technical Docs
- Use consistent terminology (one term per concept)
- Reference specific file/function names in backticks
- Include code snippets for non-obvious patterns
- Every claim needs a mechanism or file reference
- No vague qualifiers ("various", "several", "issues")

## Validation
1. Every section from the structure is present or explicitly marked N/A
2. All function tables have complete columns
3. Code snippets are syntactically valid
4. Cross-references (function names, file paths) are consistent
5. Prose passes style profile rules
