# backend/database.py
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# SQLite 数据库 URL（相对路径：项目根目录下的 ./app.db）
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# 关键：SQLite 支持多线程需加 connect_args（仅同步用）
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 特有
    # 可选：避免频繁创建文件句柄（适用于测试/开发）
    poolclass=StaticPool,
)

# Session 工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 基类
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
