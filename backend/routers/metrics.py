# backend/routers/metrics.py
from typing import List

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import Metric
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

router = APIRouter(prefix="/metrics", tags=["Metrics"])


# 📦 Pydantic 模型
class MetricBase(BaseModel):
    name: str = Field(..., max_length=100, description="指标名称，如'销售额'")
    unit: str = Field("", max_length=20, description="单位，如'元'、'人'")
    weight: float = Field(1.0, description="权重（可为负值）")
    type: str = Field("", description="类型：如 'fixed'(固定)、'optional'(可选)")
    description: str = Field("", max_length=200, description="描述信息")
    is_active: bool = True


class MetricCreate(MetricBase):
    pass


class MetricUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    unit: str | None = Field(None, max_length=20)
    weight: float | None = None
    type: str | None = None
    description: str | None = Field(None, max_length=200)
    is_active: bool | None = None


class MetricResponse(MetricBase):
    id: int

    class Config:
        from_attributes = True  # SQLAlchemy 2.0+ 兼容


# 🚀 路由
@router.post("", response_model=MetricResponse, status_code=status.HTTP_201_CREATED)
def create_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    # 检查重名
    db_metric = db.query(Metric).filter(Metric.name == metric.name).first()
    if db_metric:
        raise HTTPException(status_code=400, detail=f"指标 '{metric.name}' 已存在")
    db_metric = Metric(**metric.model_dump())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.get("", response_model=List[MetricResponse])
def read_metrics(db: Session = Depends(get_db)):
    metrics = db.query(Metric).all()
    return metrics


@router.get("/{metric_id}", response_model=MetricResponse)
def read_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="指标不存在")
    return metric


@router.put("/{metric_id}", response_model=MetricResponse)
def update_metric(
    metric_id: int, metric_update: MetricUpdate, db: Session = Depends(get_db)
):
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="指标不存在")

    update_data = metric_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(metric, key, value)

    db.commit()
    db.refresh(metric)
    return metric


@router.delete("/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="指标不存在")
    db.delete(metric)
    db.commit()
    return
