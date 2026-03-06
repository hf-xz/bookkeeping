# backend/database.py
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# 数据库路径从环境变量读取，默认当前目录
DB_PATH = os.getenv("DB_PATH", "./app.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

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
