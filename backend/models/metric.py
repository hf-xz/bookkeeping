# backend/models/metric.py
from database import Base
from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.orm import relationship


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)  # 如 "销售额"
    unit = Column(String(20), default="")  # 单位："人"、"元"、"次"
    weight = Column(Float, default=1.0, nullable=False)  # 权重
    # TODO fixed 改为 type
    fixed = Column(Boolean, default=False)  # 是否每日固定录入
    description = Column(String(200), default="")  # 描述（可选）
    is_active = Column(Boolean, default=True)

    # 反向关系：一个指标 → 多条记录
    transactions = relationship(
        "Transaction",
        back_populates="metric",
        cascade="all, delete-orphan",  # 删除指标时自动删记录
    )
