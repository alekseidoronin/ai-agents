from abc import ABC, abstractmethod
from pathlib import Path

import openai
from anthropic import Anthropic

from app.config import settings

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class BaseAgent(ABC):
    """Base class for all AI agents on the platform."""

    agent_type: str = "base"

    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)

    def load_prompt(self, filename: str) -> str:
        return (PROMPTS_DIR / filename).read_text(encoding="utf-8")

    async def call_openai(
        self,
        system_prompt: str,
        user_message: str,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
    ) -> str:
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content

    @abstractmethod
    async def execute(self, **kwargs) -> dict:
        """Run the agent's main task. Must be implemented by subclasses."""
