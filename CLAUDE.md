# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A lottery shop bookkeeping system (彩票店记账系统) for tracking daily revenue and metrics.

- **Backend**: Python FastAPI + SQLAlchemy + SQLite
- **Frontend**: Vue 3 + TypeScript + Vant UI + Chart.js

## Commands

### Backend

```sh
cd backend

# 激活虚拟环境
source .venv/bin/activate

# 启动开发服务器（热更新）
fastapi dev

# 初始化数据库
python -m cli.init_db
```

### Frontend

```sh
cd frontend

# 安装依赖
yarn install

# 启动开发服务器
yarn dev
```

## Architecture

### Backend Structure

```
backend/
├── main.py           # FastAPI 入口，包含 CORS 配置
├── database.py       # SQLAlchemy 配置（SQLite）
├── models/           # ORM 模型
│   ├── metric.py     # 指标模型（含 MetricType 枚举）
│   └── transaction.py # 交易记录模型
├── routers/         # API 路由
│   ├── metrics.py    # 指标 CRUD 接口
│   └── transactions.py # 交易记录接口
└── cli/             # 命令行工具
    └── init_db.py   # 数据库初始化脚本
```

### Frontend Structure

```
frontend/src/
├── App.vue          # 根组件
├── main.ts          # 入口文件
├── router/          # Vue Router 配置
├── views/           # 页面组件
│   ├── HomeView.vue        # 首页（概览、图表）
│   ├── RecordView/         # 记录页面
│   │   ├── index.vue
│   │   └── DayRecordForm.vue
│   └── MetricView/         # 指标配置页面
│       └── index.vue
├── components/      # 可复用组件
│   └── charts/      # 图表组件（Chart.js）
├── apis/            # API 调用
├── models/          # TypeScript 类型定义
└── utils/           # 工具函数
```

### Database

- SQLite 数据库位于 `backend/app.db`
- 两个主要表：`metrics`（指标配置）和 `transactions`（每日记录）

### API Endpoints

- `GET /metrics` - 获取指标列表
- `POST/PUT/DELETE /metrics` - 指标的增删改
- `GET /transactions` - 获取交易记录（支持日期范围查询）
- `POST /transactions/bulk-upsert` - 批量 upsert 记录
- `GET /transactions/profit` - 获取利润统计

## Key Patterns

- Metric type enum: `daily` (每日必填) | `optional` (可选)
- 指标 type 字段使用 Python enum `MetricType` 验证
- 前端使用 `onActivated` 钩子刷新页面数据（Vue Router Tab 切换）
- 图表组件解耦到 `components/charts/` 目录
