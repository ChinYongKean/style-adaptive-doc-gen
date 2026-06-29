#!/usr/bin/env python3
"""Token cost estimator for Style-Adaptive Document Generation."""
import argparse
import math

MODELS = {
    "sonnet": {"name": "Claude Sonnet 4", "input": 3.00, "output": 15.00},
    "haiku": {"name": "Claude Haiku 3.5", "input": 0.80, "output": 4.00},
    "gpt4o": {"name": "GPT-4o", "input": 2.50, "output": 10.00},
    "gpt4o-mini": {"name": "GPT-4o Mini", "input": 0.15, "output": 0.60},
}

DOC_TYPES = {
    "report": {"input_per_page": 500, "output_per_page": 800, "base_input": 3300},
    "task-list": {"input_per_page": 400, "output_per_page": 600, "base_input": 2800},
    "diagram": {"input_per_page": 2000, "output_per_page": 3000, "base_input": 2500},
    "technical-doc": {"input_per_page": 600, "output_per_page": 900, "base_input": 3300},
}

COMPLEXITY = {"simple": 1.0, "medium": 1.3, "complex": 1.7}


def estimate(doc_type, pages, model, complexity):
    dt = DOC_TYPES[doc_type]
    m = MODELS[model]
    cx = COMPLEXITY[complexity]

    input_tokens = math.ceil((dt["base_input"] + pages * dt["input_per_page"]) * cx)
    output_tokens = math.ceil(pages * dt["output_per_page"] * cx)

    input_cost = input_tokens * m["input"] / 1_000_000
    output_cost = output_tokens * m["output"] / 1_000_000
    total = input_cost + output_cost

    return {
        "model": m["name"],
        "doc_type": doc_type,
        "pages": pages,
        "complexity": complexity,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total,
    }


def main():
    parser = argparse.ArgumentParser(description="Estimate token cost for document generation")
    parser.add_argument("--type", choices=DOC_TYPES.keys(), required=True)
    parser.add_argument("--pages", type=int, required=True)
    parser.add_argument("--model", choices=MODELS.keys(), default="sonnet")
    parser.add_argument("--complexity", choices=COMPLEXITY.keys(), default="medium")
    args = parser.parse_args()

    r = estimate(args.type, args.pages, args.model, args.complexity)

    print(f"\nDocument: {r['doc_type']} ({r['pages']} pages)")
    print(f"Complexity: {r['complexity']} ({COMPLEXITY[r['complexity']]}x)")
    print(f"Model: {r['model']}")
    print(f"\nToken Breakdown:")
    print(f"  Input:  {r['input_tokens']:,} tokens (${r['input_cost']:.3f})")
    print(f"  Output: {r['output_tokens']:,} tokens (${r['output_cost']:.3f})")
    print(f"  Total:  {r['input_tokens']+r['output_tokens']:,} tokens (${r['total_cost']:.3f})")


if __name__ == "__main__":
    main()
