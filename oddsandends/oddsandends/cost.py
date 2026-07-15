MODEL_PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "claude-3-opus": {"input": 15.00, "output": 75.00},
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "llama-3-70b": {"input": 0.65, "output": 0.65},
    "llama-3-8b": {"input": 0.20, "output": 0.20},
    "mistral-large": {"input": 2.00, "output": 6.00},
    "mistral-medium": {"input": 0.70, "output": 2.10},
    "mixtral-8x7b": {"input": 0.70, "output": 0.70},
}


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "gpt-4o",
) -> dict:
    pricing = MODEL_PRICING.get(model)
    if pricing is None:
        return {"error": f"Unknown model: {model}"}

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    total = input_cost + output_cost

    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total, 6),
        "pricing_per_1m": pricing,
    }


def list_models() -> list[dict]:
    return [
        {"model": m, "input_price": p["input"], "output_price": p["output"]}
        for m, p in sorted(MODEL_PRICING.items())
    ]
