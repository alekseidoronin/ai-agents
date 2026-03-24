from app.agents.base import BaseAgent


class ContentPlanAgent(BaseAgent):
    agent_type = "content_plan"

    async def execute(self, *, product: str, audience: str) -> dict:
        prompt = self.load_prompt("content_plan.txt")
        user_message = f"Продукт: {product}\nЦА: {audience}"

        raw = await self.call_openai(system_prompt=prompt, user_message=user_message)
        topics = self._parse_topics(raw)

        return {
            "topics": topics,
            "schedule": self._build_schedule(topics),
            "raw_response": raw,
        }

    @staticmethod
    def _parse_topics(text: str) -> list[str]:
        return [
            line.strip("- ").strip()
            for line in text.split("\n")
            if line.strip().startswith("-")
        ]

    @staticmethod
    def _build_schedule(topics: list[str]) -> dict:
        schedule = {}
        for i, topic in enumerate(topics):
            week = i // 3 + 1
            day = ["Пн", "Ср", "Пт"][i % 3]
            schedule[f"Неделя {week}, {day}"] = topic
        return schedule
