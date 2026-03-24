import openai
from anthropic import Anthropic
from app.config import settings

class AIService:
    def __init__(self):
        self.openai = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        self.anthropic = Anthropic(api_key=settings.anthropic_api_key)

    async def generate_content_plan(self, product: str, audience: str) -> list:
        prompt = self._load_prompt("content_plan.txt")

        response = await self.openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Продукт: {product}\nЦА: {audience}"}
            ],
            temperature=0.7
        )

        return self._parse_topics(response.choices[0].message.content)

    def _load_prompt(self, filename: str) -> str:
        with open(f"app/prompts/{filename}", "r") as f:
            return f.read()

    def _parse_topics(self, text: str) -> list:
        # Парсинг ответа AI
        return [line.strip("- ") for line in text.split("\n") if line.strip().startswith("-")]
