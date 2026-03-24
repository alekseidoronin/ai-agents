from app.agents import ContentPlanAgent, SalesFunnelAgent, AnalyticsAgent


class AIService:
    """Facade over all AI agents for use in routers and Telegram bot."""

    def __init__(self):
        self.content_plan_agent = ContentPlanAgent()
        self.sales_funnel_agent = SalesFunnelAgent()
        self.analytics_agent = AnalyticsAgent()

    async def generate_content_plan(self, product: str, audience: str) -> dict:
        return await self.content_plan_agent.execute(product=product, audience=audience)

    async def generate_sales_funnel(
        self,
        product: str,
        audience: str,
        funnel_type: str = "standard",
    ) -> dict:
        return await self.sales_funnel_agent.execute(
            product=product, audience=audience, funnel_type=funnel_type
        )

    async def run_analytics(self, data_description: str, goal: str) -> dict:
        return await self.analytics_agent.execute(
            data_description=data_description, goal=goal
        )
