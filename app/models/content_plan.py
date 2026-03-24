from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base

class ContentPlan(Base):
    __tablename__ = "content_plans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_name = Column(String(255))
    target_audience = Column(Text)
    topics = Column(JSON)  # Список тем
    schedule = Column(JSON)  # Календарь публикаций
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
