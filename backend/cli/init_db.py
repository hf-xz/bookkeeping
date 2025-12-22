"""
backend/cli/init_db.py
初始化数据库脚本。
"""

from database import Base, engine
from models import *  # noqa: F403 导入所有模型以确保它们被注册


# 初始化数据库（创建所有表）
def init_db():
    """
    初始化数据库，创建所有表。
    """

    print("Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


if __name__ == "__main__":
    init_db()
