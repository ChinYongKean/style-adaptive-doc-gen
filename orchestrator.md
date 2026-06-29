---
type: Agent Skill
title: "Orchestrator — Sub-Agent Workflow"
description: "Decomposes large document generation into parallel sub-agent tasks for context efficiency."
tags: [orchestration, sub-agent, parallel, workflow]
timestamp: 2026-06-29T12:00:00+08:00
version: "1.0"
---

# Orchestrator — Sub-Agent Workflow

## Purpose
Decompose large document generation tasks into focused sub-agent tasks that run in parallel, preserving main agent context for final assembly.

## When to Use
- Document requires >10 pages of output
- Multiple source materials need to be read and synthesized
- Style extraction + content gathering + generation in one request
- Context budget would be exhausted by reading all sources in main agent

## Workflow Pattern

```
USER REQUEST
│
▼
ORCHESTRATOR (main agent — stays lean, coordinates only)
│
├─── Sub-Agent 1: STYLE EXTRACTION ──────────────────────┐
│    "Read reference doc. Extract style profile YAML."    │
│    Input: reference document                            │
│    Output: style-profile.yaml                           │ PARALLEL
│                                                         │
├─── Sub-Agent 2: CONTENT GATHERING ─────────────────────┤
│    "Read source material. Extract structured data."     │
│    Input: source docs, codebases, configs               │
│    Output: content.json (facts, metrics, structure)     │
│                                                         │
├─── Sub-Agent 3: TOKEN ESTIMATION ──────────────────────┘
│    "Estimate tokens for this generation task."
│    Input: doc type, page count, complexity
│    Output: cost estimate
│
▼ (wait for all sub-agents)
│
├─── Sub-Agent 4: GENERATION ────────────────────────────┐
│    "Using style profile + content, generate document." │
│    Input: style-profile.yaml + content.json            │ SEQUENTIAL
│    Output: document (DOCX/XLSX/drawio/MD)              │
│                                                         │
├─── Sub-Agent 5: VALIDATION ────────────────────────────┘
│    "Compare output against style profile."
│    Input: generated doc + style-profile.yaml
│    Output: deviation report (pass/fix list)
│
▼
FINAL OUTPUT (or fix loop if validation fails)
```

## Sub-Agent Prompt Templates

### Sub-Agent 1: Style Extraction
```
Read the following reference document. Using the extraction checklist from
style-analyzer.md, extract every visual, structural, and prose styling rule.
Output as YAML following the style-profile schema exactly.

Reference: [path or content]
```

### Sub-Agent 2: Content Gathering
```
Read the following source material. Extract ALL factual content needed to
generate a [doc_type]. Output as structured JSON with these sections:

- metadata: {project_name, date, author, version}
- sections: [{title, content, metrics[], tables[]}]
- diagrams: [{name, components[], connections[]}]

Source: [path or content]
```

### Sub-Agent 3: Token Estimation
```
Estimate the token cost for generating this document:
- Type: [report/task-list/diagram/technical-doc]
- Pages: [estimated]
- Complexity: [simple/medium/complex]
- Model: [claude-sonnet/claude-haiku/gpt-4o]

Use the formulas from token-calculator.md.
```

### Sub-Agent 4: Generation
```
Generate a [doc_type] using:
- Style: [style-profile.yaml contents]
- Content: [content.json contents]
- Generator rules: [from generators/X.md]

Output the complete document. Apply every rule from the style profile.
```

### Sub-Agent 5: Validation
```
Compare this generated document against the style profile.
Check every field in the profile and verify the output matches.

Report format:
- PASS: [rule] — matches profile
- FIX: [rule] — expected [X], got [Y]

Style Profile: [yaml]
Generated Output: [document]
```

## Orchestrator Decision Logic

```python
def should_use_orchestrator(request):
    """Decide if sub-agent decomposition is needed."""
    triggers = [
        request.page_count > 10,
        request.source_count > 3,
        request.needs_style_extraction and request.needs_generation,
        request.estimated_input_tokens > 50000,
    ]
    return any(triggers)

def plan_sub_agents(request):
    """Plan which sub-agents to launch."""
    agents = []
    
    if not request.has_style_profile:
        agents.append(("style_extraction", PARALLEL))
    
    if request.has_source_material:
        agents.append(("content_gathering", PARALLEL))
    
    if request.user_wants_estimate:
        agents.append(("token_estimation", PARALLEL))
    
    # These always run sequentially after parallel phase
    agents.append(("generation", SEQUENTIAL))
    agents.append(("validation", SEQUENTIAL))
    
    return agents
```

## Context Budget Rules

| Phase | Max Context Usage |
|-------|-------------------|
| Style extraction | 30% of budget |
| Content gathering | 30% of budget |
| Generation | 50% of budget (largest) |
| Validation | 20% of budget |
| Orchestrator overhead | 10% of budget |

**Key rule:** Sub-agents output COMPACT structured data, never raw source material. The orchestrator receives only the distilled outputs.

## Error Handling

| Error | Action |
|-------|--------|
| Style extraction fails (unclear doc) | Ask user for clarification or a clearer reference |
| Content gathering incomplete | Flag missing sections, generate partial with placeholders |
| Generation exceeds context | Split into sections, generate per-section |
| Validation finds >5 deviations | Auto-fix loop (max 2 iterations), then flag to user |
