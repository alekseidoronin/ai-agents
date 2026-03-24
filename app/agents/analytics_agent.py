from app.agents.base import BaseAgent


class AnalyticsAgent(BaseAgent):
    agent_type = "analytics"

    async def execute(self, *, data_description: str, goal: str) -> dict:
        prompt = self.load_prompt("analytics.txt")
        user_message = f"Данные: {data_description}\nЦель анализа: {goal}"

        raw = await self.call_openai(
            system_prompt=prompt,
            user_message=user_message,
            temperature=0.3,
        )

        return {
            "insights": self._parse_insights(raw),
            "recommendations": self._parse_recommendations(raw),
            "raw_response": raw,
        }

    @staticmethod
    def _parse_insights(text: str) -> list[str]:
        insights = []
        capture = False
        for line in text.split("\n"):
            lower = line.lower().strip()
            if "инсайт" in lower or "вывод" in lower or "наблюдени" in lower:
                capture = True
                continue
            if capture and line.strip().startswith(("-", "*", "•")):
                insights.append(line.strip().lstrip("-*• ").strip())
            elif capture and line.strip() == "":
                capture = False
        return insights

    @staticmethod
    def _parse_recommendations(text: str) -> list[str]:
        recs = []
        capture = False
        for line in text.split("\n"):
            lower = line.lower().strip()
            if "рекомендац" in lower or "предложени" in lower:
                capture = True
                continue
            if capture and line.strip().startswith(("-", "*", "•")):
                recs.append(line.strip().lstrip("-*• ").strip())
            elif capture and line.strip() == "":
                capture = False
        return recs
