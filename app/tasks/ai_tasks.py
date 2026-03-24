import asyncio
import logging

from app.celery_app import celery

logger = logging.getLogger("ai_agents.tasks")


def _run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery.task(bind=True, max_retries=3, default_retry_delay=30)
def generate_content_plan_task(self, product: str, audience: str) -> dict:
    from app.agents.content_plan_agent import ContentPlanAgent

    logger.info("Generating content plan for product=%s", product)
    try:
        agent = ContentPlanAgent()
        return _run_async(agent.execute(product=product, audience=audience))
    except Exception as exc:
        logger.exception("Content plan generation failed")
        raise self.retry(exc=exc)


@celery.task(bind=True, max_retries=3, default_retry_delay=30)
def generate_sales_funnel_task(
    self,
    product: str,
    audience: str,
    funnel_type: str = "standard",
) -> dict:
    from app.agents.sales_funnel_agent import SalesFunnelAgent

    logger.info("Generating sales funnel for product=%s type=%s", product, funnel_type)
    try:
        agent = SalesFunnelAgent()
        return _run_async(
            agent.execute(product=product, audience=audience, funnel_type=funnel_type)
        )
    except Exception as exc:
        logger.exception("Sales funnel generation failed")
        raise self.retry(exc=exc)


@celery.task(bind=True, max_retries=3, default_retry_delay=30)
def run_analytics_task(self, data_description: str, goal: str) -> dict:
    from app.agents.analytics_agent import AnalyticsAgent

    logger.info("Running analytics, goal=%s", goal)
    try:
        agent = AnalyticsAgent()
        return _run_async(agent.execute(data_description=data_description, goal=goal))
    except Exception as exc:
        logger.exception("Analytics task failed")
        raise self.retry(exc=exc)
