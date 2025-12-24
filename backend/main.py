from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import metrics, transactions

app = FastAPI()

app.include_router(metrics.router)
app.include_router(transactions.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
