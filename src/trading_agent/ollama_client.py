"""Ollama cloud chat integration."""

from trading_agent.config import get_ollama_api_key

from ollama import Client


OLLAMA_MODEL = "gemma4:31b"


def chat_with_ollama(prompt: str) -> str:
    """Send a user prompt to the configured Ollama cloud model."""
    from ollama import Client

    prompt = prompt.strip()
    if not prompt:
        raise ValueError("Prompt cannot be empty.")

    client = Client(
        host="https://ollama.com",
        headers={"Authorization": "Bearer " + get_ollama_api_key()},
    )
    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content


def get_client() -> Client:
    return Client(
        host="https://ollama.com",
        headers={"Authorization": "Bearer " + get_ollama_api_key()}
    )

def get_model() -> str:
    return OLLAMA_MODEL;