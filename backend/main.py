from fastapi import FastAPI
from routers import metrics, transactions

app = FastAPI()

app.include_router(metrics.router)
app.include_router(transactions.router)


@app.get("/")
def read_root():
    return {
        "message": "💰 指标记账系统",
        "docs": "/docs",
        "metrics": "/metrics",
        "transactions": "/transactions",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
