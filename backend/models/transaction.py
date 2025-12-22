# backend/models/transaction.py
from database import Base
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(
        Integer, ForeignKey("metrics.id", ondelete="CASCADE"), nullable=False
    )
    record_date = Column(Date, index=True, nullable=False)  # 按天聚合
    value = Column(Float, nullable=False)
    note = Column(String(200), default="")  # 备注（可选）

    # 关系
    metric = relationship("Metric", back_populates="transactions")

    # 联合唯一约束：每天每个指标只允许一条记录（防重复）
    __table_args__ = ({"sqlite_autoincrement": True},)
