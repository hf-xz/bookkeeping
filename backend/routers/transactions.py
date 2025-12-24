# backend/routers/transactions.py
from datetime import date, timedelta
from typing import List, Optional

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import Metric, Transaction
from pydantic import BaseModel, Field
from sqlalchemy import and_
from sqlalchemy.orm import Session

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# 📦 Pydantic 模型
class TransactionBase(BaseModel):
    metric_id: int = Field(..., gt=0)
    record_date: date = Field(default_factory=date.today)
    value: float = Field(..., description="数值（可正可负）")
    note: str = Field("", max_length=200)


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    metric_name: str  # 额外返回指标名，方便前端

    class Config:
        from_attributes = True


class ProfitResponse(BaseModel):
    record_date: date
    profit: float
    details: dict[str, float]  # {指标名: 贡献值}


# 🚀 路由
@router.post(
    "", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED
)
def upsert_transaction(txn: TransactionCreate, db: Session = Depends(get_db)):
    """
    新增或更新记账记录
    1. 如果同一指标、同一天的记录已存在，则更新该记录
    2. 否则新增记录
    """
    # 检查指标是否存在 & 是否激活
    metric = db.query(Metric).filter(Metric.id == txn.metric_id).first()
    if not metric:
        raise HTTPException(status_code=400, detail="指标ID不存在")
    if metric.is_active is False:
        raise HTTPException(status_code=400, detail="该指标已停用")

    # 检查是否已存在相同日期的记录
    db_txn = (
        db.query(Transaction)
        .filter(
            and_(
                Transaction.metric_id == txn.metric_id,
                Transaction.record_date == txn.record_date,
            )
        )
        .first()
    )

    if db_txn:
        # 已存在相同日期的记录，更新
        update_data = txn.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_txn, key, value)

        db.commit()
        db.refresh(db_txn)

        # 注入 metric_name
        db_txn.metric_name = metric.name
        return db_txn
    else:
        # 新建记录
        db_txn = Transaction(**txn.model_dump())
        db.add(db_txn)
        db.commit()
        db.refresh(db_txn)

        # 注入 metric_name
        db_txn.metric_name = metric.name
        return db_txn


@router.get("", response_model=List[TransactionResponse])
def read_transactions(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    metric_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Transaction).join(Metric)

    if start_date:
        query = query.filter(Transaction.record_date >= start_date)
    if end_date:
        query = query.filter(Transaction.record_date <= end_date)
    if metric_id:
        query = query.filter(Transaction.metric_id == metric_id)

    txns = query.order_by(Transaction.record_date.desc()).all()

    # 注入 metric_name
    for t in txns:
        t.metric_name = t.metric.name
    return txns


@router.get("/profit", response_model=List[ProfitResponse])
def get_profit_summary(
    start_date: date = date.today() - timedelta(days=30),
    end_date: date = date.today(),
    db: Session = Depends(get_db),
):
    """
    按日汇总加权利润
    返回：每天的总利润 + 各指标贡献明细
    """
    # 先查所有相关记录
    records = (
        db.query(
            Transaction.record_date,
            Metric.name.label("metric_name"),
            Transaction.value,
            Metric.weight,
        )
        .join(Metric)
        .filter(
            and_(
                Transaction.record_date >= start_date,
                Transaction.record_date <= end_date,
                Metric.is_active,
            )
        )
        .order_by(Transaction.record_date)
        .all()
    )

    # 按日期聚合
    daily_data = dict()

    for r in records:
        day = daily_data.get(r.record_date, {"total": 0.0, "details": dict()})
        day["details"][r.metric_name] = float(r.value * r.weight)
        day["total"] += float(r.value * r.weight)
        daily_data[r.record_date] = day

    # 转为列表
    result = [
        ProfitResponse(record_date=d, profit=v["total"], details=v["details"])
        for d, v in sorted(daily_data.items())
    ]
    return result
