---
type: Agent Skill
title: "Token Calculator — Cost Estimation"
description: "Estimates input/output tokens and dollar cost for document generation tasks before execution."
tags: [tokens, cost, estimation, pricing]
timestamp: 2026-06-29T12:00:00+08:00
version: "1.0"
---

# Token Calculator — Cost Estimation

## Purpose
Estimate input/output tokens and dollar cost for a document generation task before execution.

## Token Estimation Formulas

### Input Tokens (what the model reads)

| Component | Formula |
|-----------|---------|
| Style profile | ~800 tokens (fixed YAML) |
| Reference doc (for extraction) | pages × 600 tokens |
| Source material | pages × 500 tokens |
| Generator prompt | ~1,500 tokens (fixed) |
| Orchestrator overhead | ~500 tokens per sub-agent |
| Validation prompt | ~1,000 tokens |

### Output Tokens (what the model generates)

| Document Type | Formula |
|---------------|---------|
| Report (DOCX) | pages × 800 tokens |
| Task list (XLSX) | tabs × tasks × 50 tokens |
| Architecture diagram (.drawio) | components × 200 tokens |
| Technical doc | pages × 900 tokens |
| Style profile extraction | ~1,200 tokens (fixed) |

### Complexity Multipliers

| Complexity | Multiplier | When |
|-----------|-----------|------|
| Simple | 1.0x | Single source, straightforward content |
| Medium | 1.3x | Multiple sources, some analysis needed |
| Complex | 1.7x | Large codebase, cross-referencing, deep analysis |

## Model Pricing (as of 2026)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude Sonnet 4 | $3.00 | $15.00 |
| Claude Haiku 3.5 | $0.80 | $4.00 |
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |

## Quick Estimates by Document Type

| Document | Pages | Est. Input | Est. Output | Cost (Sonnet) |
|----------|-------|-----------|------------|---------------|
| Monthly infra report | 15 | 12K | 12K | $0.22 |
| DR/RTO report | 10 | 8K | 8K | $0.14 |
| Technical system doc | 25 | 18K | 22K | $0.38 |
| Architecture diagram | 1 | 4K | 6K | $0.10 |
| Migration task list | 5 tabs | 6K | 8K | $0.14 |
| Style extraction only | - | 4K | 1.2K | $0.03 |

## Calculation Example

```
Task: Generate 15-page infrastructure report
Model: Claude Sonnet 4
Complexity: Medium (1.3x)

Input tokens:
  Style profile:        800
  Source material:    7,500  (15 pages × 500)
  Generator prompt:   1,500
  Validation:         1,000
  ─────────────────────────
  Subtotal:          10,800
  × 1.3 complexity:  14,040

Output tokens:
  Report content:    12,000  (15 pages × 800)
  × 1.3 complexity:  15,600

Cost:
  Input:  14,040 × $3.00/1M  = $0.042
  Output: 15,600 × $15.00/1M = $0.234
  ─────────────────────────────────────
  Total:                        $0.276
```

## Usage

```bash
python tools/estimate_tokens.py --type report --pages 15 --model sonnet --complexity medium
```

Output:
```
Document: Infrastructure Report (15 pages)
Complexity: Medium (1.3x)
Model: Claude Sonnet 4

Token Breakdown:
  Input:  14,040 tokens ($0.042)
  Output: 15,600 tokens ($0.234)
  Total:  29,640 tokens ($0.276)
```
