from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Protocol

import requests


class Provider(Protocol):
    def generate(self, system_prompt: str, user_prompt: str) -> str: ...


@dataclass
class OpenAICompatibleProvider:
    base_url: str
    model: str
    api_key: str = ""
    timeout: int = 180
    temperature: float = 0.7

    @classmethod
    def from_environment(cls) -> "OpenAICompatibleProvider":
        base_url = os.environ.get("ATAS_LLM_BASE_URL", "").rstrip("/")
        model = os.environ.get("ATAS_LLM_MODEL", "")
        if not base_url or not model:
            raise ValueError("ATAS_LLM_BASE_URL and ATAS_LLM_MODEL are required")
        return cls(
            base_url=base_url,
            model=model,
            api_key=os.environ.get("ATAS_LLM_API_KEY", ""),
            timeout=int(os.environ.get("ATAS_LLM_TIMEOUT", "180")),
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": self.temperature,
                "response_format": {"type": "json_object"},
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


class MockProvider:
    """Produces deterministic placeholder bodies for testing the pipeline."""

    def __init__(self, messages: list[dict]):
        self.messages = messages

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        emails = []
        for message in self.messages:
            emails.append({
                "id": message["id"],
                "body": (
                    f"Draft body for {message['id']}. This placeholder confirms that "
                    "thread generation, validation, review, and merge are working."
                ),
            })
        return json.dumps({"emails": emails})
