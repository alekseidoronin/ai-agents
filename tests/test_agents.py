from app.agents.content_plan_agent import ContentPlanAgent
from app.agents.sales_funnel_agent import SalesFunnelAgent
from app.agents.analytics_agent import AnalyticsAgent


def test_content_plan_parse_topics():
    text = "- Тема 1: Введение | Цель: awareness\n- Тема 2: Обзор | Цель: engagement\nОбычная строка"
    result = ContentPlanAgent._parse_topics(text)
    assert len(result) == 2
    assert "Тема 1" in result[0]


def test_content_plan_build_schedule():
    topics = ["Тема A", "Тема B", "Тема C", "Тема D"]
    schedule = ContentPlanAgent._build_schedule(topics)
    assert "Неделя 1, Пн" in schedule
    assert "Неделя 1, Ср" in schedule
    assert "Неделя 1, Пт" in schedule
    assert "Неделя 2, Пн" in schedule
    assert schedule["Неделя 1, Пн"] == "Тема A"


def test_sales_funnel_parse_stages():
    text = "- Этап 1\n- Этап 2\n* Этап 3\nПросто текст"
    result = SalesFunnelAgent._parse_stages(text, fallback=["Fallback"])
    assert len(result) == 3
    assert result[0]["name"] == "Этап 1"


def test_sales_funnel_parse_stages_fallback():
    result = SalesFunnelAgent._parse_stages("Нет этапов", fallback=["A", "B"])
    assert len(result) == 2
    assert result[0]["name"] == "A"


def test_sales_funnel_extract_budget():
    text = "Некоторый текст\nРекомендуем бюджет 50 000 руб.\nЕщё текст"
    result = SalesFunnelAgent._extract_budget(text)
    assert result is not None
    assert "50 000" in result


def test_sales_funnel_extract_budget_none():
    assert SalesFunnelAgent._extract_budget("Просто обычный текст") is None


def test_sales_funnel_templates():
    assert "standard" in SalesFunnelAgent.FUNNEL_TEMPLATES
    assert "webinar" in SalesFunnelAgent.FUNNEL_TEMPLATES
    assert "tripwire" in SalesFunnelAgent.FUNNEL_TEMPLATES


def test_analytics_parse_insights():
    text = "Инсайты:\n- Рост конверсии на 20%\n- Падение трафика\n\nДругой раздел"
    result = AnalyticsAgent._parse_insights(text)
    assert len(result) == 2
    assert "Рост конверсии" in result[0]


def test_analytics_parse_recommendations():
    text = "Рекомендации:\n- Увеличить бюджет\n- Оптимизировать лендинг\n\nКонец"
    result = AnalyticsAgent._parse_recommendations(text)
    assert len(result) == 2
    assert "Увеличить бюджет" in result[0]
