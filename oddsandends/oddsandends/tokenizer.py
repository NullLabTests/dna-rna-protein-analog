import re

MODEL_ENCODINGS = {
    "gpt-4": "cl100k_base",
    "gpt-4-turbo": "cl100k_base",
    "gpt-4o": "o200k_base",
    "gpt-4o-mini": "o200k_base",
    "gpt-3.5-turbo": "cl100k_base",
    "text-davinci-003": "p50k_base",
    "text-embedding-ada-002": "cl100k_base",
    "claude-3-opus": "cl100k_base",
    "claude-3-sonnet": "cl100k_base",
    "claude-3-haiku": "cl100k_base",
    "claude-3-5-sonnet": "cl100k_base",
    "llama-2": "llama",
    "llama-3": "llama",
    "mistral": "mistral",
    "mixtral": "mistral",
    "gemma": "gemma",
}

FALLBACK_WPM = 0.75
FALLBACK_CPT = 4.0

_ENCODING_CACHE = {}


def _get_tiktoken_encoding(model: str):
    import tiktoken
    enc_name = MODEL_ENCODINGS.get(model, "cl100k_base")
    if enc_name not in _ENCODING_CACHE:
        _ENCODING_CACHE[enc_name] = tiktoken.get_encoding(enc_name)
    return _ENCODING_CACHE[enc_name]


def count_tokens(text: str, model: str = "gpt-4") -> int:
    try:
        enc = _get_tiktoken_encoding(model)
        return len(enc.encode(text))
    except (ImportError, KeyError):
        return int(len(text) / FALLBACK_CPT)


def estimate_tokens(text: str) -> int:
    words = len(re.findall(r'\S+', text))
    return int(words * FALLBACK_WPM)


def count_messages(messages: list, model: str = "gpt-4") -> int:
    total = 0
    for msg in messages:
        total += count_tokens(msg.get("content", ""), model)
        total += 4
    total += 2
    return total


def format_token_count(text: str, model: str = "gpt-4") -> dict:
    try:
        exact = count_tokens(text, model)
    except ImportError:
        exact = None
    estimated = estimate_tokens(text)
    return {
        "model": model,
        "exact": exact,
        "estimated": estimated,
        "characters": len(text),
        "words": len(re.findall(r'\S+', text)),
    }
