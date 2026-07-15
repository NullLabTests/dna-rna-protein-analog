MODEL_CONTEXT_WINDOWS = {
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-turbo": 128000,
    "gpt-4o": 128000,
    "gpt-4o-mini": 128000,
    "gpt-3.5-turbo": 16385,
    "claude-3-opus": 200000,
    "claude-3-sonnet": 200000,
    "claude-3-haiku": 200000,
    "claude-3-5-sonnet": 200000,
    "llama-2": 4096,
    "llama-3": 8192,
    "llama-3-70b": 8192,
    "llama-3-8b": 8192,
    "mistral": 32768,
    "mixtral": 32768,
    "gemma": 8192,
}


def get_context_window(model: str) -> int | None:
    return MODEL_CONTEXT_WINDOWS.get(model)


def check_fit(
    token_count: int,
    model: str,
    reserve_output: int = 2048,
) -> dict:
    max_context = get_context_window(model)
    if max_context is None:
        return {"fit": None, "error": f"Unknown model: {model}"}

    available = max_context - reserve_output
    fits = token_count <= available

    return {
        "model": model,
        "context_window": max_context,
        "token_count": token_count,
        "reserved_output": reserve_output,
        "available_for_input": available,
        "fit": fits,
        "overshoot_by": max(0, token_count - available) if not fits else 0,
    }
