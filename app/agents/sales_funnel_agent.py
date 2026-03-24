from app.agents.base import BaseAgent


class SalesFunnelAgent(BaseAgent):
    agent_type = "sales_funnel"

    FUNNEL_TEMPLATES: dict[str, list[str]] = {
        "standard": [
            "Осведомлённость (Awareness)",
            "Интерес (Interest)",
            "Решение (Decision)",
            "Действие (Action)",
        ],
        "webinar": [
            "Лид-магнит / бесплатный контент",
            "Регистрация на вебинар",
            "Вебинар / презентация",
            "Оффер / продажа",
            "Upsell / допродажа",
        ],
        "tripwire": [
            "Привлечение трафика",
            "Лид-магнит",
            "Tripwire (недорогой продукт)",
            "Основной продукт",
            "Максимизация прибыли (Upsell)",
        ],
    }

    async def execute(
        self,
        *,
        product: str,
        audience: str,
        funnel_type: str = "standard",
    ) -> dict:
        template_stages = self.FUNNEL_TEMPLATES.get(
            funnel_type, self.FUNNEL_TEMPLATES["standard"]
        )

        prompt = self.load_prompt("sales_funnel.txt")
        user_message = (
            f"Продукт: {product}\n"
            f"ЦА: {audience}\n"
            f"Тип воронки: {funnel_type}\n"
            f"Этапы: {', '.join(template_stages)}"
        )

        raw = await self.call_openai(system_prompt=prompt, user_message=user_message)

        return {
            "funnel_type": funnel_type,
            "stages": self._parse_stages(raw, template_stages),
            "budget_recommendation": self._extract_budget(raw),
            "raw_response": raw,
        }

    @staticmethod
    def _parse_stages(text: str, fallback: list[str]) -> list[dict]:
        stages = []
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("-") or stripped.startswith("*"):
                stages.append({"name": stripped.lstrip("-* ").strip()})
        if not stages:
            stages = [{"name": s} for s in fallback]
        return stages

    @staticmethod
    def _extract_budget(text: str) -> str | None:
        lower = text.lower()
        for keyword in ["бюджет", "рекомендуем", "стоимость"]:
            idx = lower.find(keyword)
            if idx != -1:
                end = text.find("\n", idx)
                return text[idx: end if end != -1 else None].strip()
        return None
