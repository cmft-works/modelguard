import asyncio

TOKEN_DIVISOR = 4
MODEL_COSTS = {
    "gpt-4o-mini": (0.00015, 0.0006),
    "gpt-4.1": (0.002, 0.008),
    "claude-3-5-sonnet": (0.003, 0.015),
    "gemini-1.5-pro": (0.0035, 0.0105),
    "internal-llama": (0.00005, 0.00005),
}

def estimate_tokens(text: str) -> int:
    return max(1, len(text) // TOKEN_DIVISOR)

def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    in_cost, out_cost = MODEL_COSTS.get(model, (0.001, 0.003))
    return round((input_tokens / 1000 * in_cost) + (output_tokens / 1000 * out_cost), 6)

async def call_model(provider: str, model: str, prompt: str) -> tuple[str, int, int, int, float]:
    start_delay_ms = 120
    await asyncio.sleep(start_delay_ms / 1000)
    input_tokens = estimate_tokens(prompt)
    response = f"Mock {provider}/{model} response. Replace provider_router.py with real SDK calls when API keys are available."
    output_tokens = estimate_tokens(response)
    cost = estimate_cost(model, input_tokens, output_tokens)
    return response, input_tokens, output_tokens, start_delay_ms, cost
